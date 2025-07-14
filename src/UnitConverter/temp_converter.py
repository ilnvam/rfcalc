from enum import auto
from src.UnitConverter.base_converter import UnitConverter, UnitEnum

class Temperature(UnitEnum):
    CELSIUS = auto()
    FAHRENHEIT = auto()
    KELVIN = auto()


class TemperatureConverter(UnitConverter):
    @property
    def base_unit(self):
        return Temperature.CELSIUS

    @property
    def _to_base(self):
        return {
            Temperature.KELVIN: lambda x: x - 273.15,
            Temperature.FAHRENHEIT: lambda x: (x - 32) * 5 / 9,
        }

    @property
    def _from_base(self):
        return {
            Temperature.KELVIN: lambda x: x + 273.15,
            Temperature.FAHRENHEIT: lambda x: x * 9 / 5 + 32,
        }

def main():

    value_to_convert = 30.0
    conv = TemperatureConverter()

    try:
        value_target_unit = conv.convert(value_to_convert, Temperature.CELSIUS, Temperature.FAHRENHEIT)
        print(f"{value_target_unit:0.2f}")
    except TypeError as err:
        print(err)

if __name__ == "__main__":
    main()