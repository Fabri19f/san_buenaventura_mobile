from collections.abc import Mapping

import flet as ft

from app.navegacion import DestinoPrincipal, EstadoNavegacion
from app.rutas import (
    RutaSecundaria,
    destino_principal,
    normalizar_ruta,
    ruta_principal,
    ruta_secundaria,
)
from components.barra_navegacion import BarraNavegacion
from tema import (
    COLOR_FONDO,
    COLOR_SUPERFICIE,
    COLOR_TEXTO_PRINCIPAL,
    crear_tema,
)
from views.contratos import PantallaSecundaria, VistaPrincipal


class AplicacionMovil:
    """Coordina la página, la navegación y las vistas principales."""

    def __init__(
        self,
        page: ft.Page,
        estado_navegacion: EstadoNavegacion,
        vistas: Mapping[DestinoPrincipal, VistaPrincipal],
        pantallas: Mapping[RutaSecundaria, PantallaSecundaria],
    ) -> None:
        self._validar_vistas(vistas)
        self._validar_pantallas(pantallas)
        self._page = page
        self._estado_navegacion = estado_navegacion
        self._vistas = dict(vistas)
        self._pantallas = dict(pantallas)
        self._contenido = ft.Container(expand=True)
        self._area_principal = ft.SafeArea(content=self._contenido, expand=True)
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
        self._page.on_route_change = self._manejar_cambio_ruta
        self._page.on_view_pop = self._manejar_retroceso
        self._reconstruir_vistas(self._page.route)

    def seleccionar_destino(self, destino: DestinoPrincipal) -> None:
        self._page.go(ruta_principal(destino))

    def _manejar_cambio_ruta(self, evento: ft.RouteChangeEvent) -> None:
        self._reconstruir_vistas(evento.route)

    async def _manejar_retroceso(self, evento: ft.ViewPopEvent) -> None:
        if evento.view is None or evento.view not in self._page.views:
            return

        self._page.views.remove(evento.view)
        if not self._page.views:
            return

        await self._page.push_route(self._page.views[-1].route)

    def _reconstruir_vistas(self, ruta: str) -> None:
        ruta_normalizada = normalizar_ruta(ruta)
        if ruta_normalizada != ruta:
            self._page.go(ruta_normalizada)
            return

        destino = destino_principal(ruta)
        self._estado_navegacion.seleccionar(destino)
        self._barra_navegacion.seleccionar(destino)
        self._mostrar_vista_actual()

        self._page.views.clear()
        self._page.views.append(self._crear_vista_principal(destino))

        secundaria = ruta_secundaria(ruta)
        if secundaria is not None:
            self._page.views.append(
                self._crear_vista_secundaria(self._pantallas[secundaria])
            )

        self._page.update()

    def _crear_vista_principal(self, destino: DestinoPrincipal) -> ft.View:
        return ft.View(
            route=ruta_principal(destino),
            controls=[self._area_principal],
            navigation_bar=self._barra_navegacion.control,
            bgcolor=COLOR_FONDO,
            padding=0,
        )

    @staticmethod
    def _crear_vista_secundaria(pantalla: PantallaSecundaria) -> ft.View:
        return ft.View(
            route=pantalla.ruta.value,
            appbar=ft.AppBar(
                title=ft.Text(
                    pantalla.titulo,
                    color=COLOR_TEXTO_PRINCIPAL,
                    weight=ft.FontWeight.W_600,
                ),
                bgcolor=COLOR_SUPERFICIE,
                elevation=0,
                automatically_imply_leading=True,
            ),
            controls=[ft.SafeArea(content=pantalla.control, expand=True)],
            bgcolor=COLOR_FONDO,
            padding=0,
        )

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

    @staticmethod
    def _validar_pantallas(
        pantallas: Mapping[RutaSecundaria, PantallaSecundaria],
    ) -> None:
        rutas_esperadas = set(RutaSecundaria)
        rutas_recibidas = set(pantallas)
        if rutas_recibidas == rutas_esperadas:
            return

        faltantes = rutas_esperadas - rutas_recibidas
        if faltantes:
            nombres = ", ".join(sorted(ruta.value for ruta in faltantes))
            raise ValueError(f"Faltan pantallas para las rutas: {nombres}")

        raise ValueError("El catálogo contiene rutas no reconocidas")
