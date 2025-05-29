from typing import Tuple, Dict, Any
from collections import defaultdict
import os

import polyscope as ps
import polyscope.imgui as psim


# TODO: add all keys
KEYMAP = {
    "space": 32,
    "1": 49,
    "a": 65,
    "b": 66,
    "d": 68,
    "e": 69,
    "f": 70,
    "g": 71,
    "h": 72,
    "i": 73,
    "j": 74,
    "k": 75,
    "m": 77,
    "n": 78,
    "o": 79,
    "p": 80,
    "q": 81,
    "r": 82,
    "s": 83,
    "t": 84,
    "u": 85,
    "y": 89,
    "z": 90,
    "left_arrow": 263,
    "right_arrow": 262,
    "up_arrow": 265,
    "down_arrow": 264,
    "rshift": 344,
    "rctrl": 345,
    "page_up": 266,
    "page_down": 267,
    "enter": 257,
}


class KeyHandler:
    """
    Handle key inputs. For example, `KEY_HANDLER("1")` is true when 1 is pressed.
    NB: Inputs are tracked and only allowed again after `interval` steps.
    To update step counts, make sure to call `step(...)` every frame!

    To prevent key input, call `lock(...)` with a string identifier, and later unlock with `unlock` (or `unlock_all` if necessary).
    """

    def __init__(self, interval: int = 10) -> None:
        self.history = defaultdict(lambda: 0)
        self.interval = interval
        self.lock_set = set()

    # Only return true if it has just been clicked on
    def __call__(self, key: str) -> bool:
        if len(self.lock_set) == 0:
            return bool(self.history[KEYMAP[key]] == self.interval)

    def step(self) -> None:
        for k in self.history:
            if self.history[k] > 0:
                self.history[k] -= 1
            elif psim.GetIO().KeysDown[k]:
                self.history[k] = self.interval

    def lock(self, name: str) -> None:
        self.lock_set.add(name)

    def unlock(self, name: str) -> None:
        if name in self.lock_set:
            self.lock_set.remove(name)
        else:
            print(f"KEY_HANDLER: tried to unlock '{name}' but it isn't there")

    def unlock_all(self) -> None:
        self.lock_set = set()


# Initialize a global key handler
KEY_HANDLER = KeyHandler()
