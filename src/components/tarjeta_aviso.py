import flet as ft

from tema import COLOR_TEXTO_SECUNDARIO


class TarjetaAviso:
    """Presenta información contextual sin convertirla en una acción."""

    def __init__(
        self,
        titulo: str,
        descripcion: str,
        icono: ft.IconData,
        color_icono: str,
        color_titulo: str,
        color_fondo: str,
    ) -> None:
        self._control = ft.Container(
            bgcolor=color_fondo,
            border_radius=18,
            padding=16,
            content=ft.Row(
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(
                        icon=icono,
                        color=color_icono,
                        size=24,
                        semantics_label=titulo,
                    ),
                    ft.Column(
                        expand=True,
                        spacing=3,
                        controls=[
                            ft.Text(
                                titulo,
                                color=color_titulo,
                                size=14,
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
