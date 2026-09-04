from collections.abc import Mapping
from enum import Enum
from types import MappingProxyType
from typing import Final

from app.navegacion import DestinoPrincipal


class RutaSecundaria(Enum):
    SOLICITAR_CITA = "/citas/solicitar"
    INFORMACION_PERSONAL = "/perfil/informacion-personal"


RUTAS_PRINCIPALES: Final[Mapping[DestinoPrincipal, str]] = MappingProxyType(
    {
        DestinoPrincipal.INICIO: "/",
        DestinoPrincipal.CITAS: "/citas",
        DestinoPrincipal.PERFIL: "/perfil",
    }
)


def ruta_principal(destino: DestinoPrincipal) -> str:
    return RUTAS_PRINCIPALES[destino]


def destino_principal(ruta: str) -> DestinoPrincipal:
    if ruta == "/citas" or ruta.startswith("/citas/"):
        return DestinoPrincipal.CITAS

    if ruta == "/perfil" or ruta.startswith("/perfil/"):
        return DestinoPrincipal.PERFIL

    return DestinoPrincipal.INICIO


def ruta_secundaria(ruta: str) -> RutaSecundaria | None:
    try:
        return RutaSecundaria(ruta)
    except ValueError:
        return None


def normalizar_ruta(ruta: str) -> str:
    if ruta in RUTAS_PRINCIPALES.values() or ruta_secundaria(ruta) is not None:
        return ruta

    return ruta_principal(destino_principal(ruta))
