from ps_utils.viewer.base_viewer import BaseViewer
from ps_utils.ui.buttons import *
from ps_utils.ui.sliders import *
from ps_utils.ui.map_utils import *
from ps_utils.ui.alert_handler import *
from ps_utils.ui.save_utils import *


# =======================
# MAP INITIALIZATION
# =======================

# Given a set of values (e.g., resolutions or animals)
# `get_list_map(...)` returns the corresponding forward and inverse maps
# both required by `choice_slider` and `choice_combo` below.
RES_VALUES = [2**i for i in range(12)]
RES_MAP, RES_INVMAP = get_list_map(RES_VALUES)

ANIMAL_VALUES = ["cat", "dog", "bunny", "turtle"]
ANIMAL_MAP, ANIMAL_INVMAP = get_list_map(ANIMAL_VALUES)

# =======================
# DEMO VIEWER
# =======================


class UiViewer(BaseViewer):
    """
    Demo viewer showcasing all the pure UI add-ons
    """

    def post_init(self):
        """
        For every slider or button, we need to create a variable to hold its current state
        """
        self.state_value = False
        self.slider_3_values = [0, 1, 2]
        self.exp_slider_value = 2.3e-4
        self.choice_slider_value1 = 32
        self.choice_slider_value2 = "bunny"

        # Initialize alert handler (with a red background)
        self.alert_handler = AlertHandler(background_color=(1.0, 0.0, 0.0, 1.0))

        # Initialize save path
        self.save_path = "saved_message.txt"
        self.save_message = "Write a poem here..."

        self.number_popup = 1

    def gui(self):
        # Just calling super to get FPS
        super().gui()

        # ===============
        # Buttons
        # ===============
        if psim.TreeNode("Buttons##ui_viewer"):
            clicked, self.state_value = state_button(self.state_value, "Stop", "Train")
            psim.TreePop()

        # ===============
        # SLIDERS & CO
        # ===============

        if psim.TreeNode("Sliders & co##ui_viewer"):

            psim.SeparatorText("Multi-input sliders")

            clicked, self.slider_3_values = slider_n(
                "Slider3##ui_viewer", self.slider_3_values, v_min=0, v_max=50
            )
            clicked, self.slider_3_values = drag_n(
                "Drag3##ui_viewer", self.slider_3_values, v_min=0, v_max=50
            )
            clicked, self.slider_3_values = input_n(
                "Input3##ui_viewer", self.slider_3_values, v_min=0, v_max=50
            )

            psim.SeparatorText("Exponential Slider")

            clicked, self.exp_slider_value = exp_slider(
                "Exp Slider##ui_viewer", self.exp_slider_value
            )

            psim.SeparatorText("Choice Components")

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

        # ===============
        # ALERTS & POPUPS
        # ===============

        if psim.TreeNode("Alerts & Popups##ui_viewer"):

            psim.SeparatorText("Alerts")

            # Create an alert
            if psim.Button("Message 1"):
                self.alert_handler.trigger("ALERT")
            psim.SameLine()
            if psim.Button("Message 2"):
                self.alert_handler.trigger("WARNING")
            psim.SameLine()
            if psim.Button("Message 3"):
                self.alert_handler.trigger("CHILL")

            psim.SeparatorText("Save")

            clicked, self.save_path = save_popup(
                "Save##ui_viewer",
                self.save_path,
                save_label="Save Message",
                confirm_label="Are you sure?",
            )
            if clicked:
                try:
                    with open(self.save_path, "w") as f:
                        f.write(self.save_message)
                except Exception as e:
                    self.alert_handler.trigger(
                        f"Could not save the message at: {self.save_path}"
                    )
            _, self.save_message = psim.InputText(
                "Message##ui_viewer", self.save_message
            )

            clicked, self.number_popup = int_popup(
                "Number Popup##ui_viewer",
                self.number_popup,
                button_label="Choose a Number",
            )

            psim.TreePop()

        # Make sure to call the alert handler so that it can trigger an alert
        self.alert_handler.gui()


if __name__ == "__main__":
    UiViewer()
