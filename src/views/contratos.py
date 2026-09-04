from typing import Protocol

import flet as ft

from app.rutas import RutaSecundaria


class VistaPrincipal(Protocol):
    @property
    def control(self) -> ft.Control:
        """Control raíz que representa la vista."""
        ...


class PantallaSecundaria(Protocol):
    @property
    def ruta(self) -> RutaSecundaria:
        """Ruta que identifica la pantalla dentro de la pila."""
        ...

    @property
    def titulo(self) -> str:
        """Título mostrado por la barra superior de la pantalla."""
        ...

    @property
    def control(self) -> ft.Control:
        """Contenido de la pantalla secundaria."""
        ...
