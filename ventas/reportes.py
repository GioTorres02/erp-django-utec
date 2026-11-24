from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def enviar_reporte_ventas(destinatarios, contexto):
    asunto = f"Reporte de ventas – {contexto['periodo']}"

    html_content = render_to_string("emails/reporte_ventas.html", contexto)
    text_content = render_to_string("emails/reporte_ventas.txt", contexto)

    msg = EmailMultiAlternatives(
        subject=asunto,
        body=text_content,
        to=destinatarios,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()