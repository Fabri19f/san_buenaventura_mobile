from unittest.mock import Mock

import flet as ft

from components.tarjeta_acceso import TarjetaAcceso


def test_tarjeta_interactiva_delega_la_seleccion() -> None:
    al_seleccionar = Mock()
    tarjeta = TarjetaAcceso(
        titulo="Acción",
        descripcion="Descripción",
        icono=ft.Icons.EVENT,
        color_icono="#000000",
        color_fondo_icono="#FFFFFF",
        al_seleccionar=al_seleccionar,
    ).control

    tarjeta.on_click(Mock(control=tarjeta))

    assert tarjeta.ink is True
    assert len(tarjeta.content.controls) == 3
    al_seleccionar.assert_called_once_with()


def test_tarjeta_informativa_no_simula_interaccion() -> None:
    tarjeta = TarjetaAcceso(
        titulo="Información",
        descripcion="Descripción",
        icono=ft.Icons.INFO,
        color_icono="#000000",
        color_fondo_icono="#FFFFFF",
    ).control

    assert tarjeta.on_click is None
    assert tarjeta.ink is False
    assert len(tarjeta.content.controls) == 2
