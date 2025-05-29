from enum import Enum
from typing import Dict

from ps_utils.ui.key_handler import KEY_HANDLER
from ps_utils.ui.map_utils import get_enum_maps
from ps_utils.ui.sliders import choice_slider

import polyscope as ps


class ControlMode(Enum):
    TRANSLATION = "translation"
    ROTATION = "rotation"
    TRANSLATION_ROTATION = "translation_rotation"
    SCALE = "scale"


CONTROL_MODE_MAP, CONTROL_MODE_IMAP, _, _ = get_enum_maps(ControlMode)

CONTROL_MODE_TO_PS_TRANSFORM = {
    ControlMode.TRANSLATION: ps.TransformMode.TRANSLATION,
    ControlMode.ROTATION: ps.TransformMode.ROTATION,
    ControlMode.TRANSLATION_ROTATION: ps.TransformMode.TRANSLATION
    | ps.TransformMode.ROTATION,
    ControlMode.SCALE: ps.TransformMode.SCALE,
}
CONTROL_MODE_KEYMAP = {
    "t": ControlMode.TRANSLATION,
    "r": ControlMode.ROTATION,
    "e": ControlMode.TRANSLATION_ROTATION,
    "s": ControlMode.SCALE,
}


def update_control_mode(structure: ps.Structure, new_mode: ControlMode) -> None:
    if structure is not None:
        structure.set_transform_mode_gizmo(CONTROL_MODE_TO_PS_TRANSFORM[new_mode])


def key_control_mode(
    structure: ps.Structure,
    control_mode: ControlMode,
    keymap: Dict[str, ControlMode] = CONTROL_MODE_KEYMAP,
) -> ControlMode:
    """
    Press key to change gizmo ControlMode of `structure` according to `keymap`
    """
    for k, mode in keymap.items():
        if KEY_HANDLER(k):
            control_mode = mode
            update_control_mode(structure, control_mode)
    return control_mode


def slider_control_mode(
    name: str,
    structure: ps.Structure,
    control_mode: ControlMode,
) -> ControlMode:
    """
    Abstraction on top of `choice_slider` to also update the corresponding gizmo
    """
    clicked, control_mode = choice_slider(
        name, control_mode, CONTROL_MODE_MAP, CONTROL_MODE_IMAP
    )
    if clicked:
        update_control_mode(structure, control_mode)
    return control_mode
