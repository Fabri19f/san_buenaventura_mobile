import pytest

from app.navegacion import DestinoPrincipal, EstadoNavegacion


def test_destino_inicial_es_inicio() -> None:
    estado = EstadoNavegacion()

    assert estado.destino_actual is DestinoPrincipal.INICIO


@pytest.mark.parametrize(
    "destino",
    [
        DestinoPrincipal.INICIO,
        DestinoPrincipal.CITAS,
        DestinoPrincipal.PERFIL,
    ],
)
def test_seleccionar_actualiza_el_destino(destino: DestinoPrincipal) -> None:
    estado = EstadoNavegacion(DestinoPrincipal.PERFIL)

    estado.seleccionar(destino)

    assert estado.destino_actual is destino
