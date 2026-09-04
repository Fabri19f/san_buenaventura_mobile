import flet as ft

from tema import (
    COLOR_BORDE,
    COLOR_SUPERFICIE,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
)


class TarjetaAcceso:
    """Presenta una gestión disponible sin implementar todavía su acción."""

    def __init__(
        self,
        titulo: str,
        descripcion: str,
        icono: ft.IconData,
        color_icono: str,
        color_fondo_icono: str,
    ) -> None:
        self._control = ft.Container(
            bgcolor=COLOR_SUPERFICIE,
            border=ft.Border.all(width=1, color=COLOR_BORDE),
            border_radius=18,
            padding=16,
            content=ft.Row(
                spacing=14,
                controls=[
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
                ],
            ),
        )

    @property
    def control(self) -> ft.Control:
        return self._control
