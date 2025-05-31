import numpy as np

import polyscope as ps

from ps_utils.viewer.base_viewer import BaseViewer

SDF_PATH = "data/bunny_sdf.npy"


class SdfViewer(BaseViewer):
    """
    Demo viewer showcasing Polyscope's native SDF visualization
    """

    def post_init(self, **kwargs):
        # Load SDF grid of dimensions (res, res, res)
        sdf_data = np.load(SDF_PATH)

        # Create the corresponding Polyscope structure
        dims = tuple(sdf_data.shape)
        bound_low = [-1.0] * 3
        bound_high = [1.0] * 3

        ps_grid = ps.register_volume_grid("sample grid", dims, bound_low, bound_high)

        # SDF-extracted mesh
        ps_grid.add_scalar_quantity(
            "mesh",
            sdf_data,
            defined_on="nodes",
            enable_isosurface_viz=True,  # Extracts the mesh corresponding to the SDF
            isosurface_level=0.0,  # Isosurface level (e.g., 0.0 for SDFs)
            slice_planes_affect_isosurface=False,  # Prevent slicing the mesh (i.e., only SDF volume)
            enabled=True,
            isolines_enabled=True,  # Show isolines for the SDF
        )
        # NOTE: most of the parameters above can be controlled directly from the UI!

        # ============
        # SLICE PLANE
        # ============
        slice_plane = ps.add_scene_slice_plane()
        # First tuple is position, second is normal of the gizmo
        slice_plane.set_pose((0.0, 0.0, 0.0), (-1.0, 0.0, 0.0))
        # Add gizmo
        slice_plane.set_draw_widget(True)
        # Uncomment to draw a transparent plane
        # slice_plane.set_draw_plane(True)

    def gui(self):
        # Just calling super to get FPS
        super().gui()


if __name__ == "__main__":
    SdfViewer()
