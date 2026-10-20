# core/views.py
"""Vistas de la configuración central del ERP — W01."""
from django.shortcuts import render
from django.urls import reverse, NoReverseMatch


def _url_modulo(app, nombres=('lista', 'inicio', 'dashboard', 'index')):
    """Devuelve la URL raíz de una app probando varios nombres de ruta.

    Si ninguno existe, devuelve '#' para que la página no se caiga.
    """
    for nombre in nombres:
        try:
            return reverse(f'{app}:{nombre}')
        except NoReverseMatch:
            continue
    return '#'


def bienvenida(request):
    """Página de inicio del ERP con tarjetas de módulos.

    Context:
        modulos (list): Lista de dicts con icono, nombre, url y descripcion.

    Returns:
        HttpResponse con template bienvenida.html.
    """
    modulos = [
        {
            'nombre': 'Productos',
            'icono': '📦',
            'url': _url_modulo('productos'),
            'descripcion': 'Inventario, precios y stock',
        },
        {
            'nombre': 'Clientes',
            'icono': '👥',
            'url': _url_modulo('clientes'),
            'descripcion': 'Cartera y gestión de clientes',
        },
        {
            'nombre': 'Proveedores',
            'icono': '🏭',
            'url': _url_modulo('proveedores'),
            'descripcion': 'Red de proveedores',
        },
        {
            'nombre': 'Ventas',
            'icono': '💰',
            'url': _url_modulo('ventas'),
            'descripcion': 'Pedidos, facturas y cobros',
        },
        {
            'nombre': 'Reportes',
            'icono': '📊',
            'url': _url_modulo('reportes'),
            'descripcion': 'Dashboard y analítica',
        },
        {
            'nombre': 'Admin',
            'icono': '⚙️',
            'url': '/admin/',
            'descripcion': 'Panel de administración Django',
        },
    ]
    return render(request, 'bienvenida.html', {'modulos': modulos})