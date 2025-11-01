# Entity Management - Django Project Documentation

## Project Overview

**entity_management** is a Django-based member management system for Studylife München e.V., a student organization. It handles member applications, member registration, payment tracking, and administrative operations through Django's admin interface.

- **Live URL**: https://studylife-muenchen.de
- **Hosted on**: Uberspace
- **Language**: German (all UI/models use German labels)
- **Git Repository**: https://github.com/zypriafl/entity_management

## Tech Stack

### Core Framework
- **Django**: Latest version (currently 5.2.7)
- **Python**: 3.8+ (CircleCI uses 3.8, venv uses 3.11)
- **Database**: SQLite3 (development), migrates to Uberspace deployment

### Key Dependencies
```
Django
django-localflavor          # IBAN/BIC field validation, SEPA support
django-recaptcha            # Google reCAPTCHA integration (v2 No-Captcha)
pytz                        # Timezone support
coverage                    # Code coverage reporting
fabric3                     # Deployment automation
flake8                      # Linting
```

### Deployment
- **CI/CD**: CircleCI 2.0
- **Deployment Tool**: Fabric (fabfile.py)
- **Server**: Uberspace with supervisor process manager
- **Web Server**: WSGI-based
- **Static Files**: Collected to `/home/study/html/static/` on production

## Project Structure

```
entity_management/
├── entity_management/          # Main Django project settings
│   ├── settings.py            # Base settings (DEBUG=True, SQLite3)
│   ├── urls.py                # Main URL router
│   ├── wsgi.py                # WSGI application
│   └── __init__.py
├── config/                    # Environment-specific settings
│   ├── production.py          # Production settings (reads env vars, HTTPS enabled)
│   ├── deployment.py          # Deployment settings (static files path)
│   └── __init__.py
├── application/               # Main app - member applications & verification
│   ├── models.py              # MemberApplication model
│   ├── views.py               # Login, verification, impressum views
│   ├── admin.py               # MemberApplication admin with actions
│   ├── forms.py               # CaptchaLoginForm
│   ├── tests.py               # Comprehensive test suite
│   ├── migrations/
│   ├── templatetags/          # Custom template tags
│   └── apps.py
├── member/                    # Member management app
│   ├── models.py              # Member model
│   ├── admin.py               # Member admin with CSV export
│   ├── migrations/
│   ├── views.py               # (empty, no views)
│   ├── tests.py               # (minimal)
│   └── apps.py
├── email_template/            # Email templating system
│   ├── models.py              # EmailTemplate model with 4 template types
│   ├── helpers.py             # send_template_mail() utility
│   ├── admin.py               # EmailTemplate admin
│   ├── migrations/
│   └── views.py               # (empty)
├── templates/                 # Global templates
│   ├── base.html
│   ├── impressum.html
│   ├── admin/                 # Custom admin templates
│   │   ├── base.html
│   │   ├── base_site.html
│   │   ├── change_form.html
│   │   └── submit_line.html
│   ├── accounting/
│   │   └── reimbursement.html
│   └── application/
│       └── index.html         # Login form with reCAPTCHA
├── fixtures/                  # Test fixtures
│   └── email_template.json    # Initial email templates
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── setup.cfg                  # Flake8 configuration
├── fabfile.py                 # Fabric deployment tasks
└── .circleci/config.yml       # CircleCI workflow definition
```

## Django Apps & Purposes

### 1. **application** (Member Onboarding)
**Purpose**: Handles new member applications and email verification workflow.

**Key Models**:
- `MemberApplication`: Represents a potential member's application form submission
  - Fields: Personal info (name, email, birthday, phone, address)
  - Payment info: IBAN, BIC (with SEPA validation)
  - Membership type: active, active_cheerleading, or support
  - Student status: TUM, LMU, other university, apprenticeship, working
  - Verification system: unique code, email verification flag
  - Timestamps: created_at, updated_at
  - Emits verification email to applicant, notification to board members

**Key Features**:
- Email verification workflow (generates random verification code)
- Admin action to accept applications → creates Member records
- Custom template tags for form descriptions
- Tests cover application creation, verification, member conversion

**URL Routes** (via application/views.py):
- `POST /` - Login with reCAPTCHA captcha
- `GET /verify/<verification_code>/` - Email verification endpoint
- `GET /impressum/` - Impressum page
- `/logout/` - Logout redirect
- `/admin/` - Admin interface (default)

### 2. **member** (Member Registry)
**Purpose**: Manages active member records and internal tracking.

