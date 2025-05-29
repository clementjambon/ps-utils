from typing import List, Dict, Any
from enum import Enum

import numpy as np
import polyscope.imgui as psim

SLIDERS_INT = [psim.SliderInt, psim.SliderInt2, psim.SliderInt3, psim.SliderInt4]
SLIDERS_FLOAT = [
    psim.SliderFloat,
    psim.SliderFloat2,
    psim.SliderFloat3,
    psim.SliderFloat4,
]


def slider_n(
    name: str, vec: List[int | float], v_min: int | float = 0, v_max: int | float = 0
):
    """Provides n_sliders side by side."""
    assert len(vec) <= 4 and len(vec) > 0, "slider_n takes 1 to 4 components!"
    return SLIDERS_INT[len(vec) - 1](name, vec, v_min=v_min, v_max=v_max)


def drag_n(
    name: str,
    vec: List[int | float],
    v_min: int | float = 0,
    v_max: int | float = 0,
    width: int = 100,
):
    """Provides n DragInts side by side."""
    assert len(vec) <= 4 and len(vec) > 0, "drag_n takes 1 to 4 components!"
    psim.PushItemWidth(width)
    update = False
    for i in range(len(vec)):
        if i > 0:
            psim.SameLine()
        clicked, vec[i] = psim.DragInt(
            f"##{name}_{i}", vec[i], v_min=v_min, v_max=v_max
        )
        update |= clicked
    psim.PopItemWidth()
    psim.SameLine()
    psim.Text(name.split("##")[0])
    return update, vec


def input_n(
    name: str,
    vec: List[int | float],
    v_min: int | float = 0,
    v_max: int | float = 0,
    step: int = 1,
    width: int = 100,
    stride: int = 3,
):
    """Provides n DragInts side by side."""
    assert len(vec) <= 5 and len(vec) > 0, "input_n takes 1 to 5 components!"
    psim.PushItemWidth(width)
    update = False
    for i in range(len(vec)):
        if i > 0 and i % stride != 0:
            psim.SameLine()
        clicked, vec[i] = psim.InputInt(f"##{name}_{i}", vec[i], step=step)
        if clicked:
            vec[i] = max(min(v_max, vec[i]), v_min)
        update |= clicked
    psim.PopItemWidth()
    psim.SameLine()
    psim.Text(name.split("##")[0])
    return update, vec


def exp_slider(
    name: str,
    val,
    v_min_exp=-5,
    v_max_exp=5,
    v_min: int = 1e-5,
    v_max: int = 1e6,
    item_width: int = 100,
):
    exp = int(np.floor(np.log10(val))) if val != 0.0 else 0
    rel = val / 10**exp
    psim.SetNextItemWidth(item_width)
    update = False
    clicked, rel = psim.SliderFloat(f"{name}_rel", rel, v_min=1.0, v_max=9.99)
    update |= clicked
    psim.SetNextItemWidth(item_width)
    psim.SameLine()
    clicked, exp = psim.SliderInt(f"{name}_exp", exp, v_min=v_min_exp, v_max=v_max_exp)
    update |= clicked
    if update:
        val = max(min(rel * 10**exp, v_max), v_min)
    return clicked, val


def choice_slider(name: str, val: Any, map: Dict[Any, int], imap: Dict[int, Any]):
    assert len(map) == len(imap)
    clicked, tmp_val = psim.SliderInt(
        name,
        map[val],
        v_min=0,
        v_max=len(map) - 1,
        format=f"{val.value if isinstance(val, Enum) else val}",
    )
    if clicked:
        val = imap[tmp_val]
    return clicked, val


def choice_combo(
    name: str, val: Any, fmap: Dict[Any, int], imap: Dict[int, Any], names: List[Any]
):
    clicked, idx = psim.Combo(
        name,
        fmap[val],
        names if isinstance(names[0], str) else [str(x) for x in names],
    )
    if clicked:
        val = imap[idx]
    return clicked, val
