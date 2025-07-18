import math
from typing import Dict, Callable

from src.UnitConverter.base_converter import BaseConverter, UnitEnum
from src.UnitConverter.rf_util import log_20, inverse_log_20


class FSUNIT(UnitEnum):
    """
    Enumeration of supported field strength and electromagnetic units.
    """

    V_PER_M = "V/m"
    UV_PER_M = "μV/m"
    DBUV_PER_M = "dBμV/m"
    DBUA_PER_M = "dBμA/m"
    A_PER_M = "A/m"
    UA_PER_M = "μA/m"
    PT = "pT"
    DBPT = "dBpT"
    Tesla = "Tesla"
    Gauss = "Gauss"
    MW_PER_CM_SQ = "mW/cm\u00b2"  # mW/(cm^2)
    W_PER_M_SQ = "W/m\u00b2"  # W/(m^2)


class FieldStrengthConverter(BaseConverter):
    """
    A unit converter for converting between various field strength and electromagnetic units.

    Inherits from:
        BaseConverter

    Base Unit:
        FSUNIT.DBUV_PER_M (dBμV/m)

    Properties:
        base_unit (UnitEnum): Defines dBμV/m as the canonical base unit.
        _to_base (dict): Dictionary mapping FSUNIT to conversion functions that
                         convert values *to* the base unit.
        _from_base (dict): Dictionary mapping FSUNIT to conversion functions that
                           convert values *from* the base unit.

    Example:
        >>> converter = FieldStrengthConverter()
        >>> converter.convert(1000, FSUNIT.UV_PER_M, FSUNIT.DBUV_PER_M)
        60.0
    """

    @property
    def base_unit(self) -> UnitEnum:
        return FSUNIT.DBUV_PER_M

    @property
    def _to_base(self) -> Dict[UnitEnum, Callable[[float], float]]:
        return {
            FSUNIT.V_PER_M: lambda x: log_20(x) + 120,
            FSUNIT.UV_PER_M: lambda x: log_20(x),
            FSUNIT.DBUA_PER_M: lambda x: x + 51.5,
            FSUNIT.A_PER_M: lambda x: log_20(x * 1e6) + 51.5,
            FSUNIT.UA_PER_M: lambda x: log_20(x) + 51.5,
            FSUNIT.DBPT: lambda x: x + 49.5,
            FSUNIT.PT: lambda x: log_20(x) + 49.5,
            FSUNIT.MW_PER_CM_SQ: lambda x: log_20((math.sqrt(x * 377 * 10)) * 1e6),
            FSUNIT.W_PER_M_SQ: lambda x: log_20((math.sqrt(x * 377)) * 1e6),
            FSUNIT.Tesla: lambda x: log_20(x * 1e12) + 49.5,
            FSUNIT.Gauss: lambda x: log_20(x * 1e8) + 49.5,
        }

    @property
    def _from_base(self) -> Dict[UnitEnum, Callable[[float], float]]:
        return {
            FSUNIT.V_PER_M: lambda x: inverse_log_20(x) / 1e6,
            FSUNIT.UV_PER_M: lambda x: inverse_log_20(x),
            FSUNIT.DBUA_PER_M: lambda x: x - 51.5,
            FSUNIT.A_PER_M: lambda x: inverse_log_20(x - 51.5) / 1e6,
            FSUNIT.UA_PER_M: lambda x: inverse_log_20(x - 51.5),
            FSUNIT.DBPT: lambda x: x - 49.5,
            FSUNIT.PT: lambda x: inverse_log_20(x - 49.5),
            FSUNIT.W_PER_M_SQ: lambda x: pow((inverse_log_20(x) / 1e8), 2)
            / 377
            * 10000,
            FSUNIT.MW_PER_CM_SQ: lambda x: pow((inverse_log_20(x) / 1e8), 2)
            / 377
            * 1000,
            FSUNIT.Tesla: lambda x: inverse_log_20(x - 49.5) / 1e12,
            FSUNIT.Gauss: lambda x: inverse_log_20(x - 49.5) / 1e8,
        }
