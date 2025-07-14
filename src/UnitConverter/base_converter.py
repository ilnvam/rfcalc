from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Any
import inspect

class UnitEnum(Enum):
    """Marker interface for unit enums."""
    pass


class BaseConverter(ABC):
    """
    Abstract base class for unit conversion between different units of the same physical quantity.

    This class defines a standard interface and partial implementation for converting values from one unit
    to another via a base unit. Subclasses must define the following:

    - `base_unit`: The canonical unit to which all conversions are first made.
    - `_to_base`: A dictionary mapping each supported unit (except the base unit) to a callable that converts
      a value from that unit to the base unit.
    - `_from_base`: A dictionary mapping each supported unit (except the base unit) to a callable that converts
      a value from the base unit to that unit.

    Conversion Process:
    1. If the source unit is not the base unit, convert the input value to the base unit using `_to_base`.
    2. If the target unit is not the base unit, convert from the base unit to the target unit using `_from_base`.
    3. If source and target units are the same, the value is returned unchanged.

    The `convert` method handles type checking and ensures the conversion functions are called with the
    appropriate parameters, raising informative exceptions when arguments are missing.

    Methods:
        - convert(value, from_unit, to_unit, **kwargs): Convert a numeric value from `from_unit` to `to_unit`.
        - _safe_invoke(func, value, **kwargs): Internal helper to safely call conversion functions with proper arguments.
    """

    @property
    @abstractmethod
    def base_unit(self) -> UnitEnum:
        """
        The base unit for the conversion system.

        This unit serves as the intermediate unit to which all conversions are normalized before
        converting to the target unit.

        Returns:
            UnitEnum: The base unit enumeration member.
        """
        pass

    """
    Dictionary contain the conversion from and to base units.
    key is the target unit and value is the function for conversion.
    """
    @property
    @abstractmethod
    def _to_base(self) -> dict[UnitEnum, Callable[..., float]]:
        """
        Mapping of units to conversion functions converting from the given unit to the base unit.

        Each key is a `UnitEnum` member representing a unit, and the corresponding value is a callable
        that takes the original value and returns the equivalent value in the base unit.

        Returns:
            dict[UnitEnum, Callable[..., float]]: Dictionary of conversion functions to the base unit.
        """
        pass

    @property
    @abstractmethod
    def _from_base(self) -> dict[UnitEnum, Callable[..., float]]:
        """
        Mapping of units to conversion functions converting from the base unit to the given unit.

        Each key is a `UnitEnum` member representing a unit, and the corresponding value is a callable
        that takes a value in the base unit and returns the equivalent value in the target unit.

        Returns:
            dict[UnitEnum, Callable[..., float]]: Dictionary of conversion functions from the base unit.
        """
        pass

    def convert(self, value: float, from_unit: UnitEnum, to_unit: UnitEnum, **kwargs: Any) -> float:
        """
        Convert a numeric value from one unit to another within the unit system.

        This method performs validation of input types, converts the input value to the base unit if needed,
        then converts from the base unit to the target unit. If the source and target units are the same,
        the original value is returned directly.

        Args:
            value (float): The numeric value to convert.
            from_unit (UnitEnum): The unit of the input value.
            to_unit (UnitEnum): The unit to convert the value to.
            **kwargs: Additional keyword arguments passed to the conversion functions.

        Returns:
            float: The converted value in the target unit.

        Raises:
            TypeError: If `value` is not numeric or units are not instances of the unit enumeration.
            KeyError: If a required keyword argument for conversion is missing.
        """

        if not isinstance(value, (int, float)):
            raise TypeError("Value must be a number.")
        if not isinstance(from_unit, self.base_unit.__class__):
            raise TypeError("Invalid source unit.")
        if not isinstance(to_unit, self.base_unit.__class__):
            raise TypeError("Invalid target unit.")

        if from_unit == to_unit:
            return value

        # Convert to base unit
        if from_unit == self.base_unit:
            base_value = value
        else:
            func = self._to_base[from_unit]
            base_value = self._safe_invoke(func, value, **kwargs)

        # Convert from base unit to target unit
        if to_unit == self.base_unit:
            return base_value
        else:
            func = self._from_base[to_unit]
            return self._safe_invoke(func, base_value, **kwargs)

    @staticmethod
    def _safe_invoke(func: Callable[..., float], value: float, **kwargs: Any) -> float:
        """
        Safely invoke a conversion function with the provided value and keyword arguments.

        This method inspects the function signature to verify required arguments are provided,
        applies default values where applicable, and raises informative errors if required arguments
        are missing.

        Args:
            func (Callable[..., float]): The conversion function to call.
            value (float): The primary value to convert.
            **kwargs: Additional keyword arguments to pass to the conversion function.

        Returns:
            float: The result of the conversion function.

        Raises:
            TypeError: If required arguments for the function are missing.
            KeyError: If a required keyword argument key is missing.
        """
        sig = inspect.signature(func)
        try:
            # Attempt to bind the arguments (this checks for missing required params)
            bound_args = sig.bind_partial(value, **kwargs)
            bound_args.apply_defaults()
            return func(value, **kwargs)
        except TypeError as e:
            # Missing positional or keyword arguments
            try:
                bound_args = sig.bind_partial(value, **kwargs)
                bound_args.apply_defaults()
                missing = [
                    name for name, param in sig.parameters.items()
                    if name not in bound_args.arguments and param.default is param.empty
                ]
            #If the re-binding fails (e.g. invalid structure), fallback to "<unknown>"
            except TypeError:
                missing = ["<unknown>"]
            raise TypeError(f"Missing required arguments for conversion: {missing}") from e
        except KeyError as e:
            # Missing a specific key in kwargs access
            missing_key = e.args[0]
            raise KeyError(f"Missing required keyword argument '{missing_key}' for conversion") from e
