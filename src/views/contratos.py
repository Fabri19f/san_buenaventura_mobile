from typing import Protocol

import flet as ft


class VistaPrincipal(Protocol):
    @property
    def control(self) -> ft.Control:
        """Control raíz que representa la vista."""
        ...
