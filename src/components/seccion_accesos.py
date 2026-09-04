from collections.abc import Sequence

import flet as ft

from components.tarjeta_acceso import TarjetaAcceso
from tema import COLOR_TEXTO_PRINCIPAL, COLOR_TEXTO_SECUNDARIO


class SeccionAccesos:
    """Agrupa opciones visuales bajo un encabezado común."""

    def __init__(
        self,
        titulo: str,
        descripcion: str,
        accesos: Sequence[TarjetaAcceso],
    ) -> None:
        self._control = ft.Column(
            spacing=12,
            controls=[
                ft.Column(
                    spacing=3,
                    controls=[
                        ft.Text(
                            titulo,
                            color=COLOR_TEXTO_PRINCIPAL,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            descripcion,
                            color=COLOR_TEXTO_SECUNDARIO,
                            size=13,
                        ),
                    ],
                ),
                *[acceso.control for acceso in accesos],
            ],
        )

    @property
    def control(self) -> ft.Control:
        return self._control
