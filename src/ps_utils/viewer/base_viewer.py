from argparse import ArgumentParser, Namespace
import time


import polyscope as ps
import polyscope.imgui as psim

from ps_utils.ui.key_handler import KEY_HANDLER


class BaseViewer:
    """
    Default viewer template with basic abstractions
    """

    def __init__(self) -> None:

        self.pre_init()

        # -----------------------
        # Init polyscope
        # -----------------------

        ps.init()
        self.ps_init()

        # -----------------------
        # Init components
        # -----------------------

        self.post_init()

        # -----------------------
        # Start polyscope
        # -----------------------

        ps.set_user_callback(self.ps_callback)
        ps.set_drop_callback(self.ps_drop_callback)
        ps.show()

    def ps_init(self) -> None:
        """
        Initialize Polyscope
        """
        ps.set_ground_plane_mode("none")
        ps.set_max_fps(120)
        ps.set_window_size(1920, 1080)
        # Anti-aliasing
        ps.set_SSAA_factor(4)
        # Uncomment to prevent polyscope from changing scales (including Gizmo!)
        # ps.set_automatically_compute_scene_extents(False)
        # ps.set_allow_headless_backends(True)

        self.last_time = time.time()

    def pre_init(self) -> None:
        pass

    def post_init(self) -> None:
        pass

    # `ps_callback` is called every frame by polyscope
    def ps_callback(self) -> None:

        # Update fps count
        new_time = time.time()
        self.fps = 1.0 / (new_time - self.last_time)
        self.last_time = new_time

        # Step anything that needs to (e.g., trainer, optimizer)
        self.step()

        # Display gui components
        self.gui()

        # Draw things, including buffer updates
        self.draw()

        # Step the global KeyHandler
        KEY_HANDLER.step()

    def ps_drop_callback(self, input_path: str) -> None:
        pass

    def step(self) -> None:
        pass

    def gui(self) -> None:
        psim.Text(f"fps: {self.fps:.4f};")

    def draw(self) -> None:
        # TODO: give an example with render buffers
        pass
