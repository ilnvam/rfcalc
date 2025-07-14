import tkinter as tk
import customtkinter
from UnitConverter import rf_util as rf


class LimitConvertFrame(customtkinter.CTkFrame):

    def __init__(self, parent, title):
        super().__init__(parent)

        # ====== Row 0 ======

        # Title label
        self.title_label = customtkinter.CTkLabel(self, text=title)
        self.title_label.cget("font").configure(size=22, weight="bold")
        self.title_label.grid(row=0, column=0, padx=12, pady=(10, 0), sticky="w", columnspan=2)

        # ====== Row 1 ======

        self.slope_val = tk.IntVar(value=20)
        self.radio20 = customtkinter.CTkRadioButton(
            self,
            text="20 dB/decade",
            variable=self.slope_val,
            command=self.on_radiobutton_change,
            value=20
        )

        self.radio40 = customtkinter.CTkRadioButton(
            self,
            text="40 dB/decade",
            variable=self.slope_val,
            command=self.on_radiobutton_change,
            value=40
        )

        self.radio20.grid(row=1, column=0, padx=12, pady=(10, 0), sticky="w")
        self.radio40.grid(row=1, column=1, padx=12, pady=(10, 0), sticky="w")

        # ====== Row 2 ======

        self.d1_label = customtkinter.CTkLabel(self, text="d1 (m):")
        self.d1_label.grid(row=2, column=0, padx=12, pady=(10, 0), sticky="w")

        self.d1_val = tk.StringVar(value="")
        self.d1_val.trace_add("write", self.update_result)

        self.d1_entry = customtkinter.CTkEntry(
            self,
            textvariable=self.d1_val,
        )
        self.d1_entry.grid(row=2, column=1, padx=12, pady=(10, 0))

        # ====== Row 3 ======

        self.d2_label = customtkinter.CTkLabel(self, text="d2 (m):")
        self.d2_label.grid(row=3, column=0, padx=12, pady=(10, 0), sticky="w")

        self.d2_val = tk.StringVar(value="")
        self.d2_val.trace_add("write", self.update_result)

        self.d2_entry = customtkinter.CTkEntry(
            self,
            textvariable=self.d2_val,
        )
        self.d2_entry.grid(row=3, column=1, padx=12, pady=(10, 0))

        # ====== Row 4 ======

        self.l1_label = customtkinter.CTkLabel(self, text="limit at d1:")
        self.l1_label.grid(row=4, column=0, padx=12, pady=(10, 0), sticky="w")

        self.l1_val = tk.StringVar(value="")
        self.l1_val.trace_add("write", self.update_result)

        self.l1_entry = customtkinter.CTkEntry(
            self,
            textvariable=self.l1_val,
        )
        self.l1_entry.grid(row=4, column=1, padx=12, pady=(10, 0))

        # ====== Row 5 ======

        self.l2_label = customtkinter.CTkLabel(self, text="limit at d2:")
        self.l2_label.grid(row=5, column=0, padx=12, pady=(10, 0), sticky="w")

        self.result_label = customtkinter.CTkLabel(
            self,
            text="...",
            fg_color=("#F9F9FA", "#343638"),
            corner_radius=6,
            width=138,
            anchor="w"
        )
        self.result_label.grid(row=5, column=1, padx=12, pady=(10, 10), sticky="w")

    def update_result(self, *args):

        try:
            if not all([self.d1_val.get(), self.d2_val.get(), self.l1_val.get()]):
                self.result_label.configure(text="...")
                return

            d1 = float(self.d1_val.get())
            d2 = float(self.d2_val.get())
            l1 = float(self.l1_val.get())
            slope = float(self.slope_val.get())

            result = rf.limit_convert(d1, d2, l1, slope)
            self.result_label.configure(text=f"{result:.2f}")

        except (ValueError, TypeError):
            self.result_label.configure(text="...")

    def on_radiobutton_change(self):
        self.update_result()