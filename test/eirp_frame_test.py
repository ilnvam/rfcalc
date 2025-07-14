import pytest
import customtkinter as ctk

from UnitConverter.eirp_converter import EIRP
from View.eirp_frame import EIRPFrame

# ---------- Fixtures ---------------------------------------------------------


@pytest.fixture(scope="module")
def tk_root():
    """
    Provide a Tk root for all tests in this module and
    destroy it when the module finishes.
    """
    root = ctk.CTk()          # customtkinter root (inherits from Tk)
    yield root
    root.destroy()


# ---------- Tests ------------------------------------------------------------


def test_valid_conversion(monkeypatch, tk_root):
    """If all numbers are valid, update_result must show the converter result."""
    frame = EIRPFrame(tk_root, "EIRP")

    # Fake the converter so we control the output
    def fake_convert(value, from_u, to_u, distance, slope):
        # sanity‑checks to prove the frame sent the right arguments
        assert value == 10.0
        assert distance == 10.0
        assert slope == 20.0
        assert from_u == EIRP.EIRP_dBm
        assert to_u == EIRP.EIRP_dBm
        return 42.0                # arbitrary deterministic result

    monkeypatch.setattr(frame.conv, "convert", fake_convert)

    # Simulate user input
    frame.from_val.set("10")
    frame.distance.set("10")
    frame.slope.set("20")

    # Trigger calculation
    frame.update_result()

    # The label text is formatted inside update_result:
    assert frame.result_label.cget("text") == "42"


def test_invalid_input_resets_label(tk_root):
    """
    Non‑numeric input in the ‘from’ field should make update_result()
    fall into the first except‑block and set the label to “0.00”.
    """
    frame = EIRPFrame(tk_root, "EIRP")

    frame.from_val.set("not‑a‑number")
    frame.update_result()

    assert frame.result_label.cget("text") == "..."


def test_option_menus_keep_enums_in_sync(tk_root):
    """
    Changing either OptionMenu must update the corresponding enum
    and immediately refresh the result.
    """
    frame = EIRPFrame(tk_root, "EIRP")

    # Pick *any* target unit that exists in your enum
    target_unit_value = next(e.value for e in EIRP if e != EIRP.EIRP_dBm)

    frame._to_option_onchange(target_unit_value)
    assert frame.to_enum_var.value == target_unit_value
