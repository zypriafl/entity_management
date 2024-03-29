from django import template
from django.utils.safestring import mark_safe

register = template.Library()

TOP_DESCRIPTION = (
    '<h2>Wir freuen uns über dein Interesse Mitglied im Studylife München e.V. zu werden. '
    'Bitte fülle dazu den Antrag aus und klicke anschließend auf sichern. '
    'Wenn du Teil unseres Cheerleading Teams bist, gib das bitte bei der Art der Mitgliedschaft an, '
    'du wirst dann automatisch auch Mitglied der Cheerleading Abteilung.</h2>')

BOTTOM_DESCRIPTION = (
    "Ich möchte zum nächstmöglichen Zeitpunkt Mitglied im Studylife München e.V. werden und "
    "akzeptiere die aktuelle Beitragsordnung.<br> Die Beitragshöhe für aktive Mitglieder beträgt "
    "<b>12 EUR</b> jährlich. Mitglieder die zusätzlich in der Abteilung „Cheerleading“ aktiv sind, "
    "müssen insgesamt einen Betrag von <b>48 EUR</b> jährlich entrichten. Der Beitrag wird jährlich "
    "im Vorraus vom Mitglied gezahlt.<br><br> Um den Mitgliedsantrag abzuschicken klicke auf SICHERN."
    "<br><br>  Wir senden dir einen Link per E-Mail, um deine E-Mail Addresse zu bestätigen.")


@register.simple_tag
def top_description():
    """Top Description"""
    return mark_safe(TOP_DESCRIPTION)


@register.simple_tag
def bottom_description():
    """Bottom Description"""
    return mark_safe(BOTTOM_DESCRIPTION)
