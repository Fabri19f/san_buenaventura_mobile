from app.navegacion import DestinoPrincipal
from main import crear_vistas_principales
from views.citas import VistaCitas
from views.inicio import VistaInicio
from views.perfil import VistaPerfil


def test_destinos_principales_usan_vistas_especializadas() -> None:
    vistas = crear_vistas_principales()

    assert isinstance(vistas[DestinoPrincipal.INICIO], VistaInicio)
    assert isinstance(vistas[DestinoPrincipal.CITAS], VistaCitas)
    assert isinstance(vistas[DestinoPrincipal.PERFIL], VistaPerfil)
