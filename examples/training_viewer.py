from collections import defaultdict
from PIL import Image
from argparse import ArgumentParser

import numpy as np
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms

import polyscope as ps
import polyscope.imgui as psim

from ps_utils.viewer.base_viewer import BaseViewer
from ps_utils.ui.buttons import state_button
from ps_utils.ui.image_utils import Thumbnail
from examples.utils.mlp_field import MlpField, normalized_pixel_grid

LR = 5e-3
NUM_ITERATIONS = 2500


class TrainingViewer(BaseViewer):
    """
    Demo viewer showcasing GPU buffers and online training
    """

    def reset(self):
        # Load Image
        image = Image.open(self.image_path).convert("RGB")  # RGB only!
        self.image = (
            transforms.Compose(
                [
                    transforms.ToTensor(),
                    transforms.CenterCrop(min(image.width, image.height)),
                    transforms.Resize((self.res, self.res)),
                ]
            )(image)
            .permute((1, 2, 0))
            .to(self.device)
        )  # Convert to Tensor
        self.height, self.width = self.image.shape[:2]

        # Create a GUI thumbnail
        self.thumbnail = Thumbnail.from_PIL(image)

        # Initialize model and optimizer
        self.model = MlpField(
            input_dim=2, output_dim=3, pe_freqs=8, num_layers=2, hidden_dim=64
        ).to(self.device)
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

    def pre_init(self, device="cpu", res=256, image_path="data/mit.jpg", **kwargs):
        self.device = device
        self.res = res
        self.image_path = image_path

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

        psim.SeparatorText("Optimization")

        psim.Text(f"Iteration: {self.i_step:03d}/{NUM_ITERATIONS:03d}")

        _, self.optimizing = state_button(self.optimizing, "Stop", "Train")

        psim.SameLine()
        if psim.Button("Reset##training_viewer"):
            self.reset()

        psim.SeparatorText("Target Image")

        self.thumbnail.gui()

    @torch.no_grad()
    def draw(self):
        rendered_image = torch.cat(
            [
                self.pred.detach(),
                torch.ones((self.height, self.width, 1), device=self.device),
            ],
            dim=-1,
        )
        if self.device == "cpu":
            self.render_buffer.update_data_from_host(rendered_image.reshape(-1, 4))
        else:
            self.render_buffer.update_data_from_device(rendered_image)

    def training_step(self):
        # Just a safety guard
        if self.i_step >= NUM_ITERATIONS:
            return False, {}

        # Store all individual losses computed at this step, here only one
        loss_dict = {}

        # Sample pixels
        pixel_pos = normalized_pixel_grid(self.height, self.width, device=self.device)

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
    parser = ArgumentParser()
    parser.add_argument("--device", type=str, choices=["cpu", "cuda"], default="cpu")
    parser.add_argument("--res", type=int, default=256)
    parser.add_argument("--image", type=str, default="data/mit.jpg")

    args = parser.parse_args()

    TrainingViewer(device=args.device, res=args.res, image_path=args.image)
