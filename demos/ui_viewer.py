from ps_utils.viewer.base_viewer import BaseViewer
from ps_utils.ui.buttons import *
from ps_utils.ui.sliders import *
from ps_utils.ui.map_utils import *


RES_VALUES = [2**i for i in range(12)]
RES_MAP, RES_INVMAP = get_list_map(RES_VALUES)

ANIMAL_VALUES = ["cat", "dog", "bunny", "turtle"]
ANIMAL_MAP, ANIMAL_INVMAP = get_list_map(ANIMAL_VALUES)


class UiViewer(BaseViewer):
    """
    Demo viewer showcasing all the pure UI add-ons
    """

    def post_init(self):
        """
        For every slider or button, we need to create a variable to hold its current state
        """
        self.slider_3_values = [0, 1, 2]
        self.exp_slider_value = 2.3e-4
        self.choice_slider_value1 = 32
        self.choice_slider_value2 = "bunny"

    def gui(self):

        if psim.TreeNode("Sliders & co##ui_viewer"):

            clicked, self.slider_3_values = slider_n(
                "Slider3##ui_viewer", self.slider_3_values, v_min=0, v_max=50
            )
            clicked, self.slider_3_values = drag_n(
                "Drag3##ui_viewer", self.slider_3_values, v_min=0, v_max=50
            )
            clicked, self.slider_3_values = input_n(
                "Input3##ui_viewer", self.slider_3_values, v_min=0, v_max=50
            )
            clicked, self.exp_slider_value = exp_slider(
                "Exp Slider##ui_viewer", self.exp_slider_value
            )
            clicked, self.choice_slider_value1 = choice_slider(
                "ChoiceSlider1##ui_viewer",
                self.choice_slider_value1,
                RES_MAP,
                RES_INVMAP,
            )
            clicked, self.choice_slider_value2 = choice_slider(
                "ChoiceSlider2##ui_viewer",
                self.choice_slider_value2,
                ANIMAL_MAP,
                ANIMAL_INVMAP,
            )

            clicked, self.choice_slider_value1 = choice_combo(
                "ChoiceCombo1##ui_viewer",
                self.choice_slider_value1,
                RES_MAP,
                RES_INVMAP,
                RES_VALUES,
            )
            clicked, self.choice_slider_value2 = choice_combo(
                "ChoiceCombo2##ui_viewer",
                self.choice_slider_value2,
                ANIMAL_MAP,
                ANIMAL_INVMAP,
                ANIMAL_VALUES,
            )

            psim.TreePop()


if __name__ == "__main__":
    UiViewer()
