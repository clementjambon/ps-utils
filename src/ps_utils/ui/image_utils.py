from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Tuple
from PIL import Image

import numpy as np
import polyscope as ps

DEFAULT_MAX_PREVIEW_SIZE = 250


@dataclass
class Thumbnail:

    image: Image.Image
    image_preview: np.ndarray
    preview_quantity: Any
    preview_size: Tuple[int, int]

    def gui(self):
        # Simply display the corresponding quantity at the requested size
        self.preview_quantity.imgui_image(self.preview_size[1], self.preview_size[0])

    @staticmethod
    def from_PIL(
        image: Image.Image,
        name: str = "thumbnail",
        max_preview_h: int = DEFAULT_MAX_PREVIEW_SIZE,
        max_preview_w: int = DEFAULT_MAX_PREVIEW_SIZE,
    ):
        # ==========
        # PROCESS
        # ==========
        image_preview = np.array(image).astype(np.float32) / 255.0
        if image_preview.shape[2] == 3:
            image_preview = np.concatenate(
                [
                    image_preview,
                    np.ones(
                        (
                            image_preview.shape[0],
                            image_preview.shape[1],
                            1,
                        ),
                        dtype=np.float32,
                    ),
                ],
                axis=-1,
            )
        preview_quantity = ps.add_color_alpha_image_quantity(
            f"{name}_buffer",
            image_preview,
        )
        h, w = image_preview.shape[:2]
        aspect_ratio = float(h) / float(w)

        clipped_h, clipped_w = min(h, max_preview_h), min(w, max_preview_w)
        preview_size = (
            int(min(clipped_h, clipped_w * aspect_ratio)),
            int(min(clipped_w, clipped_h / aspect_ratio)),
        )

        return Thumbnail(
            image=image,
            image_preview=image_preview,
            preview_quantity=preview_quantity,
            preview_size=preview_size,
        )

    @staticmethod
    def from_path(
        input_path: str,
        name: str = "thumbnail",
        max_preview_h: int = DEFAULT_MAX_PREVIEW_SIZE,
        max_preview_w: int = DEFAULT_MAX_PREVIEW_SIZE,
    ) -> Thumbnail:
        # ==========
        # LOAD
        # ==========
        image = Image.open(input_path)

        return Thumbnail.from_PIL(
            image, name=name, max_preview_h=max_preview_h, max_preview_w=max_preview_w
        )


def load_image(self, path: str):
    # ==========
    # IMAGE
    # ==========
    self.image = Image.open(path)

    # ==========
    # THUMBNAIL
    # ==========
    self.image_preview = np.array(self.image).astype(np.float32) / 255.0
    if self.image_preview.shape[2] == 3:
        self.image_preview = np.concatenate(
            [
                self.image_preview,
                np.ones(
                    (
                        self.image_preview.shape[0],
                        self.image_preview.shape[1],
                        1,
                    ),
                    dtype=np.float32,
                ),
            ],
            axis=-1,
        )
    self.preview_quantity = ps.add_color_alpha_image_quantity(
        f"preview_buffer",
        self.image_preview,
    )
    h, w = self.image_preview.shape[:2]
    aspect_ratio = float(h) / float(w)
    MAX_PREVIEW_SIZE = 250
    clipped_h, clipped_w = min(h, MAX_PREVIEW_SIZE), min(w, MAX_PREVIEW_SIZE)
    self.preview_size = (
        int(min(clipped_h, clipped_w * aspect_ratio)),
        int(min(clipped_w, clipped_h / aspect_ratio)),
    )
