import os
import glob
import ast
from functools import partial
from typing import Callable, Set, Optional

import polyscope.imgui as psim

from ps_utils.ui.key_handler import KEY_HANDLER, KEYMAP


def get_next_save_factory(
    default_folder: str, extension: Optional[str], prefix: str = "exported"
) -> Callable[[], str]:
    """
    Create a function that crawls a folder for `{prefix}_{:06d}.{extension}` and returns the next valid path.
    NB: Use `extension` = None for folders.
    """

    def aux(default_folder: str, extension: str, prefix: str = "exported"):
        os.makedirs(default_folder, exist_ok=True)
        all_exported_paths = glob.glob(
            os.path.join(
                default_folder,
                f"{prefix}_*.{extension}" if extension is not None else f"{prefix}_*",
            )
        )
        return os.path.join(
            default_folder,
            (
                f"{prefix}_{len(all_exported_paths):06d}.{extension}"
                if extension is not None
                else f"{prefix}_{len(all_exported_paths):06d}"
            ),
        )

    return partial(
        aux, default_folder=default_folder, extension=extension, prefix=prefix
    )


def parse_int_list(s: str) -> list[int]:
    """
    Safely parse s into a list of ints.
    Raises ValueError if s is not a list of ints.
    DISCLAIMER: this is from ChatGPT
    """
    try:
        val = ast.literal_eval(s)
    except (ValueError, SyntaxError):
        raise ValueError(f"Not a valid Python literal: {s!r}")

    if not isinstance(val, list):
        raise ValueError(f"Expected a list, got {type(val).__name__}")
    if not all(isinstance(x, int) for x in val):
        bad = [x for x in val if not isinstance(x, int)]
        raise ValueError(f"List contains non-int elements: {bad!r}")

    return val


BASIC_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def check_extension(input_path: str, extensions: Set[str] = BASIC_IMAGE_EXTENSIONS):
    extension = os.path.splitext(input_path)[1]
    return extension in BASIC_IMAGE_EXTENSIONS
