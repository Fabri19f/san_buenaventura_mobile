import flet as ft

from components.tarjeta_acceso import TarjetaAcceso
from tema import (
    COLOR_AZUL,
    COLOR_AZUL_SUAVE,
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_OSCURO,
    COLOR_PRIMARIO_SUAVE,
    COLOR_ROJO,
    COLOR_ROJO_SUAVE,
    COLOR_SUPERFICIE,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
)


class VistaInicio:
    """Presenta el resumen inicial del paciente sin datos simulados."""

    def __init__(self) -> None:
        self._control = ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                spacing=24,
                controls=[
                    self._crear_cabecera(),
                    self._crear_resumen_proxima_cita(),
                    self._crear_gestiones(),
                    self._crear_aviso_privacidad(),
                ],
            ),
        )

    @property
    def control(self) -> ft.Control:
        return self._control

    @staticmethod
    def _crear_cabecera() -> ft.Control:
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    expand=True,
                    spacing=4,
                    controls=[
                        ft.Text(
                            "CLÍNICA SAN BUENAVENTURA",
                            color=COLOR_PRIMARIO,
                            size=11,
                            weight=ft.FontWeight.W_600,
                        ),
                        ft.Text(
                            "Bienvenido",
                            color=COLOR_TEXTO_PRINCIPAL,
                            size=30,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "Gestiona tus citas de forma simple y segura.",
                            color=COLOR_TEXTO_SECUNDARIO,
                            size=14,
                        ),
                    ],
                ),
                ft.Container(
                    width=54,
                    height=54,
                    alignment=ft.Alignment.CENTER,
                    bgcolor=COLOR_PRIMARIO_SUAVE,
                    shape=ft.BoxShape.CIRCLE,
                    content=ft.Icon(
                        icon=ft.Icons.HEALTH_AND_SAFETY,
                        color=COLOR_PRIMARIO,
                        size=28,
                        semantics_label="Salud y seguridad",
                    ),
                ),
            ],
        )

    @staticmethod
    def _crear_resumen_proxima_cita() -> ft.Control:
        return ft.Container(
            bgcolor=COLOR_PRIMARIO,
            border_radius=24,
            padding=20,
            content=ft.Row(
                spacing=16,
                controls=[
                    ft.Column(
                        expand=True,
                        spacing=8,
                        controls=[
                            ft.Text(
                                "PRÓXIMA CITA",
                                color=COLOR_PRIMARIO_SUAVE,
                                size=11,
                                weight=ft.FontWeight.W_600,
                            ),
                            ft.Text(
                                "Tu próxima cita aparecerá aquí",
                                color=COLOR_SUPERFICIE,
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Podrás consultar la fecha, la hora y su estado.",
                                color=COLOR_PRIMARIO_SUAVE,
                                size=13,
                            ),
                        ],
                    ),
                    ft.Container(
                        width=54,
                        height=54,
                        alignment=ft.Alignment.CENTER,
                        bgcolor=COLOR_PRIMARIO_OSCURO,
                        shape=ft.BoxShape.CIRCLE,
                        content=ft.Icon(
                            icon=ft.Icons.CALENDAR_MONTH,
                            color=COLOR_SUPERFICIE,
                            size=27,
                            semantics_label="Próxima cita",
                        ),
                    ),
                ],
            ),
        )

    @staticmethod
    def _crear_gestiones() -> ft.Control:
        accesos = (
            TarjetaAcceso(
                titulo="Ver mis citas",
                descripcion="Consulta tus citas programadas.",
                icono=ft.Icons.EVENT,
                color_icono=COLOR_AZUL,
                color_fondo_icono=COLOR_AZUL_SUAVE,
            ),
            TarjetaAcceso(
                titulo="Solicitar una cita",
                descripcion="Inicia una nueva solicitud de atención.",
                icono=ft.Icons.MORE_TIME,
                color_icono=COLOR_PRIMARIO,
                color_fondo_icono=COLOR_PRIMARIO_SUAVE,
            ),
            TarjetaAcceso(
                titulo="Cancelar una cita",
                descripcion="Gestiona una cita que ya fue programada.",
                icono=ft.Icons.EVENT_BUSY,
                color_icono=COLOR_ROJO,
                color_fondo_icono=COLOR_ROJO_SUAVE,
            ),
        )

        return ft.Column(
            spacing=12,
            controls=[
                ft.Column(
                    spacing=3,
                    controls=[
                        ft.Text(
                            "Gestiones de citas",
                            color=COLOR_TEXTO_PRINCIPAL,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "Todo lo necesario para organizar tu atención.",
                            color=COLOR_TEXTO_SECUNDARIO,
                            size=13,
                        ),
                    ],
                ),
                *(acceso.control for acceso in accesos),
            ],
        )

    @staticmethod
    def _crear_aviso_privacidad() -> ft.Control:
        return ft.Container(
            bgcolor=COLOR_PRIMARIO_SUAVE,
            border_radius=18,
            padding=16,
            content=ft.Row(
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(
                        icon=ft.Icons.SHIELD,
                        color=COLOR_PRIMARIO,
                        size=24,
                        semantics_label="Protección de información",
                    ),
                    ft.Column(
                        expand=True,
                        spacing=3,
                        controls=[
                            ft.Text(
                                "Tu información, protegida",
                                color=COLOR_PRIMARIO_OSCURO,
                                size=14,
                                weight=ft.FontWeight.W_600,
                            ),
                            ft.Text(
                                "La aplicación se enfoca únicamente en la gestión "
                                "de tus citas.",
                                color=COLOR_TEXTO_SECUNDARIO,
                                size=12,
                            ),
                        ],
                    ),
                ],
            ),
        )
