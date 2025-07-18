def is_float_or_empty(text: str) -> bool:
    if text == "":
        return True
    try:
        float(text)
        return True
    except ValueError:
        return False


def is_float_and_not_zero(text: str) -> bool:
    try:
        val = float(text)
        if val <= 0:
            return False
        return True
    except ValueError:
        return False
