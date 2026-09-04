from collections.abc import Callable

import flet as ft

from tema import (
    COLOR_BORDE,
    COLOR_SUPERFICIE,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
)


class TarjetaAcceso:
    """Presenta una gestión y delega opcionalmente su selección."""

    def __init__(
        self,
        titulo: str,
        descripcion: str,
        icono: ft.IconData,
        color_icono: str,
        color_fondo_icono: str,
        al_seleccionar: Callable[[], None] | None = None,
    ) -> None:
        self._al_seleccionar = al_seleccionar
        controles: list[ft.Control] = [
            ft.Container(
                width=46,
                height=46,
                alignment=ft.Alignment.CENTER,
                bgcolor=color_fondo_icono,
                border_radius=14,
                content=ft.Icon(
                    icon=icono,
                    color=color_icono,
                    size=24,
                    semantics_label=f"Icono de {titulo.lower()}",
                ),
            ),
            ft.Column(
                expand=True,
                spacing=3,
                controls=[
                    ft.Text(
                        titulo,
                        color=COLOR_TEXTO_PRINCIPAL,
                        size=15,
                        weight=ft.FontWeight.W_600,
                    ),
                    ft.Text(
                        descripcion,
                        color=COLOR_TEXTO_SECUNDARIO,
                        size=12,
                    ),
                ],
            ),
        ]
        if al_seleccionar is not None:
            controles.append(
                ft.Icon(
                    icon=ft.Icons.CHEVRON_RIGHT,
                    color=COLOR_TEXTO_SECUNDARIO,
                    size=22,
                    semantics_label="Abrir",
                )
            )

        self._control = ft.Container(
            bgcolor=COLOR_SUPERFICIE,
            border=ft.Border.all(width=1, color=COLOR_BORDE),
            border_radius=18,
            padding=16,
            ink=al_seleccionar is not None,
            on_click=(
                self._manejar_seleccion if al_seleccionar is not None else None
            ),
            content=ft.Row(
                spacing=14,
                controls=controles,
            ),
        )

    @property
    def control(self) -> ft.Control:
        return self._control

    def _manejar_seleccion(self, _: ft.Event[ft.Container]) -> None:
        if self._al_seleccionar is not None:
            self._al_seleccionar()
