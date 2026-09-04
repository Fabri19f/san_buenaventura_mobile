from typing import Protocol

import flet as ft


class VistaPrincipal(Protocol):
    @property
    def control(self) -> ft.Control:
        """Control raíz que representa la vista."""
        ...


class VistaInformativa:
    """Vista sencilla para destinos que aún no tienen funciones adicionales."""

    def __init__(self, titulo: str, descripcion: str) -> None:
        self._control = ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            padding=24,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                controls=[
                    ft.Text(titulo, size=28),
                    ft.Text(descripcion, size=16),
                ],
            ),
        )

    @property
    def control(self) -> ft.Control:
        return self._control
