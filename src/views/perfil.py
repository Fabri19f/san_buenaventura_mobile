import flet as ft

from components.encabezado_seccion import EncabezadoSeccion
from components.seccion_accesos import SeccionAccesos
from components.tarjeta_acceso import TarjetaAcceso
from components.tarjeta_aviso import TarjetaAviso
from tema import (
    COLOR_AZUL,
    COLOR_AZUL_SUAVE,
    COLOR_BORDE,
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_OSCURO,
    COLOR_PRIMARIO_SUAVE,
    COLOR_ROJO,
    COLOR_ROJO_SUAVE,
    COLOR_SUPERFICIE,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
)


class VistaPerfil:
    """Presenta la estructura de cuenta sin asumir datos editables."""

    def __init__(self) -> None:
        self._control = ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                spacing=24,
                controls=[
                    EncabezadoSeccion(
                        titulo="Perfil",
                        descripcion="Consulta la información asociada a tu cuenta.",
                        icono=ft.Icons.ACCOUNT_CIRCLE,
                        color_icono=COLOR_AZUL,
                        color_fondo_icono=COLOR_AZUL_SUAVE,
                    ).control,
                    self._crear_identidad(),
                    self._crear_opciones_cuenta(),
                    TarjetaAviso(
                        titulo="Privacidad por diseño",
                        descripcion=(
                            "La historia clínica no forma parte de esta aplicación."
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
    def control(self) -> ft.Control:
        return self._control

    @staticmethod
    def _crear_identidad() -> ft.Control:
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
                        width=64,
                        height=64,
                        alignment=ft.Alignment.CENTER,
                        bgcolor=COLOR_PRIMARIO_SUAVE,
                        shape=ft.BoxShape.CIRCLE,
                        content=ft.Icon(
                            icon=ft.Icons.PERSON,
                            color=COLOR_PRIMARIO,
                            size=34,
                            semantics_label="Paciente",
                        ),
                    ),
                    ft.Column(
                        expand=True,
                        spacing=5,
                        controls=[
                            ft.Text(
                                "Perfil del paciente",
                                color=COLOR_TEXTO_PRINCIPAL,
                                size=18,
                                weight=ft.FontWeight.W_600,
                            ),
                            ft.Text(
                                "La información de tu cuenta aparecerá aquí.",
                                color=COLOR_TEXTO_SECUNDARIO,
                                size=13,
                            ),
                        ],
                    ),
                ],
            ),
        )

    @staticmethod
    def _crear_opciones_cuenta() -> ft.Control:
        return SeccionAccesos(
            titulo="Cuenta",
            descripcion="Opciones relacionadas con tu perfil y acceso.",
            accesos=(
                TarjetaAcceso(
                    titulo="Información personal",
                    descripcion="Consulta los datos asociados a tu cuenta.",
                    icono=ft.Icons.CONTACT_PAGE,
                    color_icono=COLOR_PRIMARIO,
                    color_fondo_icono=COLOR_PRIMARIO_SUAVE,
                ),
                TarjetaAcceso(
                    titulo="Seguridad y acceso",
                    descripcion="Administra el acceso seguro a la aplicación.",
                    icono=ft.Icons.LOCK_PERSON,
                    color_icono=COLOR_AZUL,
                    color_fondo_icono=COLOR_AZUL_SUAVE,
                ),
                TarjetaAcceso(
                    titulo="Cerrar sesión",
                    descripcion="Finaliza el acceso en este dispositivo.",
                    icono=ft.Icons.LOGOUT,
                    color_icono=COLOR_ROJO,
                    color_fondo_icono=COLOR_ROJO_SUAVE,
                ),
            ),
        ).control
