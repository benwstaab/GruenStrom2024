import datetime
import re


def intConv(data, message: str):
    """
    Converts input data to an integer.

    Parameters:
    - data (any): Data to convert to integer.
    - message (str): Error message prefix for exception.

    Returns:
    - int: Converted integer value.

    Raises:
    - InputParameterException: If data cannot be converted to integer.
    """
    try:
        return int(data)
    except ValueError:
        raise InputParameterException(f"{message} must be an integer")


def checkZip(data):
    """
    Validates if the input data is a valid postal code.

    Parameters:
    - data (str): Input data to validate as a postal code.

    Returns:
    - str: Valid postal code if input passes validation.

    Raises:
    - InputParameterException: If input data is not a valid postal code.
    """
    pattern = re.compile(r'^\d{5}$')

    if not pattern.match(data):
        raise InputParameterException(f"{data} is not a valid postal code")

    postal_code_int = int(data)
    if not (1001 <= postal_code_int <= 99998):
        raise InputParameterException(f"{data} is not a valid postal code")

    return data


def getHourFromEpoch(epoch_time):
    """
    Convert epoch time to hour of the day.

    Parameters:
    - epoch_time (int): Epoch time in seconds.

    Returns:
    - int: Hour of the day (0-23).
    """
    dt = datetime.datetime.utcfromtimestamp(epoch_time)
    return dt.hour


def normalizeValues(data):
    non_zero_values = [entry['value'] for entry in data if entry['value'] != 0]

    if non_zero_values:
        min_value = min(non_zero_values)
        max_value = max(non_zero_values)
    else:
        return data

    for entry in data:
        if entry['value'] != 0:
            entry['value'] = (entry['value'] - min_value) / (max_value - min_value)

    return data


class InputParameterException(Exception):
    pass
