import tkinter as tk
import customtkinter
from UnitConverter.rf_converter import FSUNIT, FieldStrengthConverter


class FieldStrengthFrame(customtkinter.CTkFrame):
    """A frame for converting field strength values with live input validation."""

    def __init__(self, master, title):
        super().__init__(master)

        self.conv = FieldStrengthConverter()
        # Hold the selected enum and set default value
        self.from_enum_var = FSUNIT.DBUV_PER_M
        self.to_enum_var = FSUNIT.DBUV_PER_M

        # ====== Row 0 ======

        # Title label
        self.title_label = customtkinter.CTkLabel(self, text=title)
        self.title_label.cget("font").configure(size=22, weight="bold")
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w", columnspan=3)

        # ====== Row 1 ======

        self.textbox = customtkinter.CTkTextbox(self, width=424, height=122)
        self.textbox.grid(row=1, column=0, padx=12, pady=(10, 5), sticky="ew", columnspan=3)
        self.textbox.insert(
            "0.0",
                   "dBµV/m \t= 20 x Log(V/m) + 120\n" +
                   "dBV/m \t= dBµV/m - 120\n" +
                   "dBW \t= dBm - 30\n"
                   "dBµA/m \t= dBµV/m + 51.5\n" +
                   "dBpT \t= dBµA/m + 2.0\n" +
                   "1 Tesla \t= 10000 Gauss\n" +
                   "1 V/m \t= \u221A(W/m\u00B2 x 377)")
        self.textbox.configure(state="disabled")

        # ====== Row 2 ======

        # Entry + Validation
        self.from_value = tk.StringVar(value="")
        self.from_value.trace_add("write", self.update_result)

        self.from_entry = customtkinter.CTkEntry(
            self,
            textvariable=self.from_value,
        )
        self.from_entry.grid(row=2, column=0, padx=12, pady=(10, 5), sticky="w")

        # Output label
        self.to_label = customtkinter.CTkLabel(
            self,
            text="...",
            fg_color=("#F9F9FA", "#343638"),
            corner_radius=6,
            width=138,
            anchor="w"
        )
        self.to_label.grid(row=2, column=1, padx=(0,12), pady=(10, 5), sticky="w")

        # ====== Row 3 ======

        # Input unit selector
        self.from_option = customtkinter.CTkOptionMenu(
            self,
            values=[name.value for name in FSUNIT],
            command=self._on_from_unit_change
        )
        self.from_option.grid(row=3, column=0, padx=12, pady=(0, 8), sticky="w")

        # Output unit selector
        self.to_option = customtkinter.CTkOptionMenu(
            self,
            values=[name.value for name in FSUNIT],
            command=self._on_to_unit_change
        )
        self.to_option.grid(row=3, column=1, padx=(0,12), pady=(0, 8), sticky="w")

        self.from_option.set(self.from_enum_var.value)
        self.to_option.set(self.to_enum_var.value)

    def update_result(self, *args):
        """Update the result label based on input."""
        try:
            value = float(self.from_value.get())
        except (ValueError, tk.TclError):
            self.to_label.configure(text="...")
            return

        # actual conversion logic
        try:
            result = self.conv.convert(value, self.from_enum_var, self.to_enum_var)
            self.to_label.configure(text=f"{result:.10f}".rstrip("0").rstrip("."))
        except (ValueError,tk.TclError) as e:
            print(e)

    def _on_from_unit_change(self, selected_value: str):
        # without next... we will get a list — but we only want one item, the first (and only) match.
        # equivalent code:
        # for e in Temperature:
        #     if e.value == selected_value:
        #     self.enum_var = e
        #     break
        self.from_enum_var = next(e for e in FSUNIT if e.value == selected_value)
        self.update_result()
        # print(f"From enum: {self.from_enum_var}")

    def _on_to_unit_change(self, selected_value: str):
        self.to_enum_var = next(e for e in FSUNIT if e.value == selected_value)
        self.update_result()
        # print(f"To enum: {self.to_enum_var}")