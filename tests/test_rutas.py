from unittest.mock import Mock, call

import pytest

from app.navegador_pila import NavegadorPila
from app.navegacion import DestinoPrincipal
from app.rutas import (
    RutaSecundaria,
    destino_principal,
    normalizar_ruta,
    ruta_principal,
    ruta_secundaria,
)


@pytest.mark.parametrize(
    ("destino", "ruta"),
    [
        (DestinoPrincipal.INICIO, "/"),
        (DestinoPrincipal.CITAS, "/citas"),
        (DestinoPrincipal.PERFIL, "/perfil"),
    ],
)
def test_destino_principal_tiene_una_ruta_estable(
    destino: DestinoPrincipal,
    ruta: str,
) -> None:
    assert ruta_principal(destino) == ruta
    assert destino_principal(ruta) is destino


@pytest.mark.parametrize(
    ("ruta", "destino"),
    [
        (RutaSecundaria.SOLICITAR_CITA, DestinoPrincipal.CITAS),
        (RutaSecundaria.INFORMACION_PERSONAL, DestinoPrincipal.PERFIL),
    ],
)
def test_ruta_secundaria_conserva_su_destino_principal(
    ruta: RutaSecundaria,
    destino: DestinoPrincipal,
) -> None:
    assert destino_principal(ruta.value) is destino
    assert ruta_secundaria(ruta.value) is ruta


def test_ruta_desconocida_no_se_convierte_en_pantalla_secundaria() -> None:
    assert ruta_secundaria("/citas/desconocida") is None


@pytest.mark.parametrize(
    ("ruta", "ruta_esperada"),
    [
        ("/desconocida", "/"),
        ("/citas/desconocida", "/citas"),
        ("/perfil/desconocida", "/perfil"),
    ],
)
def test_ruta_desconocida_se_normaliza_a_una_raiz_segura(
    ruta: str,
    ruta_esperada: str,
) -> None:
    assert normalizar_ruta(ruta) == ruta_esperada


def test_navegador_traduce_intenciones_a_rutas_de_flet() -> None:
    page = Mock()
    navegador = NavegadorPila(page)

    navegador.ir_a_destino(DestinoPrincipal.CITAS)
    navegador.abrir(RutaSecundaria.SOLICITAR_CITA)

    assert page.navigate.call_args_list == [
        call("/citas"),
        call("/citas/solicitar"),
    ]
