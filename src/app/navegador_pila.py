from typing import Protocol

import flet as ft

from app.navegacion import DestinoPrincipal
from app.rutas import RutaSecundaria, ruta_principal


class NavegadorAplicacion(Protocol):
    def ir_a_destino(self, destino: DestinoPrincipal) -> None:
        """Selecciona una pestaña dentro de la vista raíz persistente."""
        ...

    def abrir(self, ruta: RutaSecundaria) -> None:
        """Apila una pantalla secundaria conservando la vista de origen."""
        ...


class NavegadorPila:
    """Adapta la navegación semántica a las rutas de Flet."""

    def __init__(self, page: ft.Page) -> None:
        self._page = page

    def ir_a_destino(self, destino: DestinoPrincipal) -> None:
        self._page.navigate(ruta_principal(destino))

    def abrir(self, ruta: RutaSecundaria) -> None:
        self._page.navigate(ruta.value)
