from collections.abc import Mapping

import flet as ft

from app.navegacion import DestinoPrincipal, EstadoNavegacion
from components.barra_navegacion import BarraNavegacion
from tema import COLOR_FONDO, crear_tema
from views.contratos import VistaPrincipal


class AplicacionMovil:
    """Coordina la página, la navegación y las vistas principales."""

    def __init__(
        self,
        page: ft.Page,
        estado_navegacion: EstadoNavegacion,
        vistas: Mapping[DestinoPrincipal, VistaPrincipal],
    ) -> None:
        self._validar_vistas(vistas)
        self._page = page
        self._estado_navegacion = estado_navegacion
        self._vistas = dict(vistas)
        self._contenido = ft.Container(expand=True)
        self._barra_navegacion = BarraNavegacion(
            destino_seleccionado=estado_navegacion.destino_actual,
            al_seleccionar=self.seleccionar_destino,
        )

    def iniciar(self) -> None:
        self._page.title = "Clínica San Buenaventura"
        self._page.padding = 0
        self._page.bgcolor = COLOR_FONDO
        self._page.theme = crear_tema()
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.navigation_bar = self._barra_navegacion.control
        self._mostrar_vista_actual()
        self._page.add(ft.SafeArea(content=self._contenido, expand=True))

    def seleccionar_destino(self, destino: DestinoPrincipal) -> None:
        self._estado_navegacion.seleccionar(destino)
        self._barra_navegacion.seleccionar(destino)
        self._mostrar_vista_actual()
        self._page.update()

    def _mostrar_vista_actual(self) -> None:
        destino = self._estado_navegacion.destino_actual
        self._contenido.content = self._vistas[destino].control

    @staticmethod
    def _validar_vistas(
        vistas: Mapping[DestinoPrincipal, VistaPrincipal],
    ) -> None:
        destinos_esperados = set(DestinoPrincipal)
        destinos_recibidos = set(vistas)
        if destinos_recibidos == destinos_esperados:
            return

        faltantes = destinos_esperados - destinos_recibidos
        if faltantes:
            nombres = ", ".join(sorted(destino.value for destino in faltantes))
            raise ValueError(f"Faltan vistas para los destinos: {nombres}")

        raise ValueError("El catálogo contiene destinos no reconocidos")
