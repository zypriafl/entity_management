from contextlib import contextmanager as _contextmanager

from fabric.api import *

env.project_name = 'studylife'
env.project_folder = 'entity_management'


def staging():
    env.hosts = ['www.studylife-muenchen.de']
    env.user = 'study'
    env.src_path = '/home/study/%(project_folder)s' % env


@_contextmanager
def virtualenv():
    require('hosts', provided_by=[staging])
    with cd(env.src_path):
        yield


def deploy():
    """
    Pulls data from git, collects static files and restarts supervisor
    """
    require('hosts', provided_by=[staging])
    with virtualenv():
        run('python3 manage.py collectstatic --noinput --settings=config.deployment')


def restart_server():
    """
    restarts supervisor
    """
    run("supervisorctl restart %(project_name)s" % env)


def install_requirements():
    """
    Install the required packages from the requirements file using pip
    """
    run('whoami')
    require('hosts', provided_by=[staging])
    with virtualenv():
        run('pip3 install -r requirements.txt --user', pty=True)


def migrate():
    require('hosts', provided_by=[staging])
    with virtualenv():
        run('python3 manage.py migrate --noinput --settings=config.deployment')


def git_pull():
    """run a git pull"""
    require('hosts', provided_by=[staging])
    with virtualenv():
        run('git reset --hard')
        run('git pull origin master')
