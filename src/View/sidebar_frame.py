import customtkinter


class SidebarFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(corner_radius=0)
        self.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self,
            text="RF Calculator",
            font=customtkinter.CTkFont(size=26, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(
            self, text="Appearance Mode:", anchor="w"
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(
            self,
            values=["System", "Dark", "Light"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_option_menu.grid(row=6, column=0, padx=10, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(
            self, text="UI Scaling:", anchor="w"
        )
        self.scaling_label.grid(row=7, column=0, padx=10, pady=(10, 0))
        self.scaling_option_menu = customtkinter.CTkOptionMenu(
            self,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_option_menu.grid(row=8, column=0, padx=10, pady=(10, 20))
        self.scaling_option_menu.set("100%")

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    @staticmethod
    def change_scaling_event(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
