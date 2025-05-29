from typing import Tuple
import polyscope.imgui as psim

# DISCLAIMER: colors given by ChatGPT
GREEN_NORMAL = (0.20, 0.70, 0.20, 1.00)
GREEN_HOVER = (0.30, 0.80, 0.30, 1.00)
GREEN_ACTIVE = (0.10, 0.60, 0.10, 1.00)

RED_NORMAL = (0.70, 0.20, 0.20, 1.00)
RED_HOVER = (0.80, 0.30, 0.30, 1.00)
RED_ACTIVE = (0.60, 0.10, 0.10, 1.00)


def state_button(
    value: bool,
    enabled_str: str,
    disabled_str: str,
    enabled_normal: Tuple[float, float, float, float] = RED_NORMAL,
    enabled_hover: Tuple[float, float, float, float] = RED_HOVER,
    enabled_active: Tuple[float, float, float, float] = RED_ACTIVE,
    disabled_normal: Tuple[float, float, float, float] = GREEN_NORMAL,
    disabled_hover: Tuple[float, float, float, float] = GREEN_HOVER,
    disabled_active: Tuple[float, float, float, float] = GREEN_ACTIVE,
) -> Tuple[bool, bool]:
    """
    A button with two states "Enabled/Disabled".
    When enabled, it shows `enabled_str`. Otherwise, `disabled_str`.
    Returns `clicked, value` tuple.
    """
    clicked = False

    psim.PushStyleColor(
        psim.ImGuiCol_Button, enabled_normal if value else disabled_normal
    )
    psim.PushStyleColor(
        psim.ImGuiCol_ButtonHovered, enabled_hover if value else disabled_hover
    )
    psim.PushStyleColor(
        psim.ImGuiCol_ButtonActive, enabled_active if value else disabled_active
    )
    if psim.Button(enabled_str if value else disabled_str):
        clicked = True
        value = not value
    psim.PopStyleColor(3)

    return clicked, value
