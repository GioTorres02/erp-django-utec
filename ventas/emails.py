from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone


def enviar_notificacion_venta(venta):
    items = venta.detalles.select_related("producto").all()  # ajusta related_name

    html = render_to_string("emails/venta_nueva.html", {
        "venta": venta,
        "items": items,
        "total": venta.total,
        "fecha": timezone.localtime().strftime("%d/%m/%Y %H:%M"),
    })

    msg = EmailMultiAlternatives(
        subject=f"🎵 Nueva venta #{venta.id} — Gio's Wax Cellar",
        body=f"Nueva venta #{venta.id} por ${venta.total}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.SALES_REPORT_EMAIL],
    )
    msg.attach_alternative(html, "text/html")
    msg.send(fail_silently=False)