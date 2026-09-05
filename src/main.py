import flet as ft

from app.aplicacion import AplicacionMovil
from app.navegador_pila import NavegadorAplicacion, NavegadorPila
from app.navegacion import DestinoPrincipal, EstadoNavegacion
from app.rutas import RutaSecundaria
from views.citas import VistaCitas
from views.contratos import PantallaSecundaria, VistaPrincipal
from views.informacion_personal import PantallaInformacionPersonal
from views.inicio import VistaInicio
from views.perfil import VistaPerfil
from views.solicitar_cita import PantallaSolicitarCita


def crear_vistas_principales(
    navegador: NavegadorAplicacion,
) -> dict[DestinoPrincipal, VistaPrincipal]:
    return {
        DestinoPrincipal.INICIO: VistaInicio(navegador),
        DestinoPrincipal.CITAS: VistaCitas(navegador),
        DestinoPrincipal.PERFIL: VistaPerfil(navegador),
    }


def crear_pantallas_secundarias() -> dict[RutaSecundaria, PantallaSecundaria]:
    return {
        RutaSecundaria.SOLICITAR_CITA: PantallaSolicitarCita(),
        RutaSecundaria.INFORMACION_PERSONAL: PantallaInformacionPersonal(),
    }


def main(page: ft.Page) -> None:
    navegador = NavegadorPila(page)
    aplicacion = AplicacionMovil(
        page=page,
        estado_navegacion=EstadoNavegacion(),
        vistas=crear_vistas_principales(navegador),
        pantallas=crear_pantallas_secundarias(),
        navegador=navegador,
    )
    aplicacion.iniciar()


if __name__ == "__main__":
    ft.run(main)
