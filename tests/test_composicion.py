import asyncio
from collections.abc import Iterator
from unittest.mock import Mock

import flet as ft
import pytest

from app.navegador_pila import NavegadorPila
from app.navegacion import DestinoPrincipal
from app.rutas import RutaSecundaria
from main import crear_pantallas_secundarias, crear_vistas_principales, main
from views.citas import VistaCitas
from views.informacion_personal import PantallaInformacionPersonal
from views.inicio import VistaInicio
from views.perfil import VistaPerfil
from views.solicitar_cita import PantallaSolicitarCita


@pytest.fixture
def pagina_flet(monkeypatch: pytest.MonkeyPatch) -> Iterator[ft.Page]:
    sesion = Mock()
    page = ft.Page(sess=sesion)

    async def cambiar_ruta(ruta: str) -> None:
        # Simula la respuesta del cliente Flutter; navigate() sigue siendo real.
        page.route = ruta
        assert page.on_route_change is not None
        page.on_route_change(
            ft.RouteChangeEvent(control=page, name="route_change", route=ruta)
        )

    monkeypatch.setattr(page, "push_route", cambiar_ruta)
    monkeypatch.setattr(page, "update", Mock())
    yield page


def test_destinos_principales_usan_vistas_especializadas() -> None:
    vistas = crear_vistas_principales(Mock())

    assert isinstance(vistas[DestinoPrincipal.INICIO], VistaInicio)
    assert isinstance(vistas[DestinoPrincipal.CITAS], VistaCitas)
    assert isinstance(vistas[DestinoPrincipal.PERFIL], VistaPerfil)


def test_rutas_secundarias_usan_pantallas_especializadas() -> None:
    pantallas = crear_pantallas_secundarias()

    assert isinstance(
        pantallas[RutaSecundaria.SOLICITAR_CITA],
        PantallaSolicitarCita,
    )
    assert isinstance(
        pantallas[RutaSecundaria.INFORMACION_PERSONAL],
        PantallaInformacionPersonal,
    )


@pytest.mark.parametrize(
    ("indice", "origen", "secundaria"),
    [
        (0, "/", RutaSecundaria.SOLICITAR_CITA),
        (1, "/citas", RutaSecundaria.SOLICITAR_CITA),
        (2, "/perfil", RutaSecundaria.INFORMACION_PERSONAL),
    ],
)
async def test_composicion_navega_con_la_api_real_de_flet_y_conserva_el_origen(
    pagina_flet: ft.Page,
    indice: int,
    origen: str,
    secundaria: RutaSecundaria,
) -> None:
    main(pagina_flet)
    raiz = pagina_flet.views[0]
    barra = raiz.navigation_bar
    assert isinstance(barra, ft.NavigationBar)
    assert barra.on_change is not None

    barra.selected_index = indice
    barra.on_change(ft.Event(control=barra, name="change"))
    # Cede un turno del bucle a la tarea programada por Page.navigate().
    await asyncio.sleep(0)

    assert pagina_flet.route == origen
    assert len(pagina_flet.views) == 1
    assert pagina_flet.views[0] is raiz
    assert raiz.route == "/"

    NavegadorPila(pagina_flet).abrir(secundaria)
    await asyncio.sleep(0)

    assert len(pagina_flet.views) == 2
    assert pagina_flet.views[0] is raiz
    assert pagina_flet.route == secundaria.value
    assert barra.selected_index == indice

    superior = pagina_flet.views[-1]
    assert pagina_flet.on_view_pop is not None
    await pagina_flet.on_view_pop(
        ft.ViewPopEvent(
            control=pagina_flet,
            name="view_pop",
            route=secundaria.value,
            view=superior,
        )
    )

    assert len(pagina_flet.views) == 1
    assert pagina_flet.views[0] is raiz
    assert pagina_flet.route == origen
    assert barra.selected_index == indice


async def test_composicion_redirige_una_ruta_invalida_con_la_api_real_de_flet(
    pagina_flet: ft.Page,
) -> None:
    pagina_flet.route = "/citas/desconocida"

    main(pagina_flet)
    await asyncio.sleep(0)

    assert pagina_flet.route == "/citas"
    assert len(pagina_flet.views) == 1
    raiz = pagina_flet.views[0]
    assert raiz.route == "/"
    assert isinstance(raiz.navigation_bar, ft.NavigationBar)
    assert raiz.navigation_bar.selected_index == 1
