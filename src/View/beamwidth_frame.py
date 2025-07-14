import customtkinter
import tkinter as tk
import UnitConverter.rf_util as rf

class BeamwidthFrame(customtkinter.CTkFrame):
    def __init__(self, parent, title):
        super().__init__(parent)

        # ====== Row 0 ======

        # Title label
        self.title_label = customtkinter.CTkLabel(self, text=title)
        self.title_label.cget("font").configure(size=22, weight="bold")
        self.title_label.grid(row=0, column=0, padx=12, pady=(10, 0), sticky="w", columnspan=2)

        # ====== Row 1 ======

        # Beamwidth Label
        self.beamwidth_label = customtkinter.CTkLabel(self, text="3dB Beamwidth (°):")
        self.beamwidth_label.grid(row=1, column=0, padx=12, pady=(10, 0), sticky="w")

        # Beamwidth Entry
        self.beamwidth_val = tk.StringVar(value="0.0")
        self.beamwidth_val.trace_add("write", self.update_result)
        self.beamwidth_entry = customtkinter.CTkEntry(self, textvariable=self.beamwidth_val)
        self.beamwidth_entry.grid(row=1, column=1, padx=12, pady=(10, 0))

        # ====== Row 2 ======

        self.height_label = customtkinter.CTkLabel(self, text="EUT Height (m):")
        self.height_label.grid(row=2, column=0, padx=12, pady=(10, 0), sticky="w")

        self.height_val = tk.StringVar(value="0.0")
        self.height_val.trace_add("write", self.update_result)
        self.height_entry = customtkinter.CTkEntry(self, textvariable=self.height_val)
        self.height_entry.grid(row=2, column=1, padx=12, pady=(10, 0))

        # ====== Row 3 ======

        # Distance Label
        self.distance_label = customtkinter.CTkLabel(self, text="Distance (m):")
        self.distance_label.grid(row=3, column=0, padx=12, pady=(10, 10), sticky="w")

        # Result Label
        self.result_label = customtkinter.CTkLabel(
            self,
            text="...",
            fg_color=("#F9F9FA", "#343638"),
            corner_radius=6,
            width=138,
            anchor="w"
        )
        self.result_label.grid(row=3, column=1, padx=12, pady=(10, 10), sticky="w")


    def update_result(self, *args):

        try:
            if not all([self.height_val.get(), self.beamwidth_val.get()]):
                self.result_label.configure(text="...")
                return

            height = float(self.height_val.get())
            beamwidth = float(self.beamwidth_val.get())

            result = rf.antenna_eut_distance(beamwidth, height)
            self.result_label.configure(text=f"{result:.2f}")

        except (ValueError, TypeError):
            self.result_label.configure(text="...")