from datetime import date

from django.core.management.base import BaseCommand

from ventas.reportes import construir_contexto_reporte, enviar_reporte_ventas

DESTINATARIOS = ["kf.belmanm.2528@cbtis198.edu.mx"]


class Command(BaseCommand):
    help = "Envía el reporte de pedidos pagados del día"

    def add_arguments(self, parser):
        parser.add_argument("--fecha", help="Fecha AAAA-MM-DD. Por defecto, hoy.")

    def handle(self, *args, **opts):
        fecha = date.fromisoformat(opts["fecha"]) if opts["fecha"] else None
        contexto = construir_contexto_reporte(fecha)
        enviar_reporte_ventas(DESTINATARIOS, contexto)
        self.stdout.write(
            self.style.SUCCESS(f"Reporte enviado: {contexto['total_pedidos']} pedidos pagados")
        )