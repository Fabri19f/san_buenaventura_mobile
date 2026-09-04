import flet as ft

from components.seccion_accesos import SeccionAccesos
from components.tarjeta_acceso import TarjetaAcceso
from components.tarjeta_aviso import TarjetaAviso
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
        return SeccionAccesos(
            titulo="Gestiones de citas",
            descripcion="Todo lo necesario para organizar tu atención.",
            accesos=(
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
            ),
        ).control

    @staticmethod
    def _crear_aviso_privacidad() -> ft.Control:
        return TarjetaAviso(
            titulo="Tu información, protegida",
            descripcion=(
                "La aplicación se enfoca únicamente en la gestión de tus citas."
            ),
            icono=ft.Icons.SHIELD,
            color_icono=COLOR_PRIMARIO,
            color_titulo=COLOR_PRIMARIO_OSCURO,
            color_fondo=COLOR_PRIMARIO_SUAVE,
        ).control
