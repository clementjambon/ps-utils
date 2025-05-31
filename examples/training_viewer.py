from collections import defaultdict
from PIL import Image

import numpy as np
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms

import polyscope as ps
import polyscope.imgui as psim

from ps_utils.viewer.base_viewer import BaseViewer
from ps_utils.ui.buttons import state_button
from examples.utils.mlp_field import MlpField, normalized_pixel_grid

LR = 1e-3
NUM_ITERATIONS = 1000
IMAGE_PATH = "data/mit.jpg"
DEVICE = "cuda"


class TrainingViewer(BaseViewer):
    """
    Demo viewer showcasing GPU buffers and online training
    """

    def reset(self):
        # Load Image
        image = Image.open(IMAGE_PATH).convert("RGB")  # RGB only!
        self.image = (
            transforms.ToTensor()(image).permute((1, 2, 0)).to(DEVICE)
        )  # Convert to Tensor
        self.height, self.width = self.image.shape[:2]

        # Initialize model and optimizer
        self.model = MlpField(input_dim=2, output_dim=3, pe_freqs=8).to(DEVICE)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=LR)
        self.loss_fn = F.mse_loss
        self.i_step = 0
        self.losses = defaultdict(lambda: [])
        self.optimizing = True

    def init_render_buffer(self):

        self.render_buffer_quantity = ps.add_raw_color_alpha_render_image_quantity(
            "render_buffer",
            np.ones((self.height, self.width), dtype=float),
            np.ones((self.height, self.width, 4), dtype=float),
            enabled=True,
            allow_fullscreen_compositing=True,
        )

        self.render_buffer = ps.get_quantity_buffer("render_buffer", "colors")

    def post_init(self, **kwargs):
        # Override resolution to square-shaped
        ps.set_window_size(1080, 1080)
        # Initialize model and optimizer
        self.reset()
        # Create a render buffer to display the result of optimization
        self.init_render_buffer()

    def step(self):
        if self.optimizing:
            self.optimizing, loss_dict = self.training_step()
            for k, v in loss_dict.items():
                self.losses[k].append(v)

    def gui(self):
        # Just calling super to get FPS
        super().gui()

        psim.Text(f"Iteration: {self.i_step:03d}/{NUM_ITERATIONS:03d}")

        _, self.optimizing = state_button(self.optimizing, "Stop", "Train")

        psim.SameLine()
        if psim.Button("Reset##training_viewer"):
            self.reset()

    @torch.no_grad()
    def draw(self):
        rendered_image = torch.cat(
            [
                self.pred.detach(),
                torch.ones((self.height, self.width, 1), device=DEVICE),
            ],
            dim=-1,
        )
        self.render_buffer.update_data_from_device(rendered_image)

    def training_step(self):
        # Just a safety guard
        if self.i_step >= NUM_ITERATIONS:
            return False, {}

        # Store all individual losses computed at this step, here only one
        loss_dict = {}

        # Sample pixels
        pixel_pos = normalized_pixel_grid(self.height, self.width, device=DEVICE)

        # Infer the predicted color
        self.pred = self.model(pixel_pos)
        # Compute the loss
        loss = self.loss_fn(self.pred, self.image)

        # Backward pass + Step
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        loss_dict["total"] = loss.item()

        self.i_step += 1

        return self.i_step < NUM_ITERATIONS, loss_dict


if __name__ == "__main__":
    TrainingViewer()
