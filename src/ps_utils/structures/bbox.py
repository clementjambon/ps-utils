import numpy as np
import polyscope as ps

# -----------------------------
# LISTS
# -----------------------------


CUBE_VERTICES_LIST = [
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [1.0, 1.0, 0.0],
    [0.0, 0.0, 1.0],
    [1.0, 0.0, 1.0],
    [0.0, 1.0, 1.0],
    [1.0, 1.0, 1.0],
]

CUBE_EDGES_LIST = [
    (4, 5),
    (5, 7),
    (7, 6),
    (6, 4),
    (0, 1),
    (1, 3),
    (3, 2),
    (2, 0),
    (4, 0),
    (5, 1),
    (7, 3),
    (6, 2),
]

CUBE_TRIANGLES_LIST = [
    (4, 5, 7),
    (7, 6, 4),
    (3, 1, 0),
    (0, 2, 3),
    (1, 7, 5),
    (7, 1, 3),
    (4, 6, 0),
    (0, 6, 2),
    (7, 3, 6),
    (6, 3, 2),
    (4, 0, 5),
    (5, 0, 1),
]


# -----------------------------
# NUMPY
# -----------------------------

CUBE_VERTICES_NP = np.array(CUBE_VERTICES_LIST)
CUBE_EDGES_NP = np.array(CUBE_EDGES_LIST)
CUBE_TRIANGLES_NP = np.array(CUBE_TRIANGLES_LIST)

# -----------------------------
# PS
# -----------------------------


def create_bbox(
    bbox_min=np.array([-1.0, -1.0, -1.0]),
    bbox_max=np.array([1.0, 1.0, 1.0]),
    edge_radius: float = 0.005,
    suffix: str = "",
    enabled: bool = True,
):
    cube_vertices = (bbox_max - bbox_min) * CUBE_VERTICES_NP + bbox_min

    bbox = ps.register_curve_network(
        f"bbox{suffix}",
        cube_vertices,
        CUBE_EDGES_NP,
        enabled=enabled,
        radius=edge_radius,
    )

    return bbox
