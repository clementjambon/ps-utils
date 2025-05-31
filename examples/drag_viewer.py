from ps_utils.viewer.base_viewer import BaseViewer
from ps_utils.ui.save_utils import check_extension, BASIC_IMAGE_EXTENSIONS
from ps_utils.ui.image_utils import Thumbnail


class DragViewer(BaseViewer):
    """
    Demo viewer showcasing drag-n-drop and image thumbnails
    """

    def post_init(self, **kwargs):
        self.thumbnail = None

    def gui(self):
        # Just calling super to get FPS
        super().gui()

        if self.thumbnail is not None:
            self.thumbnail.gui()

    def ps_drop_callback(self, input_path):
        # Check valid image extensions
        if check_extension(input_path, BASIC_IMAGE_EXTENSIONS):
            try:
                # Load thumbnail object
                self.thumbnail = Thumbnail.from_path(input_path)
            except Exception as e:
                print(f"Couldn't load image at: {input_path}")
        else:
            print(f"Can only load images with extensions: {BASIC_IMAGE_EXTENSIONS}")


if __name__ == "__main__":
    DragViewer()
