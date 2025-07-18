import customtkinter

from View.beamwidth_frame import BeamwidthFrame
from View.eirp_frame import EIRPFrame
from View.field_strength_frame import FieldStrengthFrame
from View.interpolate_frame import InterpolateFrame
from View.limit_convert_frame import LimitConvertFrame
from View.sidebar_frame import SidebarFrame


class App(customtkinter.CTk):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.title("RF Calculator")
        self.geometry("1130x600")
        customtkinter.set_default_color_theme("blue")
        customtkinter.set_appearance_mode("system")

        # list out all column and row configure for easy edit
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        side_frame = SidebarFrame(self)
        side_frame.grid(row=0, column=0, sticky="nsew", rowspan=4)

        scroll_mainframe = customtkinter.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0
        )
        scroll_mainframe.grid(row=0, column=1, sticky="nsew", rowspan=4)

        # ====== Row 0 ======
        fs_frame = FieldStrengthFrame(scroll_mainframe, "Field Strength Converter")
        fs_frame.grid(row=0, column=1, padx=(10, 0), pady=(10, 0), sticky="nsew")

        e_frame = EIRPFrame(scroll_mainframe, "EIRP Calculator")
        e_frame.grid(row=0, column=2, padx=(10, 0), pady=(10, 0), sticky="nsew")

        # ====== Row 1 ======
        i_frame = InterpolateFrame(scroll_mainframe, "Interpolate")
        i_frame.grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky="nsew")

        l_frame = LimitConvertFrame(scroll_mainframe, "Limit Convert")
        l_frame.grid(row=1, column=2, padx=(10, 0), pady=(10, 0), sticky="nsew")

        # ====== Row 2 ======

        b_frame = BeamwidthFrame(scroll_mainframe, "Antenna to EUT Distance")
        b_frame.grid(row=2, column=1, padx=(10, 0), pady=(10, 10), sticky="nsew")


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
