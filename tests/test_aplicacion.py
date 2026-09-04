from unittest.mock import AsyncMock, Mock

import flet as ft
import pytest

from app.aplicacion import AplicacionMovil
from app.navegacion import DestinoPrincipal, EstadoNavegacion
from app.rutas import RutaSecundaria, ruta_principal
from views.contratos import PantallaSecundaria, VistaPrincipal


class VistaPrueba:
    def __init__(self, nombre: str) -> None:
        self._control = ft.Text(nombre)

    @property
    def control(self) -> ft.Control:
        return self._control


class PantallaPrueba:
    def __init__(self, ruta: RutaSecundaria) -> None:
        self._ruta = ruta
        self._control = ft.Text(f"Pantalla {ruta.value}")

    @property
    def ruta(self) -> RutaSecundaria:
        return self._ruta

    @property
    def titulo(self) -> str:
        return f"Título {self._ruta.value}"

    @property
    def control(self) -> ft.Control:
        return self._control


def crear_vistas() -> dict[DestinoPrincipal, VistaPrincipal]:
    return {
        destino: VistaPrueba(f"Vista {destino.value}")
        for destino in DestinoPrincipal
    }


def crear_pantallas() -> dict[RutaSecundaria, PantallaSecundaria]:
    return {ruta: PantallaPrueba(ruta) for ruta in RutaSecundaria}


def crear_pagina(ruta: str = "/") -> Mock:
    page = Mock()
    page.route = ruta
    page.views = []
    page.push_route = AsyncMock()
    return page


def crear_aplicacion(
    page: Mock,
    estado: EstadoNavegacion | None = None,
) -> tuple[
    AplicacionMovil,
    dict[DestinoPrincipal, VistaPrincipal],
    dict[RutaSecundaria, PantallaSecundaria],
]:
    vistas = crear_vistas()
    pantallas = crear_pantallas()
    aplicacion = AplicacionMovil(
        page,
        estado or EstadoNavegacion(),
        vistas,
        pantallas,
    )
    return aplicacion, vistas, pantallas


def test_iniciar_muestra_inicio_y_configura_los_tres_destinos() -> None:
    page = crear_pagina()
    aplicacion, vistas, _ = crear_aplicacion(page)

    aplicacion.iniciar()

    raiz = page.views[0]
    area_segura = raiz.controls[0]
    assert raiz.route == "/"
    assert area_segura.content.content is vistas[DestinoPrincipal.INICIO].control
    assert raiz.navigation_bar.selected_index == 0
    assert [
        destino.label for destino in raiz.navigation_bar.destinations
    ] == ["Inicio", "Citas", "Perfil"]
    page.update.assert_called_once_with()


@pytest.mark.parametrize(
    ("indice", "destino_esperado"),
    [
        (0, DestinoPrincipal.INICIO),
        (1, DestinoPrincipal.CITAS),
        (2, DestinoPrincipal.PERFIL),
    ],
)
def test_barra_cambia_la_ruta_y_mantiene_la_seleccion_coherente(
    indice: int,
    destino_esperado: DestinoPrincipal,
) -> None:
    page = crear_pagina("/perfil")
    estado = EstadoNavegacion(DestinoPrincipal.PERFIL)
    aplicacion, vistas, _ = crear_aplicacion(page, estado)
    aplicacion.iniciar()
    page.update.reset_mock()

    def cambiar_ruta(ruta: str) -> None:
        page.route = ruta
        page.on_route_change(Mock(route=ruta))

    page.go.side_effect = cambiar_ruta
    barra = page.views[0].navigation_bar

    barra.selected_index = indice
    barra.on_change(Mock(control=barra))

    raiz = page.views[0]
    area_segura = raiz.controls[0]
    assert estado.destino_actual is destino_esperado
    assert raiz.route == ruta_principal(destino_esperado)
    assert raiz.navigation_bar.selected_index == indice
    assert area_segura.content.content is vistas[destino_esperado].control
    page.go.assert_called_once_with(ruta_principal(destino_esperado))
    page.update.assert_called_once_with()


@pytest.mark.parametrize("ruta", list(RutaSecundaria))
def test_ruta_secundaria_se_apila_sobre_su_destino_principal(
    ruta: RutaSecundaria,
) -> None:
    page = crear_pagina(ruta.value)
    aplicacion, _, pantallas = crear_aplicacion(page)

    aplicacion.iniciar()

    raiz, secundaria = page.views
    destino = (
        DestinoPrincipal.CITAS
        if ruta is RutaSecundaria.SOLICITAR_CITA
        else DestinoPrincipal.PERFIL
    )
    assert raiz.route == ruta_principal(destino)
    assert raiz.navigation_bar is not None
    assert secundaria.route == ruta.value
    assert secundaria.navigation_bar is None
    assert secundaria.appbar.title.value == pantallas[ruta].titulo
    assert secundaria.controls[0].content is pantallas[ruta].control


async def test_retroceso_desapila_la_pantalla_y_restaura_la_ruta_raiz() -> None:
    page = crear_pagina(RutaSecundaria.SOLICITAR_CITA.value)
    aplicacion, _, _ = crear_aplicacion(page)
    aplicacion.iniciar()
    secundaria = page.views[-1]

    await page.on_view_pop(Mock(view=secundaria))

    assert len(page.views) == 1
    assert page.views[0].route == "/citas"
    page.push_route.assert_awaited_once_with("/citas")


def test_ruta_desconocida_se_redirige_a_su_raiz() -> None:
    page = crear_pagina("/citas/desconocida")
    aplicacion, _, _ = crear_aplicacion(page)

    aplicacion.iniciar()

    page.go.assert_called_once_with("/citas")
    assert page.views == []


def test_aplicacion_rechaza_un_catalogo_de_vistas_incompleto() -> None:
    vistas = crear_vistas()
    del vistas[DestinoPrincipal.PERFIL]

    with pytest.raises(ValueError, match="perfil"):
        AplicacionMovil(
            crear_pagina(),
            EstadoNavegacion(),
            vistas,
            crear_pantallas(),
        )


def test_aplicacion_rechaza_un_catalogo_de_pantallas_incompleto() -> None:
    pantallas = crear_pantallas()
    del pantallas[RutaSecundaria.INFORMACION_PERSONAL]

    with pytest.raises(ValueError, match="informacion-personal"):
        AplicacionMovil(
            crear_pagina(),
            EstadoNavegacion(),
            crear_vistas(),
            pantallas,
        )
