import flet as ft

from app.aplicacion import AplicacionMovil
from app.navegacion import DestinoPrincipal, EstadoNavegacion
from views.citas import VistaCitas
from views.contratos import VistaPrincipal
from views.inicio import VistaInicio
from views.perfil import VistaPerfil


def crear_vistas_principales() -> dict[DestinoPrincipal, VistaPrincipal]:
    return {
        DestinoPrincipal.INICIO: VistaInicio(),
        DestinoPrincipal.CITAS: VistaCitas(),
        DestinoPrincipal.PERFIL: VistaPerfil(),
    }


def main(page: ft.Page) -> None:
    aplicacion = AplicacionMovil(
        page=page,
        estado_navegacion=EstadoNavegacion(),
        vistas=crear_vistas_principales(),
    )
    aplicacion.iniciar()


if __name__ == "__main__":
    ft.run(main)
