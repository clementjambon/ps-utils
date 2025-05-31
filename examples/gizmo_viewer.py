import trimesh
import polyscope as ps
import polyscope.imgui as psim

from ps_utils.viewer.base_viewer import BaseViewer
from ps_utils.viewer.gizmo import (
    ControlMode,
    CONTROL_MODE_TO_PS_TRANSFORM,
    key_control_mode,
    slider_control_mode,
    CONTROL_MODE_KEYMAP,
)

MESH_PATH = "data/bunny.obj"


class GizmoViewer(BaseViewer):
    """
    Demo viewer showcasing gizmos
    """

    def post_init(self, **kwargs):
        # Create a mesh
        mesh = trimesh.load(MESH_PATH)
        self.ps_mesh = ps.register_surface_mesh("mesh", mesh.vertices, mesh.faces)

        # Add a gizmo
        self.control_mode = ControlMode.TRANSLATION_ROTATION
        self.ps_mesh.set_transform_gizmo_enabled(True)
        self.ps_mesh.set_transform_mode_gizmo(
            CONTROL_MODE_TO_PS_TRANSFORM[self.control_mode]
        )

    def gui(self):
        # Just calling super to get FPS
        super().gui()

        psim.SeparatorText("Slider")

        self.control_mode = slider_control_mode(
            "Control", self.ps_mesh, self.control_mode
        )

        psim.SeparatorText("Keys")

        self.control_mode = key_control_mode(self.ps_mesh, self.control_mode)

        for k, mode in CONTROL_MODE_KEYMAP.items():
            psim.Text(f"{k}: {mode.value}")


if __name__ == "__main__":
    GizmoViewer()
