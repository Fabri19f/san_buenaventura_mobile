from unittest.mock import AsyncMock, Mock

import flet as ft
import pytest

from app.aplicacion import AplicacionMovil
from app.navegador_pila import NavegadorPila
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
    def cambiar_ruta(nueva_ruta: str) -> None:
        page.route = nueva_ruta
        page.on_route_change(Mock(route=nueva_ruta))

    page = Mock()
    page.route = ruta
    page.views = []
    page.navigate.side_effect = cambiar_ruta
    page.push_route = AsyncMock(side_effect=cambiar_ruta)
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
        NavegadorPila(page),
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
@pytest.mark.parametrize("origen", list(DestinoPrincipal))
def test_barra_cambia_la_ruta_y_mantiene_la_seleccion_coherente(
    indice: int,
    destino_esperado: DestinoPrincipal,
    origen: DestinoPrincipal,
) -> None:
    page = crear_pagina(ruta_principal(origen))
    estado = EstadoNavegacion(origen)
    aplicacion, vistas, _ = crear_aplicacion(page, estado)
    aplicacion.iniciar()
    page.update.reset_mock()

    raiz_original = page.views[0]
    barra = raiz_original.navigation_bar

    barra.selected_index = indice
    barra.on_change(Mock(control=barra))

    raiz = page.views[0]
    area_segura = raiz.controls[0]
    assert len(page.views) == 1
    assert raiz is raiz_original
    assert estado.destino_actual is destino_esperado
    assert raiz.route == "/"
    assert page.route == ruta_principal(destino_esperado)
    assert raiz.navigation_bar.selected_index == indice
    assert area_segura.content.content is vistas[destino_esperado].control
    page.navigate.assert_called_once_with(ruta_principal(destino_esperado))
    page.update.assert_called_once_with()


