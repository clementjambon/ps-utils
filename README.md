# ps-utils: Utils to build viewers for (almost) anything with Polyscope 🖥️


## Getting started

Make sure to install all the requirements of Polyscope because we'll rebuild a custom version of Polyscope from scratch
```bash
sudo apt install xorg-dev libglu1-mesa-dev freeglut3-dev mesa-common-dev
```

Then, in your favorite environment, just run:
```bash
pip install -r requirements.txt
```

For GPU-only features and examples, install CUDA 11.8 and
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements_gpu.txt
```

## What's included?

### BaseViewer

`BaseViewer` provides a simple backbone to build your own viewer in very few steps. Check out [Examples](#examples) for concrete examples.
`BaseViewer` automatically initializes `polyscope` and callbacks.
Initialize your variables by overriding `post_init(...)`.

Every frame, `BaseViewer` calls the following routines in this order 
* `step(...)` for anything related to training, optimization or simulation
* `gui(...)` for UI
* `draw(...)` to draw or render anything including direct buffer updates


## Examples

Examples can be executed with
```bash
python examples/xxxx_viewer.py
```
All examples override `BaseViewer`.

### UiViewer

`UiViewer` (`examples/ui_viewer.py`) provides additional UI abstractions including buttons, sliders, alert and popup handlers.

### DragViewer

`DragViewer` (`examples/drag_viewer.py`) showchases drag-and-drop features.
When dropped, an image is loaded as a `Thumbnail` via `Thumbnail.from_path(...)`
It can then be displayed with `thumbnail.gui()` in the GUI loop.

NB: Adding a new thumbnail will override a previously existing one if a distinct name isn't specified.

### GizmoViewer

`GizmoViewer` shows how to use various gizmo and key shortcuts.

### TrainingViewer (GPU-only)

`TrainingViewer` trains a small MLP neural field to reconstruct an image while rendering it in real-time.

## TODOS:

* Creating a global UI state that can be stored persistently 
* OpenGL example (both CPU & GPU)