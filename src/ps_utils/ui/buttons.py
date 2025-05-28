from typing import Tuple
import polyscope.imgui as psim


def state_button(
    value: bool,
    enabled_str: str,
    disabled_str: str,
    # enabled_hue: float = 0.0,
    # disable_hue: float = 0.4,
) -> Tuple[bool, bool]:
    """
    A button with two states "Enabled/Disabled".
    When enables, it shows `enabled_str`. Otherwise, `disabled_str`.
    Returns `clicked, value` tuple.
    """
    clicked = False

    if psim.Button(enabled_str if value else disabled_str):
        clicked = True
        value = not value

    return clicked, value
