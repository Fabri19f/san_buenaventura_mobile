from enum import Enum


class DestinoPrincipal(Enum):
    INICIO = "inicio"
    CITAS = "citas"
    PERFIL = "perfil"


class EstadoNavegacion:
    """Mantiene una única fuente de verdad para la navegación principal."""

    def __init__(
        self,
        destino_inicial: DestinoPrincipal = DestinoPrincipal.INICIO,
    ) -> None:
        self._destino_actual = destino_inicial

    @property
    def destino_actual(self) -> DestinoPrincipal:
        return self._destino_actual

    def seleccionar(self, destino: DestinoPrincipal) -> None:
        self._destino_actual = destino
