import polyscope as ps
import polyscope.imgui as psim


class AlertHandler:
    """
    Enables easy alert to be pushed to screen (e.g., when something goes wrong).
    Call `trigger` to display a message. Make sure `gui` is called from your gui.
    """

    def __init__(
        self, popup_name: str = "Alert Popup", background_color: str | None = None
    ) -> None:
        self.popup_name = popup_name
        self.message = ""
        self.show_alert = False
        self.background_color = background_color

    def gui(self) -> None:
        if self.show_alert:
            psim.OpenPopup(self.popup_name)
            self.show_alert = False

        if self.background_color is not None:
            psim.PushStyleColor(psim.ImGuiCol_PopupBg, self.background_color)

        # Ckpt mismatch alert
        if psim.BeginPopup(self.popup_name):

            psim.Text(self.message)
            if psim.Button("Close##viewer"):
                self.show_alert = False
                psim.CloseCurrentPopup()

            psim.EndPopup()

        if self.background_color is not None:
            psim.PopStyleColor()

    def trigger(self, message: str) -> None:
        self.message = message
        self.show_alert = True
