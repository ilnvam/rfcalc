import tkinter as tk

import customtkinter

from UnitConverter.eirp_converter import EIRPConverter, EIRP


class EIRPFrame(customtkinter.CTkFrame):

    def __init__(self, parent, title):
        super().__init__(parent)

        self.conv = EIRPConverter()
        self.from_enum_var = EIRP.dbuv_per_m
        self.to_enum_var = EIRP.EIRP_dBm

        # ====== Row 0 ======

        # Title label
        self.title_label = customtkinter.CTkLabel(self, text=title)
        self.title_label.cget("font").configure(size=22, weight="bold")
        self.title_label.grid(
            row=0, column=0, padx=12, pady=(10, 0), sticky="w", columnspan=3
        )

        # ====== Row 1 ======

        self.textbox = customtkinter.CTkTextbox(self, width=424, height=100)
        self.textbox.grid(
            row=1, column=0, padx=12, pady=(10, 0), sticky="w", columnspan=3
        )
        self.textbox.insert(
            "0.0",
            "E[dBµV/m] \t= EIRP[dBm] - 20Log(d[m]) + 10Log(50\u2126/4\u03c0)\n"
            + "E[dBµV/m] \t= EIRP[dBm] - 20Log(d[m]) + 104.8\n\n"
            + "P[W/m\u00b2] \t= EIRP / (4\u03c0 x d[m]\u00b2) \n"
            + "EIRP \t= dBuV + 107.0",
        )
        self.textbox.configure(state="disabled")

        # ====== Row 2 ======

        # Distance Label
        self.distance_label = customtkinter.CTkLabel(self, text="Distance (m):")
        self.distance_label.grid(row=2, column=0, padx=12, pady=4, sticky="w")

        self.distance = tk.StringVar(value="10.0")
        self.distance.trace_add("write", self.update_result)

        # Distance Entry
        self.distance_entry = customtkinter.CTkEntry(
            self,
            textvariable=self.distance,
        )
        self.distance_entry.grid(row=2, column=1, padx=12, pady=4)

        # ====== Row 3 ======

        # Slope label
        self.slope_label = customtkinter.CTkLabel(self, text="Slope (dB/decade):")
        self.slope_label.grid(row=3, column=0, padx=12, pady=4, sticky="w")

        # Slope Entry
        self.slope = tk.StringVar(value="20.0")
        self.slope.trace_add("write", self.update_result)
        self.slope_entry = customtkinter.CTkEntry(
            self,
            textvariable=self.slope,
        )
        self.slope_entry.grid(row=3, column=1, padx=12, pady=4)

        # ====== Row 4 ======

        # 'Convert from' label
        self.from_label = customtkinter.CTkLabel(self, text="Convert from:")
        self.from_label.grid(row=4, column=0, padx=12, pady=4, sticky="w", columnspan=2)

        # 'Convert from' Entry
        self.from_val = tk.StringVar(value="0.0")
        self.from_val.trace_add("write", self.update_result)
        self.from_entry = customtkinter.CTkEntry(
            self,
            textvariable=self.from_val,
        )
        self.from_entry.grid(row=4, column=1, padx=12, pady=4)

        # 'Convert from' option menu
        self.from_option = customtkinter.CTkOptionMenu(
            self,
            values=[name.value for name in EIRP],
            command=self._from_option_onchange,
        )
        self.from_option.grid(row=4, column=2, padx=(0, 12), pady=4)

        # ====== Row 5 ======

        # 'Convert to' label
        self.to_label = customtkinter.CTkLabel(self, text="Convert to:")
        self.to_label.grid(row=5, column=0, padx=12, pady=4, sticky="w")

        # Result Label
        self.result_label = customtkinter.CTkLabel(
            self,
            text="...",
            fg_color=("#F9F9FA", "#343638"),
            corner_radius=6,
            width=138,
            anchor="w",
        )
        self.result_label.grid(row=5, column=1, padx=0, pady=(4, 8))

        # 'Convert to' Option menu
        self.to_option = customtkinter.CTkOptionMenu(
            self, values=[name.value for name in EIRP], command=self._to_option_onchange
        )
        self.to_option.grid(row=5, column=2, padx=(0, 12), pady=(4, 10))

        self.from_option.set(self.from_enum_var.value)
        self.to_option.set(self.to_enum_var.value)

    def update_result(self, *args):
        try:
            value = float(self.from_entry.get())

            result = self.conv.convert(
                value,
                self.from_enum_var,
                self.to_enum_var,
                distance=float(self.distance.get()),
                slope=float(self.slope.get()),
            )

            self.result_label.configure(text=f"{result:.10f}".rstrip("0").rstrip("."))

        except (ValueError, tk.TclError):
            self.result_label.configure(text="...")

    def _from_option_onchange(self, selected_value: str):
        self.from_enum_var = next(e for e in EIRP if e.value == selected_value)
        self.update_result()

    def _to_option_onchange(self, selected_value: str):
        self.to_enum_var = next(e for e in EIRP if e.value == selected_value)
        self.update_result()
