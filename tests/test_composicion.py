from unittest.mock import Mock

from app.navegacion import DestinoPrincipal
from app.rutas import RutaSecundaria
from main import crear_pantallas_secundarias, crear_vistas_principales
from views.citas import VistaCitas
from views.informacion_personal import PantallaInformacionPersonal
from views.inicio import VistaInicio
from views.perfil import VistaPerfil
from views.solicitar_cita import PantallaSolicitarCita


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
