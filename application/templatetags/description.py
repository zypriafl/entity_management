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
    "akzeptiere die aktuelle Beitragsordnung. <br> Die Beitragshöhe für aktive Mitglieder beträgt "
    "<b>12</b> EUR jährlich. Mitglieder die zusätzlich in der Abteilung „Cheerleading“ aktiv sind, "
    "müssen insgesamt einen Betrag von 52 EUR jährlich entrichten.<br><br> Hiermit ermächtige ich den "
    "Studylife München e.V., Kreittmayrstr. 1, 80335 München als Zahlungsempfängerin die fälligen Zahlungen "
    "von meinem oben genannten Konto mittels Lastschrift einzuziehen. Zugleich weise ich mein Kreditinstitut "
    "(identifizierbar durch die angegebene BIC) an, die vom Studylife München e.V. auf mein Konto gezogenen "
    "Lastschriften einzulösen.<br><br> Hinweis: Ich kann innerhalb von acht Wochen, beginnend mit dem Belastungsdatum, "
    "die Erstattung des belasteten Betrages verlangen. Es gelten dabei die mit meinem Kreditinstitut vereinbarten "
    "Bedingungen. Die Gläubiger-ID des Studylife München e.V. ist DE65ZZZ00002669888. Die Mandatsreferenznummer "
    "wird separat mitgeteilt. Um den Mitgliedsantrag abzuschicken, klicke auf SICHERN.<br>"
    "Wir senden dir einen Link per E-Mail, um deine E-Mail Addresse zu bestätigen.")


@register.simple_tag
def top_description():
    """Top Description"""
    return mark_safe(TOP_DESCRIPTION)


@register.simple_tag
def bottom_description():
    """Bottom Description"""
    return mark_safe(BOTTOM_DESCRIPTION)