@pytest.mark.parametrize("ruta", list(RutaSecundaria))
def test_enlace_directo_a_secundaria_usa_su_destino_principal_como_raiz(
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
    assert raiz.route == "/"
    assert raiz.navigation_bar is not None
    assert raiz.navigation_bar.selected_index == list(DestinoPrincipal).index(destino)
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
    assert page.views[0].route == "/"
    assert page.route == "/citas"
    page.push_route.assert_awaited_once_with("/citas")


@pytest.mark.parametrize(
    ("origen", "ruta"),
    [
        (DestinoPrincipal.INICIO, RutaSecundaria.SOLICITAR_CITA),
        (DestinoPrincipal.CITAS, RutaSecundaria.SOLICITAR_CITA),
        (DestinoPrincipal.PERFIL, RutaSecundaria.INFORMACION_PERSONAL),
    ],
)
async def test_abrir_y_retroceder_conserva_la_vista_de_origen(
    origen: DestinoPrincipal,
    ruta: RutaSecundaria,
) -> None:
    page = crear_pagina(ruta_principal(origen))
    estado = EstadoNavegacion(origen)
    aplicacion, vistas, _ = crear_aplicacion(page, estado)
    aplicacion.iniciar()
    raiz = page.views[0]
    indice_original = raiz.navigation_bar.selected_index
    navegador = NavegadorPila(page)

    navegador.abrir(ruta)

    assert len(page.views) == 2
    assert page.views[0] is raiz
    assert raiz.route == "/"
    assert estado.destino_actual is origen
    assert raiz.navigation_bar.selected_index == indice_original
    assert raiz.controls[0].content.content is vistas[origen].control
    assert page.views[-1].route == ruta.value

    await page.on_view_pop(Mock(view=page.views[-1]))

    assert len(page.views) == 1
    assert page.views[0] is raiz
    assert page.route == ruta_principal(origen)
    assert estado.destino_actual is origen
    assert raiz.navigation_bar.selected_index == indice_original
    assert raiz.controls[0].content.content is vistas[origen].control


def test_repetir_una_ruta_no_duplica_ni_recrea_la_pantalla() -> None:
    page = crear_pagina()
    aplicacion, _, _ = crear_aplicacion(page)
    aplicacion.iniciar()
    navegador = NavegadorPila(page)
    navegador.abrir(RutaSecundaria.SOLICITAR_CITA)
    raiz, secundaria = page.views

    navegador.abrir(RutaSecundaria.SOLICITAR_CITA)

    assert len(page.views) == 2
    assert page.views[0] is raiz
    assert page.views[1] is secundaria


@pytest.mark.parametrize("con_secundaria", [False, True])
async def test_retroceso_no_elimina_la_raiz_ni_una_vista_ajena(
    con_secundaria: bool,
) -> None:
    page = crear_pagina()
    aplicacion, _, _ = crear_aplicacion(page)
    aplicacion.iniciar()
    raiz = page.views[0]
    if con_secundaria:
        NavegadorPila(page).abrir(RutaSecundaria.SOLICITAR_CITA)
    pila_original = list(page.views)

    await page.on_view_pop(Mock(view=raiz))
    await page.on_view_pop(Mock(view=None))
    await page.on_view_pop(Mock(view=ft.View(route="/ajena")))

    assert len(page.views) == len(pila_original)
    assert all(actual is original for actual, original in zip(page.views, pila_original))
    page.push_route.assert_not_awaited()


async def test_retroceso_a_una_secundaria_conserva_las_vistas_inferiores() -> None:
    page = crear_pagina()
    aplicacion, _, _ = crear_aplicacion(page)
    aplicacion.iniciar()
    navegador = NavegadorPila(page)
    navegador.abrir(RutaSecundaria.SOLICITAR_CITA)
    raiz, solicitud = page.views
    navegador.abrir(RutaSecundaria.INFORMACION_PERSONAL)
    superior = page.views[-1]

    await page.on_view_pop(Mock(view=superior))
    await page.on_view_pop(Mock(view=superior))

    assert len(page.views) == 2
    assert page.views[0] is raiz
    assert page.views[1] is solicitud
    assert page.route == RutaSecundaria.SOLICITAR_CITA.value
    page.push_route.assert_awaited_once_with(RutaSecundaria.SOLICITAR_CITA.value)


def test_volver_por_ruta_a_una_vista_existente_recorta_la_pila() -> None:
    page = crear_pagina()
    aplicacion, _, _ = crear_aplicacion(page)
    aplicacion.iniciar()
    navegador = NavegadorPila(page)
    navegador.abrir(RutaSecundaria.SOLICITAR_CITA)
    raiz, solicitud = page.views
    navegador.abrir(RutaSecundaria.INFORMACION_PERSONAL)

    page.on_route_change(Mock(route=RutaSecundaria.SOLICITAR_CITA.value))

    assert len(page.views) == 2
    assert page.views[0] is raiz
    assert page.views[1] is solicitud


def test_ruta_principal_cierra_la_secundaria_sin_reemplazar_la_raiz() -> None:
    page = crear_pagina()
    aplicacion, vistas, _ = crear_aplicacion(page)
    aplicacion.iniciar()
    raiz = page.views[0]
    navegador = NavegadorPila(page)
    navegador.abrir(RutaSecundaria.SOLICITAR_CITA)

    navegador.ir_a_destino(DestinoPrincipal.PERFIL)

    assert len(page.views) == 1
    assert page.views[0] is raiz
    assert raiz.route == "/"
    assert page.route == "/perfil"
    assert raiz.navigation_bar.selected_index == 2
    assert raiz.controls[0].content.content is vistas[DestinoPrincipal.PERFIL].control


def test_ruta_desconocida_se_redirige_a_su_raiz() -> None:
    page = crear_pagina("/citas/desconocida")
    aplicacion, _, _ = crear_aplicacion(page)

    aplicacion.iniciar()

    page.navigate.assert_called_once_with("/citas")
    assert len(page.views) == 1
    assert page.route == "/citas"
    assert page.views[0].route == "/"
    assert page.views[0].navigation_bar.selected_index == 1


def test_aplicacion_rechaza_un_catalogo_de_vistas_incompleto() -> None:
    vistas = crear_vistas()
    del vistas[DestinoPrincipal.PERFIL]

    with pytest.raises(ValueError, match="perfil"):
        AplicacionMovil(
            crear_pagina(),
            EstadoNavegacion(),
            vistas,
            crear_pantallas(),
            Mock(),
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
            Mock(),
        )


def test_aplicacion_rechaza_una_pantalla_registrada_con_otra_ruta() -> None:
    pantallas = crear_pantallas()
    pantallas[RutaSecundaria.SOLICITAR_CITA] = PantallaPrueba(
        RutaSecundaria.INFORMACION_PERSONAL
    )

    with pytest.raises(ValueError, match="/citas/solicitar.*informacion-personal"):
        AplicacionMovil(
            crear_pagina(),
            EstadoNavegacion(),
            crear_vistas(),
            pantallas,
            Mock(),
        )
