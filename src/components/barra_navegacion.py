from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

from app.navegacion import DestinoPrincipal
from tema import COLOR_PRIMARIO_SUAVE, COLOR_SUPERFICIE


@dataclass(frozen=True, slots=True)
class ElementoNavegacion:
    destino: DestinoPrincipal
    etiqueta: str
    icono: ft.IconData
    icono_seleccionado: ft.IconData


ELEMENTOS_NAVEGACION = (
    ElementoNavegacion(
        destino=DestinoPrincipal.INICIO,
        etiqueta="Inicio",
        icono=ft.Icons.HOME_OUTLINED,
        icono_seleccionado=ft.Icons.HOME,
    ),
    ElementoNavegacion(
        destino=DestinoPrincipal.CITAS,
        etiqueta="Citas",
        icono=ft.Icons.CALENDAR_MONTH_OUTLINED,
        icono_seleccionado=ft.Icons.CALENDAR_MONTH,
    ),
    ElementoNavegacion(
        destino=DestinoPrincipal.PERFIL,
        etiqueta="Perfil",
        icono=ft.Icons.PERSON_OUTLINE,
        icono_seleccionado=ft.Icons.PERSON,
    ),
)


class BarraNavegacion:
    """Adapta los eventos de Flet a destinos propios de la aplicación."""

    def __init__(
        self,
        destino_seleccionado: DestinoPrincipal,
        al_seleccionar: Callable[[DestinoPrincipal], None],
    ) -> None:
        self._al_seleccionar = al_seleccionar
        self._control = ft.NavigationBar(
            selected_index=self._indice_de(destino_seleccionado),
            bgcolor=COLOR_SUPERFICIE,
            indicator_color=COLOR_PRIMARIO_SUAVE,
            elevation=2,
            label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
            on_change=self._manejar_cambio,
            destinations=[
                ft.NavigationBarDestination(
                    label=elemento.etiqueta,
                    icon=elemento.icono,
                    selected_icon=elemento.icono_seleccionado,
                )
                for elemento in ELEMENTOS_NAVEGACION
            ],
        )

    @property
    def control(self) -> ft.NavigationBar:
        return self._control

    def seleccionar(self, destino: DestinoPrincipal) -> None:
        self._control.selected_index = self._indice_de(destino)

    def _manejar_cambio(self, evento: ft.Event[ft.NavigationBar]) -> None:
        destino = ELEMENTOS_NAVEGACION[evento.control.selected_index].destino
        self._al_seleccionar(destino)

    @staticmethod
    def _indice_de(destino: DestinoPrincipal) -> int:
        for indice, elemento in enumerate(ELEMENTOS_NAVEGACION):
            if elemento.destino is destino:
                return indice

        raise ValueError(f"Destino sin elemento de navegación: {destino.value}")
