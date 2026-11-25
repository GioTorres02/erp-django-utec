# catalogo/webhook_views.py
"""Endpoint de webhook para recibir eventos de Stripe — W15/W16/W17.

Verificación de seguridad:
    Stripe firma cada evento con STRIPE_WEBHOOK_SECRET.
    stripe.Webhook.construct_event() verifica la firma.
    Si la firma es inválida → 400 (Stripe no reintenta).
    Si la firma es válida → procesar el evento → 200.

Eventos manejados:
    payment_intent.succeeded      → Pedido.estado = 'pagado'
                                    Descontar stock
                                    Encolar correo de confirmación y reporte del día
    payment_intent.payment_failed → Pedido.estado = 'cancelado'
"""
import logging

import stripe
from django.conf import settings
from django.db.models import F
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from productos.models import Producto
from ventas.models import Pedido
from ventas.tasks import enviar_confirmacion_pedido, reporte_ventas_diario

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def stripe_webhook(request) -> HttpResponse:
    """Recibe y procesa eventos de Stripe.

    Returns:
        200 si el evento fue procesado (o ignorado),
        400 si la firma o el payload son inválidos.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    # ── 1. Verificar firma ─────────────────────────────────────────────
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        logger.warning('Webhook: payload inválido recibido.')
        return HttpResponse('Payload inválido.', status=400)
    except stripe.error.SignatureVerificationError:
        logger.warning('Webhook: firma inválida — posible ataque.')
        return HttpResponse('Firma inválida.', status=400)

    # stripe >= 15 devuelve StripeObject, que ya no tiene .get()
    if hasattr(event, 'to_dict'):
        event = event.to_dict()

    # ── 2. Despachar por tipo de evento ────────────────────────────────
    tipo = event['type']
    logger.info(f'Webhook recibido: {tipo}')

    if tipo == 'payment_intent.succeeded':
        _manejar_pago_exitoso(event['data']['object'])

    elif tipo == 'payment_intent.payment_failed':
        _manejar_pago_fallido(event['data']['object'])

    else:
        logger.debug(f'Evento ignorado: {tipo}')

    # Siempre 200 para eventos que no necesitamos (Stripe reintenta en 4xx/5xx)
    return HttpResponse(status=200)


# ── HANDLERS INTERNOS ──────────────────────────────────────────────────

def _manejar_pago_exitoso(payment_intent: dict) -> None:
    """Marca el pedido como pagado, descuenta stock y encola los correos.

    El UPDATE condicional es atómico: solo una entrega del webhook logra
    pasar el pedido de no pagado a pagado, así que los correos y el stock
    se procesan una sola vez aunque Stripe reenvíe el evento.
    """
    pedido_id = _extraer_pedido_id(payment_intent)
    if pedido_id is None:
        return

    try:
        pedido = Pedido.objects.get(pk=pedido_id)
    except Pedido.DoesNotExist:
        logger.error(f'Webhook: Pedido {pedido_id} no encontrado en BD.')
        return

    actualizados = (
        Pedido.objects
        .filter(pk=pedido.pk)
        .exclude(estado='pagado')
        .update(estado='pagado')
    )

    if actualizados != 1:
        logger.info(
            f'Pedido {pedido.numero_pedido} ya estaba pagado — '
            f'idempotente, sin cambios.'
        )
        return

    pedido.estado = 'pagado'
    logger.info(f'Pedido {pedido.numero_pedido} actualizado a "pagado".')

    _descontar_stock(pedido)

    # La vista no usa transacción atómica, así que el update ya quedó
    # guardado y el reporte del día incluye esta compra.
    _encolar_correos(pedido.pk, pedido.numero_pedido)


def _encolar_correos(pedido_pk: int, numero_pedido: str) -> None:
    """Encola el correo de confirmación al cliente y el reporte del día.

    Si Redis no responde, el pago ya quedó registrado: se deja constancia
    en el log y se responde 200 a Stripe igualmente.
    """
    try:
        enviar_confirmacion_pedido.delay(pedido_pk)
    except Exception:
        logger.exception(
            f'Webhook: no se pudo encolar la confirmación del pedido '
            f'{numero_pedido} (¿Redis disponible?).'
        )

    try:
        reporte_ventas_diario.delay()
    except Exception:
        logger.exception(
            f'Webhook: no se pudo encolar el reporte de ventas '
            f'tras el pedido {numero_pedido}.'
        )


def _manejar_pago_fallido(payment_intent: dict) -> None:
    """Marca el pedido como 'cancelado' si sigue pendiente."""
    pedido_id = _extraer_pedido_id(payment_intent)
    if pedido_id is None:
        return

    try:
        pedido = Pedido.objects.get(pk=pedido_id)
    except Pedido.DoesNotExist:
        logger.error(f'Webhook: Pedido {pedido_id} no encontrado.')
        return

    if pedido.estado == 'pendiente':
        pedido.estado = 'cancelado'
        pedido.save(update_fields=['estado'])
        logger.info(f'Pedido {pedido.numero_pedido} cancelado por pago fallido.')


def _extraer_pedido_id(payment_intent: dict) -> int | None:
    """Extrae el pedido_id del metadata del PaymentIntent."""
    metadata = payment_intent.get('metadata', {})
    pedido_id = metadata.get('pedido_id')

    if not pedido_id:
        logger.warning(
            f'Webhook: PaymentIntent sin pedido_id en metadata. '
            f'ID de PaymentIntent: {payment_intent.get("id")}'
        )
        return None

    try:
        return int(pedido_id)
    except (ValueError, TypeError):
        logger.error(f'Webhook: pedido_id inválido: {pedido_id!r}')
        return None


def _descontar_stock(pedido: 'Pedido') -> None:
    """Descuenta el stock de los productos del pedido con F() (atómico)."""
    for item in pedido.items_snapshot or []:
        producto_id = item.get('producto_id')
        cantidad = int(item.get('cantidad', 0))

        if not producto_id or cantidad <= 0:
            continue

        filas_actualizadas = Producto.objects.filter(
            pk=producto_id,
            stock__gte=cantidad,
        ).update(stock=F('stock') - cantidad)

        if filas_actualizadas:
            logger.info(f'Stock decrementado: Producto {producto_id} - {cantidad} unidades.')
        else:
            logger.warning(
                f'Producto {producto_id}: stock insuficiente para '
                f'decrementar {cantidad} unidades.'
            )