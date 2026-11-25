import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count, Sum
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from ventas.models import DetalleVenta, Venta

logger = logging.getLogger(__name__)


def enviar_reporte_ventas():
    """Envía el reporte de ventas pagadas del día a SALES_REPORT_EMAIL."""
    hoy = timezone.localdate()
    pagadas = Venta.objects.filter(fecha__date=hoy, estado="pagado")  # ajusta campos

    totales = pagadas.aggregate(total=Sum("total"), pedidos=Count("id"))

    top = (
        DetalleVenta.objects.filter(venta__in=pagadas)
        .values("producto__nombre")
        .annotate(unidades=Sum("cantidad"), ingreso=Sum("subtotal"))
        .order_by("-unidades")[:2]
    )

    contexto = {
        "fecha": timezone.localtime().strftime("%d/%m/%Y %H:%M"),
        "config": {"nombre_empresa": "Gio's Wax Cellar", "rfc": ""},
        "total_pedidos": totales["pedidos"] or 0,
        "total_facturado": totales["total"] or 0,
        "top_productos": [
            {"nombre": t["producto__nombre"], "unidades": t["unidades"], "ingreso": t["ingreso"]}
            for t in top
        ],
        "url_admin": settings.SITE_URL + reverse("admin:index"),
    }

    html = render_to_string("emails/reporte_ventas.html", contexto)
    texto = render_to_string("emails/reporte_ventas.txt", contexto)

    msg = EmailMultiAlternatives(
        subject=f"📊 Reporte de ventas — {timezone.localtime():%d/%m/%Y %H:%M}",
        body=texto,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.SALES_REPORT_EMAIL],
    )
    msg.attach_alternative(html, "text/html")
    msg.send(fail_silently=False)
    logger.info("Reporte de ventas enviado: %s pedidos", contexto["total_pedidos"])