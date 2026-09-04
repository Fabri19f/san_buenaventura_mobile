import flet as ft

from tema import COLOR_TEXTO_PRINCIPAL, COLOR_TEXTO_SECUNDARIO


class EncabezadoSeccion:
    """Mantiene una jerarquía visual común en las vistas principales."""

    def __init__(
        self,
        titulo: str,
        descripcion: str,
        icono: ft.IconData,
        color_icono: str,
        color_fondo_icono: str,
    ) -> None:
        self._control = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    expand=True,
                    spacing=4,
                    controls=[
                        ft.Text(
                            titulo,
                            color=COLOR_TEXTO_PRINCIPAL,
                            size=30,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            descripcion,
                            color=COLOR_TEXTO_SECUNDARIO,
                            size=14,
                        ),
                    ],
                ),
                ft.Container(
                    width=54,
                    height=54,
                    alignment=ft.Alignment.CENTER,
                    bgcolor=color_fondo_icono,
                    shape=ft.BoxShape.CIRCLE,
                    content=ft.Icon(
                        icon=icono,
                        color=color_icono,
                        size=28,
                        semantics_label=titulo,
                    ),
                ),
            ],
        )

    @property
    def control(self) -> ft.Control:
        return self._control
