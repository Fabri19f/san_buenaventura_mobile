from collections.abc import Mapping

import flet as ft

from app.navegacion import DestinoPrincipal, EstadoNavegacion
from app.navegador_pila import NavegadorAplicacion
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
        navegador: NavegadorAplicacion,
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
            al_seleccionar=navegador.ir_a_destino,
        )
        self._vista_principal = self._crear_vista_principal()

    def iniciar(self) -> None:
        self._page.title = "Clínica San Buenaventura"
        self._page.padding = 0
        self._page.bgcolor = COLOR_FONDO
        self._page.theme = crear_tema()
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.on_route_change = self._manejar_cambio_ruta
        self._page.on_view_pop = self._manejar_retroceso
        self._page.views[:] = [self._vista_principal]
        # Un enlace directo no tiene una vista de origen en esta sesión.
        self._mostrar_destino(destino_principal(self._page.route))
        self._sincronizar_vistas(self._page.route)

    def _manejar_cambio_ruta(self, evento: ft.RouteChangeEvent) -> None:
        self._sincronizar_vistas(evento.route)

    async def _manejar_retroceso(self, evento: ft.ViewPopEvent) -> None:
        if len(self._page.views) <= 1 or evento.view is not self._page.views[-1]:
            return

        self._page.views.pop()
        ruta = (
            ruta_principal(self._estado_navegacion.destino_actual)
            if len(self._page.views) == 1
            else self._page.views[-1].route
        )
        self._page.update()
        await self._page.push_route(ruta)

    def _sincronizar_vistas(self, ruta: str) -> None:
        ruta_normalizada = normalizar_ruta(ruta)
        if ruta_normalizada != ruta:
            self._page.navigate(ruta_normalizada)
            return

        secundaria = ruta_secundaria(ruta)
        if secundaria is None:
            del self._page.views[1:]
            self._mostrar_destino(destino_principal(ruta))
        else:
            self._apilar_pantalla(secundaria)

        self._page.update()

    def _apilar_pantalla(self, ruta: RutaSecundaria) -> None:
        for indice, vista in enumerate(self._page.views):
            if vista.route == ruta.value:
                del self._page.views[indice + 1 :]
                return

        self._page.views.append(
            self._crear_vista_secundaria(self._pantallas[ruta])
        )

    def _crear_vista_principal(self) -> ft.View:
        return ft.View(
            # Flet 0.86.5 usa View.route como clave del Navigator de Flutter.
            # Debe ser estable para cambiar de pestaña sin transición de pila.
            route="/",
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

    def _mostrar_destino(self, destino: DestinoPrincipal) -> None:
        self._estado_navegacion.seleccionar(destino)
        self._barra_navegacion.seleccionar(destino)
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
            for ruta, pantalla in pantallas.items():
                if pantalla.ruta is not ruta:
                    raise ValueError(
                        f"La pantalla registrada en {ruta.value} declara "
                        f"la ruta {pantalla.ruta.value}"
                    )
            return

        faltantes = rutas_esperadas - rutas_recibidas
        if faltantes:
            nombres = ", ".join(sorted(ruta.value for ruta in faltantes))
            raise ValueError(f"Faltan pantallas para las rutas: {nombres}")

        raise ValueError("El catálogo contiene rutas no reconocidas")
