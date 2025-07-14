import tkinter as tk
import customtkinter
from UnitConverter import rf_util as rf


class InterpolateFrame(customtkinter.CTkFrame):

    def __init__(self, parent, title):
        super().__init__(parent)

        # ====== Row 0 ======

        # Title label
        self.title_label = customtkinter.CTkLabel(self, text=title)
        self.title_label.cget("font").configure(size=22, weight="bold")
        self.title_label.grid(row=0, column=0, padx=12, pady=(10, 0), sticky="w", columnspan=3)

        # ====== Row 1 ======

        self.freq_label = customtkinter.CTkLabel(self, text="Frequency")
        self.freq_label.grid(row=1, column=1, padx=12, pady=(10, 0))

        self.amplitude_label = customtkinter.CTkLabel(self, text="Amplitude")
        self.amplitude_label.grid(row=1, column=2, padx=12, pady=(10, 0))

        # ====== Row 2 ======

        self.start_label = customtkinter.CTkLabel(self, text="Start")
        self.start_label.grid(row=2, column=0, padx=12, pady=(10, 0))

        self.start_freq_val = tk.StringVar(value="")
        self.start_freq_val.trace_add("write", self.update_result)

        self.start_freq_entry = customtkinter.CTkEntry(
            self,
            textvariable=self.start_freq_val,
            )
        self.start_freq_entry.grid(row=2, column=1, padx=12, pady=(10, 0))

        self.start_amp_val = tk.StringVar(value="")
        self.start_amp_val.trace_add("write", self.update_result)

        self.start_amp_entry = customtkinter.CTkEntry(
            self,
            textvariable=self.start_amp_val
        )
        self.start_amp_entry.grid(row=2, column=2, padx=(0,12), pady=(10, 0))

        # ====== Row 3 ======

        self.stop_label = customtkinter.CTkLabel(self, text="Stop")
        self.stop_label.grid(row=3, column=0, padx=12, pady=(10, 0))

        self.stop_freq_val = tk.StringVar(value="")
        self.stop_freq_val.trace_add("write", self.update_result)

        self.stop_freq_entry = customtkinter.CTkEntry(
            self,
            textvariable=self.stop_freq_val
        )
        self.stop_freq_entry.grid(row=3, column=1, padx=12, pady=(10, 0))

        self.stop_amp_val = tk.StringVar(value="")
        self.stop_amp_val.trace_add("write", self.update_result)

        self.stop_amp_entry = customtkinter.CTkEntry(
            self,
            textvariable=self.stop_amp_val
        )
        self.stop_amp_entry.grid(row=3, column=2, padx=(0,12), pady=(10, 0))

        # ====== Row 4 ======

        self.target_label = customtkinter.CTkLabel(self, text="Target")
        self.target_label.grid(row=4, column=0, padx=12, pady=(10, 0))

        self.target_freq_val = tk.StringVar(value="")
        self.target_freq_val.trace_add("write", self.update_result)

        self.target_freq_entry = customtkinter.CTkEntry(
            self,
            textvariable=self.target_freq_val
        )
        self.target_freq_entry.grid(row=4, column=1, padx=12, pady=(10, 0))

        self.target_amp_label = customtkinter.CTkLabel(
            self,
            text="...",
            fg_color=("#F9F9FA", "#343638"),
            corner_radius=6,
            width=138,
            anchor="w"
        )
        self.target_amp_label.grid(row=4, column=2, padx=(0,12), pady=(10, 0), sticky="w")

    def update_result(self, *args):
        try:
            # Extract and validate all values

            if not all([self.start_freq_val.get(),
                        self.start_amp_val.get(),
                        self.stop_amp_val.get(),
                        self.stop_freq_val.get(),
                        self.target_freq_val.get()]):
                self.target_amp_label.configure(text="...")
                return

            freq1 = float(self.start_freq_val.get())
            amp1 = float(self.start_amp_val.get())
            freq2 = float(self.stop_freq_val.get())
            amp2 = float(self.stop_amp_val.get())
            target_freq = float(self.target_freq_val.get())

            # Interpolate
            result = rf.interpolate(freq1, amp1, freq2, amp2, target_freq)
            self.target_amp_label.configure(text=f"{result:.2f}")

        except ValueError:
            # Catch ValueError for empty/invalid conversions or negative/zero freq
            self.target_amp_label.configure(text="Invalid")
        except TypeError:
            # If any input is not a float
            self.target_amp_label.configure(text="Invalid")
        except Exception as e:
            # For other unexpected errors
            self.target_amp_label.configure(text="Error")
            print(f"Interpolation error: {e}")