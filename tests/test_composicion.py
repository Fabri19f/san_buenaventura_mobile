from app.navegacion import DestinoPrincipal
from main import crear_vistas_principales
from views.inicio import VistaInicio
from views.vista_informativa import VistaInformativa


def test_inicio_usa_una_vista_especializada() -> None:
    vistas = crear_vistas_principales()

    assert isinstance(vistas[DestinoPrincipal.INICIO], VistaInicio)
    assert isinstance(vistas[DestinoPrincipal.CITAS], VistaInformativa)
    assert isinstance(vistas[DestinoPrincipal.PERFIL], VistaInformativa)
