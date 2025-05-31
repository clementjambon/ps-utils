from collections import defaultdict
from PIL import Image

import numpy as np
import trimesh
import pyrender

import polyscope as ps
import polyscope.imgui as psim

from ps_utils.viewer.base_viewer import BaseViewer

MESH_PATH = "data/bunny.obj"
RENDER_SIZE = 512
LIGHT_INTENSITY = 8.0


class GlViewer(BaseViewer):
    """
    Demo viewer showcasing OpenGL viewer
    NB: a copy is made from GPU -> CPU to update the buffer. This could be improved...
    """

    def reset(self):
        # 1. Load mesh once
        mesh_trimesh = trimesh.load(MESH_PATH)
        self.mesh = pyrender.Mesh.from_trimesh(mesh_trimesh, smooth=False)

        # 2. Create renderer
        self.renderer = pyrender.OffscreenRenderer(RENDER_SIZE, RENDER_SIZE)

    def init_render_buffer(self):

        self.render_buffer_quantity = ps.add_raw_color_alpha_render_image_quantity(
            "render_buffer",
            np.ones((RENDER_SIZE, RENDER_SIZE), dtype=float),
            np.ones((RENDER_SIZE, RENDER_SIZE, 4), dtype=float),
            enabled=True,
            allow_fullscreen_compositing=True,
        )

        self.render_buffer = ps.get_quantity_buffer("render_buffer", "colors")

    def pre_init(self, **kwargs):
        # Initialize renderer and scene
        self.reset()

    def post_init(self, **kwargs):
        # Override resolution to square-shaped
        ps.set_window_size(1080, 1080)
        # Create a render buffer to display the result of optimization
        self.init_render_buffer()

        # 3. Build scene
        self.scene = pyrender.Scene(
            bg_color=[0, 0, 0, 0],
            ambient_light=[0.1, 0.1, 0.1],
        )
        self.scene.add(self.mesh)

        # 3. Prepare camera
        camera_parameters = ps.get_view_camera_parameters()
        cam = pyrender.PerspectiveCamera(
            yfov=np.deg2rad(camera_parameters.get_fov_vertical_deg()),
            aspectRatio=camera_parameters.get_aspect(),
        )

        self.cam_node = self.scene.add(cam, pose=camera_parameters.get_E())

        # 4. Add light
        light = pyrender.DirectionalLight(color=np.ones(3), intensity=LIGHT_INTENSITY)
        self.scene.add(light, pose=camera_parameters.get_E())

    def gui(self):
        # Just calling super to get FPS
        super().gui()

    def draw(self):
        color, depth = self.renderer.render(self.scene, flags=pyrender.RenderFlags.RGBA)
        color = color.astype(float) / 255.0
        color = color.reshape(-1, 4)

        self.render_buffer.update_data_from_host(color)


if __name__ == "__main__":
    GlViewer()
