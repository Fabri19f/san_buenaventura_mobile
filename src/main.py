import flet as ft

from app.aplicacion import AplicacionMovil
from app.navegacion import DestinoPrincipal, EstadoNavegacion
from views.vista_informativa import VistaInformativa, VistaPrincipal


def crear_vistas_principales() -> dict[DestinoPrincipal, VistaPrincipal]:
    return {
        DestinoPrincipal.INICIO: VistaInformativa(
            titulo="Inicio",
            descripcion=(
                "Bienvenido a la aplicación móvil de la Clínica San Buenaventura."
            ),
        ),
        DestinoPrincipal.CITAS: VistaInformativa(
            titulo="Citas",
            descripcion="Esta es la sección destinada a tus citas.",
        ),
        DestinoPrincipal.PERFIL: VistaInformativa(
            titulo="Perfil",
            descripcion="Esta es la sección destinada a tu perfil.",
        ),
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
