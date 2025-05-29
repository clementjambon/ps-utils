from typing import Tuple
import os

import polyscope.imgui as psim

from ps_utils.ui.key_handler import KEY_HANDLER, KEYMAP

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


def save_popup(
    popup_name: str,
    path: str,
    save_label: str = "Save",
    confirm_label: str = "Confirm",
    show_warning: str = True,
):
    """
    Creates a save popup. When hitting `save_label`, a popup will open with the target path.
    If a file already exists at the target location, the popup will issue a warning (unless `show_warning` is set to False)
    Returns `requested, path`

    NB: Save popups trigger a KEY_HANDLER lock associated to their name!
    """
    requested = False

    if psim.Button(f"{save_label}##{popup_name}"):
        psim.OpenPopup(f"save_popup##{popup_name}")
        KEY_HANDLER.lock(popup_name)

    if psim.BeginPopup(f"save_popup##{popup_name}"):

        _, path = psim.InputText(f"path##{popup_name}", path)

        if show_warning and os.path.exists(path):
            psim.Text("Warning: a file already exists at this location!")

        if (
            psim.Button(f"{confirm_label}##{popup_name}")
            or psim.GetIO().KeysDown[KEYMAP["enter"]]
        ):
            requested = True
            KEY_HANDLER.unlock(popup_name)
            psim.CloseCurrentPopup()

        psim.EndPopup()

    return requested, path


# Save as save_popup but for an integer only
def int_popup(
    popup_name: str,
    val: int,
    val_name: str = "N",
    button_label: str = "Add",
    confirm_label: str = "Confirm",
):
    requested = False

    if psim.Button(f"{button_label}##{popup_name}"):
        psim.OpenPopup(f"int_popup##{popup_name}")
        KEY_HANDLER.lock(popup_name)

    if psim.BeginPopup(f"int_popup##{popup_name}"):

        _, val = psim.InputInt(f"{val_name}##{popup_name}", val)

        if (
            psim.Button(f"{confirm_label}##{popup_name}")
            or psim.GetIO().KeysDown[KEYMAP["enter"]]
        ):
            requested = True
            KEY_HANDLER.unlock(popup_name)
            psim.CloseCurrentPopup()

        psim.EndPopup()

    return requested, val
