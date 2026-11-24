from collections import defaultdict
from datetime import date
from decimal import Decimal

from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.template.loader import render_to_string

from ventas.models import Pedido

ESTADO_PAGADO = "pagado"


def construir_contexto_reporte(fecha=None):
    fecha = fecha or date.today()
    fecha_txt = fecha.strftime("%d/%m/%Y")

    pedidos = Pedido.objects.filter(estado=ESTADO_PAGADO, fecha_pedido__date=fecha)

    total = pedidos.aggregate(t=Sum("total_pagado"))["t"] or Decimal("0")

    # Acumular unidades e ingreso por producto desde items_snapshot
    acumulado = defaultdict(lambda: {"unidades": 0, "ingreso": Decimal("0")})
    for pedido in pedidos:
        for item in pedido.items_snapshot or []:
            nombre = item.get("nombre", "Sin nombre")
            cantidad = int(item.get("cantidad", 0))
            precio = Decimal(str(item.get("precio", "0")))
            acumulado[nombre]["unidades"] += cantidad
            acumulado[nombre]["ingreso"] += precio * cantidad

    top = sorted(acumulado.items(), key=lambda x: x[1]["unidades"], reverse=True)[:2]

    return {
        "fecha": fecha_txt,
        "periodo": fecha_txt,
        "config": {"nombre_empresa": "Gio's Wax Cellar"},
        "total_pedidos": pedidos.count(),
        "total_facturado": f"{total:,.2f}",
        "top_productos": [
            {
                "nombre": nombre,
                "unidades": datos["unidades"],
                "ingreso": f"{datos['ingreso']:,.2f}",
            }
            for nombre, datos in top
        ],
        "url_admin": "/admin/",
    }


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