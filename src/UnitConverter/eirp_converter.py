from math import log10, pi
from src.UnitConverter.base_converter import UnitConverter, UnitEnum


class EIRP(UnitEnum):
    EIRP_dBm = "EIRP (dBm)"
    EIRP_mW = "EIRP (mW)"
    ERP_dBm = "ERP (dBm)"
    ERP_mW = "ERP (mW)"
    dbuv_per_m = "dBμV/m"
    dbuv = "dBμV"
    W_m_sq = "W/m\u00B2" # W/(m^2)

def eirp_to_dbuvm(value:float, radius:float, slope:float = 20) -> float:
    """
    Converts EIRP (in dBm) to electric field strength in dBμV/m.

    The conversion is based on the following formula:
        E (dBμV/m) = EIRP (dBm) - slope * log10(radius) + 104.8

    Args:
        value (float): The EIRP value in dBm.
        radius (float): Distance from the source in meters.
        slope (float, optional): Propagation loss slope, typically 20 for far-field conditions.

    Returns:
        float: Electric field strength in dBμV/m.
    """
    return value - slope * log10(radius) + 104.8

def dbuvm_to_eirp(value:float, radius:float, slope:float = 20) -> float:
    """
    Converts electric field strength (dBμV/m) to EIRP (dBm).

    The conversion is based on the inverse of the free-space field strength formula:
        EIRP (dBm) = E (dBμV/m) + slope * log10(radius) - 104.8

    Args:
        value (float): Electric field strength in dBμV/m.
        radius (float): Distance from the source in meters.
        slope (float, optional): Propagation loss slope, typically 20.

    Returns:
        float: EIRP value in dBm.
    """
    return value + slope * log10(radius) - 104.8

def eirp_to_wm2(value:float, distance:float,) -> float:
    """
    Converts EIRP (in dBm) to power flux density (W/m²).

    W/m² = EIRP / 4 * pi * distance²

    Args:
        value (float): EIRP in dBm.
        distance (float): Distance from the source in meters.

    Returns:
        float: Power density in watts per square meter (W/m²).
    """
    return (pow(10, value / 10) / 1e3) / (4 * pi * pow(distance, 2))

class EIRPConverter(UnitConverter):
    """
    A unit converter for Effective Isotropic Radiated Power (EIRP) and related units.

    This class provides bidirectional conversion between different representations
    of radiated power including:

    - EIRP (dBm)
    - EIRP (mW)
    - ERP (dBm)
    - ERP (mW)
    - Field strength (dBμV/m)
    - Voltage level (dBμV)
    - Power flux density (W/m²)

    Conversions involving field strength (dBμV/m) and power flux density (W/m²)
    require additional context such as distance (in meters) and optionally slope (default: 20),
    which corresponds to the propagation loss factor in logarithmic scale.

    The base unit used internally is EIRP in dBm.

    Notes:
        - ERP is assumed to be 2.15 dB less than EIRP.
        - Field strength (dBμV/m) conversions are derived from standard free-space propagation formulas.
        - W/m² is calculated assuming isotropic radiation over a spherical surface area.

    Example:
        >>> c = EIRPConverter()
        >>> c.convert(30, EIRP.EIRP_dBm, EIRP.dbuv_per_m, distance=3.0)
        110.45757490560675

    Raises:
        KeyError: If required keyword arguments (e.g., distance) are missing for certain conversions.
        TypeError: If input types are incorrect or incompatible with conversion logic.

    Properties:
        base_unit (EIRP): The canonical unit for EIRP (dBm) used as the conversion base.
    """

    @property
    def base_unit(self):
        return EIRP.EIRP_dBm

    @property
    def _to_base(self):
        return {
            EIRP.EIRP_mW: lambda x, **kwargs: 10 * log10(x),
            EIRP.ERP_dBm: lambda x, **kwargs: x + 2.15,
            EIRP.ERP_mW: lambda x, **kwargs: 10 * log10(x) + 2.15,
            EIRP.dbuv_per_m: lambda x, **kwargs: dbuvm_to_eirp(x, kwargs["distance"], kwargs["slope"]),
            EIRP.dbuv: lambda x, **kwargs: x - 107,
            EIRP.W_m_sq: lambda x, **kwargs: x * (4 * pi * pow(kwargs["distance"], 2) )
        }

    @property
    def _from_base(self):
        return {
            EIRP.EIRP_mW: lambda x, **kwargs: pow(10, x / 10),
            EIRP.ERP_dBm: lambda x, **kwargs: x - 2.15,
            EIRP.ERP_mW: lambda x, **kwargs: pow(10, ( x - 2.15 ) / 10),
            EIRP.dbuv_per_m: lambda x, **kwargs: eirp_to_dbuvm(x, kwargs["distance"], kwargs["slope"]),
            EIRP.dbuv: lambda x, **kwargs: x + 107,
            EIRP.W_m_sq: lambda x, **kwargs: eirp_to_wm2(x, kwargs["distance"])
        }


if __name__ == "__main__":
    c = EIRPConverter()
    print(c.convert(30, EIRP.EIRP_dBm, EIRP.dbuv_per_m, distance=3.0, slope=20))

    try:
        print(c.convert(30, EIRP.EIRP_dBm, EIRP.EIRP_mW, slope=20))
    except (KeyError, TypeError) as e:
        print(e)
