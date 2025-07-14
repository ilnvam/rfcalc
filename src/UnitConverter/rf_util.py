from math import log10, tan, radians

def log_20(value):
    """ Log value for voltage and current in 50ohm system """
    return 20 * log10(value)

def inverse_log_20(value):
    """ Inverse Log value for voltage and current in 50ohm system """
    return pow(10,value/20)

def interpolate(freq1: float, amp1: float, freq2: float, amp2: float, target_freq: float) -> float:
    """
    Linearly interpolates the amplitude at a given target frequency
    between two known frequency-amplitude points.

    Args:
        freq1 (float): The first known frequency (Hz).
        amp1 (float): The amplitude at freq1.
        freq2 (float): The second known frequency (Hz).
        amp2 (float): The amplitude at freq2.
        target_freq (float): The frequency at which to interpolate (Hz).

    Returns:
        float: Interpolated amplitude at target_freq.

    Raises:
        TypeError: If any argument is not a real number.
        ValueError: If freq1 and freq2 are the same, which would cause division by zero.
    """
    # ---------- Type checks ----------
    for name, val in {
        "freq1": freq1, "amp1": amp1,
        "freq2": freq2, "amp2": amp2,
        "target_freq": target_freq
    }.items():
        if not isinstance(val, (int, float)):
            raise TypeError(f"{name} must be a number, got {type(val).__name__!s}")

    # ---------- Value checks ----------
    if freq1 <= 0 or freq2 <= 0 or target_freq <= 0:
        raise ValueError("Frequencies must be greater than zero hertz.")
    if freq1 == freq2:
        raise ValueError("freq1 and freq2 must be different for interpolation.")

    lower, upper = sorted((freq1, freq2))
    if not (lower <= target_freq <= upper):
        raise ValueError(f"Target frequency {target_freq} is outside the interpolation range ({lower}–{upper}).")

    # Linear interpolation formula:
    interpolated_amp = amp1 + (amp2 - amp1) * ((target_freq - freq1) / (freq2 - freq1))
    return interpolated_amp

def limit_convert(d1:float, d2:float, l1:float, slope:float) -> float:
    """
    Calculate the limit conversion using the formula:
    l1 + (slope * log10(d1/d2))

    Parameters:
        d1 (float): First distance value. Must be positive.
        d2 (float): Second distance value. Must be positive.
        l1 (float): Limit value at distance d1.
        slope (float): Slope used in the conversion.

    Returns:
        float: Limit value at distance d2.

    Raises:
        ValueError: If d1 or d2 is not a positive number.
        TypeError: If any input is not a float or int.
    """
    for name, value in {'d1': d1, 'd2': d2, 'l1': l1, 'slope': slope}.items():
        if not isinstance(value, (float, int)):
            raise TypeError(f"{name} must be a float or int, got {type(value).__name__}")

    if d1 <= 0:
        raise ValueError("d1 must be a positive number.")
    if d2 <= 0:
        raise ValueError("d2 must be a positive number.")

    return l1 + (slope * log10(d1/d2))

def antenna_eut_distance(beamwidth: float, eut_height: float) -> float:
    """
    Calculate the horizontal distance between an antenna and the Equipment Under Test (EUT)
    based on the antenna's half-power beamwidth and the EUT height.

    The distance is derived using simple trigonometry, assuming the beamwidth forms
    a symmetric cone and the EUT is located at the centerline of the beam.

    Parameters
    ----------
    beamwidth : float
        The half-power beamwidth of the antenna in degrees. Must be a positive number.
    eut_height : float
        The vertical height from the antenna to the EUT in meters. Must be a positive number.

    Returns
    -------
    float
        The required horizontal distance (in meters) between the antenna and the EUT.

    Raises
    ------
    TypeError
        If `beamwidth` or `eut_height` is not a float or int.
    ValueError
        If `beamwidth` or `eut_height` is not positive.
    """
    for name, value in {'beamwidth': beamwidth, 'eut_height': eut_height}.items():
        if not isinstance(value, (float, int)):
            raise TypeError(f"{name} must be a float or int, got {type(value).__name__}")

    if beamwidth <= 0:
        raise ValueError("beamwidth must be a positive number.")
    if eut_height <= 0:
        raise ValueError("eut_height must be a positive number.")

    return eut_height / (2 * tan(radians(beamwidth) / 2))