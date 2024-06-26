from api.tools.converter import intConv, checkZip, normalizeValues
from api.tools.zipToLongLat import getLongLat
from api.usecase import stromRechnerSolarUsecase, stromRechnerUsecase
from api.tools.timeFrameFinder import getTimeFrame


class Input:
    """
    Class to handle input validation and initialization.
    """

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

    # Fetch data from usecases
    data_solar = stromRechnerSolarUsecase.getData(input_data.zip_code)
    data_green = stromRechnerUsecase.getData(input_data.zip_code)

    # Combine and aggregate normalized data
    efficiency_scores = []
    for obj in data_solar:
        obj_green = find_value_by_epochtime(data_green, obj['epochtime'])
        if obj_green is not None:
            obj['details']['GSI'] = obj_green['value'] / 100
            obj['details']['cloud'] *= 0.5
            obj['details']['consumption'] *= 0.5
            obj['details']['generation'] *= 0.5

            efficiency_scores.append({
                'epochtime': obj['epochtime'],
                'value': round(obj['value'] + obj_green['value'] / 100, 2),
                'details': obj['details']
            })

    # Get time frame for aggregated data
    return getTimeFrame(efficiency_scores, input_data.split, input_data.dur, input_data.take_off)


def find_value_by_epochtime(array, target_epochtime):
    for entry in array:
        if entry['epochtime'] == target_epochtime:
            return entry
    return None
