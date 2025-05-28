from enum import Enum
from typing import List, Any, Dict

import polyscope.imgui as psim


def get_enum_maps(enum: Enum):
    fmap = {x: i for i, x in enumerate(enum)}
    imap = {i: x for i, x in enumerate(enum)}
    names = [x.value for x in enum]
    inv_names = {x.value: i for i, x in enumerate(enum)}
    return fmap, imap, names, inv_names


def get_list_map(vals: List[Any]):
    fmap = {x: i for i, x in enumerate(vals)}
    imap = {i: x for i, x in enumerate(vals)}
    return fmap, imap


def combo_enum(
    name: str, val: Any, fmap: Dict[Any, int], imap: Dict[int, Any], names: List[str]
):
    clicked, idx = psim.Combo(
        name,
        fmap[val],
        names,
    )
    if clicked:
        val = imap[idx]
    return clicked, val
