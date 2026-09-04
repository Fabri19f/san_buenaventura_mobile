import flet as ft

from app.rutas import RutaSecundaria
from components.tarjeta_aviso import TarjetaAviso
from tema import (
    COLOR_AZUL,
    COLOR_AZUL_SUAVE,
    COLOR_BORDE,
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_OSCURO,
    COLOR_PRIMARIO_SUAVE,
    COLOR_SUPERFICIE,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
)


class PantallaInformacionPersonal:
    """Estructura la información de cuenta sin definir campos editables."""

    def __init__(self) -> None:
        self._control = ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                spacing=20,
                controls=[
                    self._crear_resumen(),
                    ft.Text(
                        "Información de la cuenta",
                        color=COLOR_TEXTO_PRINCIPAL,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                    self._crear_bloque(
                        titulo="Identificación",
                        descripcion=(
                            "Los datos de identificación asociados a tu cuenta "
                            "aparecerán aquí."
                        ),
                        icono=ft.Icons.CONTACT_PAGE,
                        color_icono=COLOR_PRIMARIO,
                        color_fondo_icono=COLOR_PRIMARIO_SUAVE,
                    ),
                    self._crear_bloque(
                        titulo="Contacto",
                        descripcion=(
                            "La información de contacto estará disponible en "
                            "esta sección."
                        ),
                        icono=ft.Icons.CONTACT_MAIL,
                        color_icono=COLOR_AZUL,
                        color_fondo_icono=COLOR_AZUL_SUAVE,
                    ),
                    TarjetaAviso(
                        titulo="Datos protegidos",
                        descripcion=(
                            "La posibilidad de editar información se definirá "
                            "antes de habilitar cambios."
                        ),
                        icono=ft.Icons.PRIVACY_TIP,
                        color_icono=COLOR_PRIMARIO,
                        color_titulo=COLOR_PRIMARIO_OSCURO,
                        color_fondo=COLOR_PRIMARIO_SUAVE,
                    ).control,
                ],
            ),
        )

    @property
    def ruta(self) -> RutaSecundaria:
        return RutaSecundaria.INFORMACION_PERSONAL

    @property
    def titulo(self) -> str:
        return "Información personal"

    @property
    def control(self) -> ft.Control:
        return self._control

    @staticmethod
    def _crear_resumen() -> ft.Control:
        return ft.Container(
            bgcolor=COLOR_SUPERFICIE,
            border=ft.Border.all(width=1, color=COLOR_BORDE),
            border_radius=22,
            padding=20,
            content=ft.Row(
                spacing=16,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=58,
                        height=58,
                        alignment=ft.Alignment.CENTER,
                        bgcolor=COLOR_PRIMARIO_SUAVE,
                        shape=ft.BoxShape.CIRCLE,
                        content=ft.Icon(
                            icon=ft.Icons.PERSON,
                            color=COLOR_PRIMARIO,
                            size=31,
                            semantics_label="Paciente",
                        ),
                    ),
                    ft.Column(
                        expand=True,
                        spacing=4,
                        controls=[
                            ft.Text(
                                "Datos del paciente",
                                color=COLOR_TEXTO_PRINCIPAL,
                                size=18,
                                weight=ft.FontWeight.W_600,
                            ),
                            ft.Text(
                                "Solo se mostrarán datos de tu propia cuenta.",
                                color=COLOR_TEXTO_SECUNDARIO,
                                size=13,
                            ),
                        ],
                    ),
                ],
            ),
        )

    @staticmethod
    def _crear_bloque(
        titulo: str,
        descripcion: str,
        icono: ft.IconData,
        color_icono: str,
        color_fondo_icono: str,
    ) -> ft.Control:
        return ft.Container(
            bgcolor=COLOR_SUPERFICIE,
            border=ft.Border.all(width=1, color=COLOR_BORDE),
            border_radius=18,
            padding=16,
            content=ft.Row(
                spacing=14,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
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
                            semantics_label=titulo,
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
