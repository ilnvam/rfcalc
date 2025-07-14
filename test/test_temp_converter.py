import pytest
from UnitConverter.temp_converter import TemperatureConverter, Temperature


conv = TemperatureConverter()

def test_c_to_f():
    x = conv.convert(10,Temperature.CELSIUS,Temperature.FAHRENHEIT)
    assert x == 50.00

def test_c_to_c():
    x = conv.convert(10,Temperature.CELSIUS,Temperature.CELSIUS)
    assert x == 10.00

def test_c_to_k():
    x = conv.convert(10,Temperature.CELSIUS,Temperature.KELVIN)
    assert x == 283.15

def test_f_to_k():
    x = conv.convert(10,Temperature.FAHRENHEIT,Temperature.KELVIN)
    assert round(x,2) == 260.93

def test_f_to_c():
    x = conv.convert(10,Temperature.FAHRENHEIT,Temperature.CELSIUS)
    assert round(x,2) == -12.22

def test_k_to_c():
    x = conv.convert(10,Temperature.KELVIN,Temperature.CELSIUS)
    assert round(x,2) == -263.15

def test_k_to_f():
    x = conv.convert(10,Temperature.KELVIN,Temperature.FAHRENHEIT)
    assert round(x,2) == -441.67

def test_invalid_input():
    with pytest.raises(TypeError):
        x = conv.convert('s',Temperature.CELSIUS,Temperature.FAHRENHEIT)