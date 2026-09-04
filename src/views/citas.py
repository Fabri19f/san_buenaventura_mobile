import flet as ft

from app.navegador_pila import NavegadorAplicacion
from app.rutas import RutaSecundaria
from components.encabezado_seccion import EncabezadoSeccion
from components.seccion_accesos import SeccionAccesos
from components.tarjeta_acceso import TarjetaAcceso
from components.tarjeta_aviso import TarjetaAviso
from tema import (
    COLOR_AZUL,
    COLOR_AZUL_SUAVE,
    COLOR_BORDE,
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_SUAVE,
    COLOR_ROJO,
    COLOR_ROJO_SUAVE,
    COLOR_SUPERFICIE,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
)


class VistaCitas:
    """Presenta el espacio de gestión de citas sin operaciones reales."""

    def __init__(self, navegador: NavegadorAplicacion) -> None:
        self._control = ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                spacing=24,
                controls=[
                    EncabezadoSeccion(
                        titulo="Citas",
                        descripcion="Organiza tu atención desde un solo lugar.",
                        icono=ft.Icons.CALENDAR_MONTH,
                        color_icono=COLOR_PRIMARIO,
                        color_fondo_icono=COLOR_PRIMARIO_SUAVE,
                    ).control,
                    self._crear_estado_citas(),
                    self._crear_acciones(navegador),
                    TarjetaAviso(
                        titulo="¿Necesitas cancelar una cita?",
                        descripcion=(
                            "Selecciona primero una cita programada; la opción de "
                            "cancelación estará dentro de su detalle."
                        ),
                        icono=ft.Icons.EVENT_BUSY,
                        color_icono=COLOR_ROJO,
                        color_titulo=COLOR_TEXTO_PRINCIPAL,
                        color_fondo=COLOR_ROJO_SUAVE,
                    ).control,
                ],
            ),
        )

    @property
    def control(self) -> ft.Control:
        return self._control

    @staticmethod
    def _crear_estado_citas() -> ft.Control:
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
                        width=56,
                        height=56,
                        alignment=ft.Alignment.CENTER,
                        bgcolor=COLOR_AZUL_SUAVE,
                        border_radius=16,
                        content=ft.Icon(
                            icon=ft.Icons.EVENT_NOTE,
                            color=COLOR_AZUL,
                            size=28,
                            semantics_label="Resumen de citas",
                        ),
                    ),
                    ft.Column(
                        expand=True,
                        spacing=5,
                        controls=[
                            ft.Text(
                                "Tus citas aparecerán aquí",
                                color=COLOR_TEXTO_PRINCIPAL,
                                size=17,
                                weight=ft.FontWeight.W_600,
                            ),
                            ft.Text(
                                "Podrás revisar sus detalles y estado cuando "
                                "estén disponibles.",
                                color=COLOR_TEXTO_SECUNDARIO,
                                size=13,
                            ),
                        ],
                    ),
                ],
            ),
        )

    @staticmethod
    def _crear_acciones(navegador: NavegadorAplicacion) -> ft.Control:
        return SeccionAccesos(
            titulo="Nueva gestión",
            descripcion="Inicia una solicitud desde esta sección.",
            accesos=(
                TarjetaAcceso(
                    titulo="Solicitar una cita",
                    descripcion="Inicia una nueva solicitud de atención.",
                    icono=ft.Icons.MORE_TIME,
                    color_icono=COLOR_PRIMARIO,
                    color_fondo_icono=COLOR_PRIMARIO_SUAVE,
                    al_seleccionar=lambda: navegador.abrir(
                        RutaSecundaria.SOLICITAR_CITA
                    ),
                ),
            ),
        ).control
