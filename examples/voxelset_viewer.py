import numpy as np

import polyscope.imgui as psim

from ps_utils.viewer.base_viewer import BaseViewer
from ps_utils.structures import VoxelSet

VOXEL_PATH = "data/bunny_voxels.npy"
VOXEL_RES = 32


class SdfViewer(BaseViewer):
    """
    Demo viewer showcasing Polyscope's native SDF visualization
    """

    def post_init(self, **kwargs):
        # Load voxel coordinates
        voxel_coords = np.load(VOXEL_PATH)

        # Create a voxel set
        self.voxel_set = VoxelSet(voxel_coords, VOXEL_RES, -1.0, 1.0)

    def gui(self):
        # Just calling super to get FPS
        super().gui()

        psim.Text("Press `Alt` to add/remove voxels from the selection.")
        psim.Text(
            "Maintain `Alt` pressed and scroll to change the radius of the selection."
        )

        self.voxel_set.gui()


if __name__ == "__main__":
    SdfViewer()
