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


class PantallaSolicitarCita:
    """Describe el flujo de solicitud sin asumir datos ni reglas del backend."""

    def __init__(self) -> None:
        self._control = ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                spacing=24,
                controls=[
                    self._crear_presentacion(),
                    self._crear_pasos(),
                    TarjetaAviso(
                        titulo="Disponibilidad validada",
                        descripcion=(
                            "Las fechas y horarios reales serán proporcionados "
                            "y confirmados por la clínica."
                        ),
                        icono=ft.Icons.FACT_CHECK,
                        color_icono=COLOR_AZUL,
                        color_titulo=COLOR_TEXTO_PRINCIPAL,
                        color_fondo=COLOR_AZUL_SUAVE,
                    ).control,
                ],
            ),
        )

    @property
    def ruta(self) -> RutaSecundaria:
        return RutaSecundaria.SOLICITAR_CITA

    @property
    def titulo(self) -> str:
        return "Solicitar cita"

    @property
    def control(self) -> ft.Control:
        return self._control

    @staticmethod
    def _crear_presentacion() -> ft.Control:
        return ft.Container(
            bgcolor=COLOR_PRIMARIO,
            border_radius=22,
            padding=20,
            content=ft.Row(
                spacing=16,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        expand=True,
                        spacing=7,
                        controls=[
                            ft.Text(
                                "PROCESO GUIADO",
                                color=COLOR_PRIMARIO_SUAVE,
                                size=11,
                                weight=ft.FontWeight.W_600,
                            ),
                            ft.Text(
                                "Nueva solicitud de cita",
                                color=COLOR_SUPERFICIE,
                                size=21,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Completa la solicitud en tres pasos sencillos.",
                                color=COLOR_PRIMARIO_SUAVE,
                                size=13,
                            ),
                        ],
                    ),
                    ft.Icon(
                        icon=ft.Icons.MORE_TIME,
                        color=COLOR_SUPERFICIE,
                        size=34,
                        semantics_label="Nueva solicitud",
                    ),
                ],
            ),
        )

    @classmethod
    def _crear_pasos(cls) -> ft.Control:
        return ft.Column(
            spacing=12,
            controls=[
                ft.Text(
                    "Cómo solicitarás tu cita",
                    color=COLOR_TEXTO_PRINCIPAL,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                cls._crear_paso(
                    numero=1,
                    titulo="Atención requerida",
                    descripcion="Indica el tipo de atención que necesitas.",
                ),
                cls._crear_paso(
                    numero=2,
                    titulo="Fecha y horario",
                    descripcion=(
                        "Consulta la disponibilidad proporcionada por la clínica."
                    ),
                ),
                cls._crear_paso(
                    numero=3,
                    titulo="Revisión y envío",
                    descripcion="Verifica la información antes de enviar.",
                ),
            ],
        )

    @staticmethod
    def _crear_paso(numero: int, titulo: str, descripcion: str) -> ft.Control:
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
                        width=40,
                        height=40,
                        alignment=ft.Alignment.CENTER,
                        bgcolor=COLOR_PRIMARIO_SUAVE,
                        shape=ft.BoxShape.CIRCLE,
                        content=ft.Text(
                            str(numero),
                            color=COLOR_PRIMARIO_OSCURO,
                            size=15,
                            weight=ft.FontWeight.BOLD,
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
