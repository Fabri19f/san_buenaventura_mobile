from unittest.mock import Mock

import flet as ft
import pytest

from app.aplicacion import AplicacionMovil
from app.navegacion import DestinoPrincipal, EstadoNavegacion
from views.contratos import VistaPrincipal


class VistaPrueba:
    def __init__(self, nombre: str) -> None:
        self._control = ft.Text(nombre)

    @property
    def control(self) -> ft.Control:
        return self._control


def crear_vistas() -> dict[DestinoPrincipal, VistaPrincipal]:
    return {
        destino: VistaPrueba(f"Vista {destino.value}")
        for destino in DestinoPrincipal
    }


def test_iniciar_muestra_inicio_y_configura_los_tres_destinos() -> None:
    page = Mock()
    vistas = crear_vistas()
    aplicacion = AplicacionMovil(page, EstadoNavegacion(), vistas)

    aplicacion.iniciar()

    area_segura = page.add.call_args.args[0]
    assert area_segura.content.content is vistas[DestinoPrincipal.INICIO].control
    assert page.navigation_bar.selected_index == 0
    assert [
        destino.label for destino in page.navigation_bar.destinations
    ] == ["Inicio", "Citas", "Perfil"]


@pytest.mark.parametrize(
    ("indice", "destino_esperado"),
    [
        (0, DestinoPrincipal.INICIO),
        (1, DestinoPrincipal.CITAS),
        (2, DestinoPrincipal.PERFIL),
    ],
)
def test_barra_cambia_la_vista_y_mantiene_la_seleccion_coherente(
    indice: int,
    destino_esperado: DestinoPrincipal,
) -> None:
    page = Mock()
    estado = EstadoNavegacion(DestinoPrincipal.PERFIL)
    vistas = crear_vistas()
    aplicacion = AplicacionMovil(page, estado, vistas)
    aplicacion.iniciar()
    barra = page.navigation_bar

    barra.selected_index = indice
    barra.on_change(Mock(control=barra))

    area_segura = page.add.call_args.args[0]
    assert estado.destino_actual is destino_esperado
    assert barra.selected_index == indice
    assert area_segura.content.content is vistas[destino_esperado].control
    page.update.assert_called_once_with()


def test_aplicacion_rechaza_un_catalogo_de_vistas_incompleto() -> None:
    vistas = crear_vistas()
    del vistas[DestinoPrincipal.PERFIL]

    with pytest.raises(ValueError, match="perfil"):
        AplicacionMovil(Mock(), EstadoNavegacion(), vistas)
