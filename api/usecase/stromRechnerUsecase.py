from api.data import endPoints
from api.tools.converter import intConv, checkZip, normalizeValues
from api.tools.timeFrameFinder import getTimeFrame


class Input:
    """Class to handle input validation and initialization."""

    def __init__(self, zip_code, dur, take_off, split):
        """
        Initialize Input object.

        Parameters:
        - zip_code (str): Postal code for fetching data.
        - dur (int): Duration parameter.
        - take_off (int): Take off parameter.
        - split (int): Split parameter.
        """
        self.zip_code = checkZip(zip_code)
        self.dur = intConv(dur, "Duration")
        self.take_off = intConv(take_off, "Take off")
        self.split = intConv(split, "Split Parameter")


def getData(zip_code):
    """
    Fetch data from API endpoint for a given postal code.

    Parameters:
    - zip_code (str): Postal code.

    Returns:
    - list: List of dictionaries containing epoch time and corresponding value.
    """
    response = endPoints.stromRechnerEndPoint(zip_code)

    efficiency_scores = []
    if response and "forecast" in response:
        for hour in response["forecast"]:
            efficiency_scores.append({
                'epochtime': hour.get('epochtime'),
                'value': hour.get("eevalue")
            })

    return efficiency_scores


def execute(zip_code, dur, take_off, split):
    """
    Execute main processing logic.

    Parameters:
    - zip_code (str): Postal code.
    - dur (int): Duration parameter.
    - take_off (int): Take off parameter.
    - split (int): Split parameter.

    Returns:
    - object: Result from getTimeFrame function.
    """
    input_data = Input(zip_code, dur, take_off, split)
    data = getData(input_data.zip_code)

    return getTimeFrame(data, input_data.split, input_data.dur, input_data.take_off)