**Key Models**:
- `Member`: Active member record (created from accepted MemberApplication)
  - Inherits core fields from application (name, contact, address, IBAN, BIC)
  - SEPA tracking: sepa_date, sepa_ok, sepa_mandat (read-only property M####)
  - Position tracking: position_type (board positions for notifications)
  - Membership status: membership_type, member_since, member_exited
  - Payment tracking: paid_2018 through paid_2026 (boolean flags)
  - Reminder status: mahnungsstatus (erinnerung, mahnung_1-3)
  - Student status: Tracks university/work status
  - FK to MemberApplication (optional, read-only)

**Key Features**:
- CSV export action for admin
- LogEntry tracking in admin
- Organized admin interface with fieldsets:
  - Personal Info
  - Address
  - SEPA Information
  - Membership
  - Payments (yearly)
  - System (metadata)
- Payment history tracked per year

### 3. **email_template** (Configurable Emails)
**Purpose**: Provides system for templated, admin-editable emails.

**Key Models**:
- `EmailTemplate`: Configurable email templates with 4 types:
  1. `NOTIFY_BOARD_NEW_APPLICATION` - Board notified of new application
  2. `NOTIFY_BOARD_VERIFIED_APPLICATION` - Board notified of verified email
  3. `NOTIFY_MEMBER_TO_VERIFY_APPLICATION` - Applicant verification email
  4. `NOTIFY_MEMBER_ABOUT_MEMBERSHIP` - Member acceptance confirmation

**Key Features**:
- Templates managed via Django admin
- `send_template_mail()` helper function in helpers.py
- Supports template variable substitution (context dict)
- Fixture loads initial templates

## Key Architectural Patterns

### 1. **Admin-Driven UI**
- Core interaction happens in Django admin interface
- Minimal custom views (mostly verification and login)
- Custom admin actions for workflows (accept application, make_done, make_new)
- Customized admin templates for branding

### 2. **Workflow: Application → Verification → Membership**
1. User fills out MemberApplication form (public-facing login page)
2. Email verification sent with unique code
3. User clicks verification link
4. Admin reviews and accepts application via admin action
5. Member record automatically created from application data
6. Member acceptance email sent

### 3. **Email Notification System**
- Triggered on model saves (MemberApplication.save())
- Uses configurable templates (admin-editable)
- Context variables passed to templates
- SMTP backend configured in production

### 4. **Internationalization (i18n)**
- Django i18n enabled (USE_I18N=True)
- German language (LANGUAGE_CODE='de')
- German locale (TIME_ZONE='Europe/Berlin')
- All model verbose_names use `gettext_lazy(_('...'))`

### 5. **Environment-Specific Configuration**
- Base settings: entity_management/settings.py (DEBUG=True, test keys)
- Production: config/production.py (reads env vars, HTTPS, real keys)
- Deployment: config/deployment.py (Uberspace paths)
- Selected via DJANGO_SETTINGS_MODULE environment variable

## Configuration & Settings

### Development Settings (Default)
**File**: `entity_management/settings.py`

```python
# Core
DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = 'test-key-exposed' (SECURITY WARNING - dev only)

# Database
DATABASES = { 'default': { 'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db.sqlite3' } }

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'application',
    'member',
    'email_template',
    'django_recaptcha',
]

# Security
CSRF middleware enabled
XFrameOptions enabled
Password validators enabled

# Locale
LANGUAGE_CODE = 'de'
TIME_ZONE = 'Europe/Berlin'
USE_TZ = True

# Captcha (Test Keys)
NOCAPTCHA = True  # reCAPTCHA v2
RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'  # Google test public key
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'  # Google test private key

# Email
DEFAULT_FROM_EMAIL = 'noreply@studylife-muenchen.de'
CURRENT_DOMAIN_URL = 'https://studylife-muenchen.de'
LOGOUT_REDIRECT_URL = "/"

# Admin
STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
```

### Production Settings
**File**: `config/production.py` (inherits from base settings)

```python
DEBUG = False
ALLOWED_HOSTS = ['study.local.uberspace.de']
CSRF_TRUSTED_ORIGINS = [
    'https://www.studylife-muenchen.de',
    'https://studylife-muenchen.de',
    'https://study.uber.space'
]

# All secrets from environment variables
SECRET_KEY = os.environ['SECRET_KEY']
RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']

# HTTPS enforced
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Email (SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True
EMAIL_PORT = 587

# Admin notifications
ADMINS = [("Administrator", email) for email in os.environ['ADMINS'].split(', ')]

# Uberspace paths
STATIC_ROOT = '/home/study/html/static/'
```

### Required Environment Variables (Production)
- `SECRET_KEY`: Django secret key
- `RECAPTCHA_PRIVATE_KEY`: Google reCAPTCHA private key
- `EMAIL_HOST`: SMTP server hostname
- `EMAIL_HOST_USER`: SMTP username
- `EMAIL_HOST_PASSWORD`: SMTP password
- `ADMINS`: Comma-separated list of admin email addresses

### Flake8 Configuration
**File**: `setup.cfg`
- Max line length: 120 characters
- Excluded: .git, migrations, fabfile.py, manage.py, venv

## Build & Development Commands

### Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create database and run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial email templates
python manage.py loaddata fixtures/email_template.json
```

### Development
```bash
# Run development server
python manage.py runserver

# Run development server on specific port
python manage.py runserver 0.0.0.0:8000
```

### Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test application
python manage.py test member

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report --omit='venv/*'
coverage xml --omit='venv/*'
```

### Database Migrations
```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Migrate specific app
python manage.py migrate application
python manage.py migrate member

# Show migration plan
python manage.py showmigrations

# Revert migration
python manage.py migrate application 0001  # migrate to specific point
```

### Code Quality
```bash
# Run linting (flake8)
flake8 ./

# Flake8 with specific config
flake8 ./ --config setup.cfg
```

### Static Files
```bash
# Collect static files (development)
python manage.py collectstatic

# Collect static files (production, no input)
python manage.py collectstatic --noinput --settings=config.deployment
```

### Admin Interface
```bash
# Access admin
# Development: http://localhost:8000/admin/
# Requires superuser login

# Create admin user
python manage.py createsuperuser
```

### Deployment (via Fabric)
```bash
# Configure Staging environment
fab staging <command>

# Available commands
fab staging git_pull          # Pull latest from master
fab staging install_requirements  # Install pip dependencies
fab staging deploy            # Collect static files and restart
fab staging migrate           # Run migrations
fab staging restart_server    # Restart supervisor process

# Full deployment sequence
fab staging git_pull
fab staging install_requirements
fab staging migrate
fab staging deploy
fab staging restart_server
```

## CI/CD Pipeline

### CircleCI Configuration
**File**: `.circleci/config.yml`

**Workflow**:
1. **Install Dependencies**: Python 3.8 venv, install requirements
2. **Cache Dependencies**: Cache venv for faster builds
3. **Lint**: Run `flake8 ./` 
4. **Test**: Run `coverage run --source='.' manage.py test`
5. **Coverage Report**: Generate coverage xml
6. **Deploy** (only on master branch):
   - `fab staging git_pull`
   - `fab staging install_requirements`
   - `fab staging deploy`
   - `fab staging migrate`
   - `fab staging restart_server`

**Code Climate Integration**: Test coverage reported to CodeClimate
- Coverage ID: 46a5ed85992bc4ad14ebe9694c1f4f9beca2051b2afbaaa2a5ece130a5642000

## Testing

### Test Coverage
- **Primary Test Suite**: `application/tests.py`
- **Framework**: Django TestCase with fixtures
- **Key Test Cases**:
  - Application creation and email notifications (2 emails: to applicant + board)
  - Member creation from application (data transfer, payment fields initialization)
  - Email verification workflow (valid code, already verified, invalid code)
  - Admin action acceptance
  - Application form rendering with custom descriptions

**Test Fixtures**:
- `fixtures/email_template.json`: Initial email template data for tests

**Running Tests**:
```bash
# All tests
python manage.py test

# With coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

## Important Files & Quick Reference

### Core Files
- `manage.py`: Django CLI entry point
- `entity_management/settings.py`: Base configuration
- `config/production.py`: Production settings
- `entity_management/urls.py`: Main URL router
- `entity_management/wsgi.py`: WSGI application

### Models & Business Logic
- `application/models.py`: MemberApplication (1900+ lines)
- `member/models.py`: Member model
- `email_template/models.py`: EmailTemplate configurations
- `application/admin.py`: MemberApplication admin + creation logic
- `member/admin.py`: Member admin + CSV export

### Views & Forms
- `application/views.py`: Login, verification, impressum views
- `application/forms.py`: CaptchaLoginForm
- `email_template/helpers.py`: send_template_mail()

### Templates
- `templates/application/index.html`: Login form with reCAPTCHA
- `templates/admin/base.html`: Custom admin template
- `templates/admin/change_form.html`: Custom form layout with fieldsets

### Database & Migrations
- `application/migrations/`: 20+ migrations for MemberApplication
- `member/migrations/`: 30+ migrations for Member
- `email_template/migrations/`: EmailTemplate migrations

### Configuration & Deployment
- `setup.cfg`: Flake8 rules
- `fabfile.py`: Deployment tasks
- `.circleci/config.yml`: CI/CD pipeline
- `requirements.txt`: Python dependencies
- `fixtures/email_template.json`: Initial email template data

### Documentation
- `README.md`: Basic project info and environment variables
- This file (CLAUDE.md)

## Notable Recent Changes

### Recent Commits (from git log)
1. **Fix flake8 E501 line length error in member admin** - Resolved linting issue
2. **Reorganize member admin form with fieldsets** - Improved admin UX with fieldsets
3. **Add SEPA-Mandat, student status, and Mahnungsstatus fields** - Enhanced member tracking
4. **Add new payment fields (paid_2024-2026)** - Extended payment history tracking

### Recent Features
- SEPA mandate tracking and validation
- Student status field (TUM, LMU, other)
- Reminder/dunning status (Mahnungsstatus)
- Multi-year payment tracking (2018-2026)
- Fieldset organization in admin interface

## Security Considerations

### Warnings in Development Settings
- DEBUG = True (will expose sensitive info in errors)
- SECRET_KEY exposed in repository (dev only)
- Test reCAPTCHA keys used (not real validation)

### Production Security
- DEBUG = False enforced
- SECRET_KEY read from environment
- Real reCAPTCHA keys read from environment
- HTTPS enforced (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
- CSRF protection enabled with trusted origins list

### Authentication
- Uses Django auth backend
- "visitor" user for public application form submission
- Superuser required for admin access
- Email verification for new applications

## Common Development Tasks

### Add a New Field to Member Model
1. Add field to `member/models.py`
2. Run `python manage.py makemigrations member`
3. Review migration in `member/migrations/`
4. Run `python manage.py migrate member`
5. Update `member/admin.py` fieldsets if needed
6. Add to tests if applicable

### Create a New Email Template
1. Add template type constant to `EmailTemplate` model
2. Add to TEMPLATE_TYPE_CHOICES
3. Create migration: `python manage.py makemigrations email_template`
4. In admin, create new EmailTemplate record
5. Use in code: `send_template_mail(EmailTemplate.NEW_TYPE, recipients, context)`

### Export Member Data
- Use admin action "Ausgewählte Mitglieder als csv exportieren" (CSV export)
- Exports: Gender, name, email, birthday, phone, address, IBAN, BIC, membership type, member_since

### Debug Email Sending
- In development, emails printed to console (console backend default)
- Or use: `python manage.py shell` to test `send_template_mail()` directly

## Useful Django Shortcuts

```bash
# Enter Django shell
python manage.py shell
>>> from member.models import Member
>>> Member.objects.all().count()

# Create test data
>>> from application.models import MemberApplication
>>> from django.utils import timezone
>>> app = MemberApplication.objects.create(...)

# Check migrations
python manage.py showmigrations

# Create new app (if needed)
python manage.py startapp new_app_name

# Export/import data
python manage.py dumpdata app_name > backup.json
python manage.py loaddata backup.json
```

## Troubleshooting

### Common Issues

**"Couldn't import Django"**
- Activate virtual environment: `source venv/bin/activate`
- Install requirements: `pip install -r requirements.txt`

**Database errors**
- Run migrations: `python manage.py migrate`
- Check migration status: `python manage.py showmigrations`

**Admin login not working**
- Create superuser: `python manage.py createsuperuser`
- Check user exists: `python manage.py shell` → `User.objects.all()`

**Email not sending**
- Check settings: Are you using production settings with real SMTP?
- Dev mode uses console backend (prints to stdout)
- Check EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD env vars

**reCAPTCHA errors**
- In dev, test keys are used (always pass)
- Production needs real keys from Google
- NOCAPTCHA = True for v2 (no-CAPTCHA version)

**Flake8 failures**
- Max line length is 120 characters (see setup.cfg)
- Exclude migrations: Don't edit migration files for style
- Run: `flake8 ./` to check

## Performance & Optimization

- **Database**: SQLite3 in dev, move to PostgreSQL for production if scaling
- **Static Files**: Served from `/home/study/html/static/` on production (Uberspace)
- **Email**: Async email sending could be added with Celery (not currently implemented)
- **Caching**: Django caching not configured (could improve admin performance)

## Notes for Future Developers

1. **Language**: All UI/models use German - maintain this for consistency
2. **Workflow**: Focus on application → verification → membership flow
3. **Admin-First Design**: Most features accessed through admin interface
4. **Testing**: Write tests for new features - use application/tests.py as template
5. **Email**: Always use send_template_mail() with configurable templates
6. **Migrations**: Never edit migration files after merging - create new ones
7. **Deployment**: CircleCI auto-deploys on master branch - test locally first
8. **Uberspace**: Remember max line length 120 (flake8), static file collection required
