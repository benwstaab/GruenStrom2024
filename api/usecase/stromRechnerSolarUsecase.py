from api.data import endPoints
from api.data.solarDic import solarDic
from api.tools.converter import intConv, checkZip, getHourFromEpoch, normalizeValues
from api.tools.timeFrameFinder import getTimeFrame
from api.tools.zipToLongLat import getLongLat


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


def getData(zip_code):
    """
    Fetch data from weather API endpoint.

    Returns:
    - list: List of dictionaries containing epoch time and computed efficiency score.
    """
    response = endPoints.stromRechnerWeatherEndPoint(zip_code)

    efficiency_scores = []
    for day in response.get('forecast', {}).get('forecastday', []):
        for hour in day.get('hour', []):
            is_day = hour.get('is_day', 1)
            uv_index = hour.get('uv', 0)
            cloud_cover = hour.get('cloud', 0)
            hour_of_day = getHourFromEpoch(hour.get('time_epoch', 1))
            solar_generation_curve = solarDic[hour_of_day]['solar_generation_curve']
            load_curve = solarDic[hour_of_day]['load_curve']

            if not is_day:
                efficiency_score = 0
            else:
                efficiency_score = 0.95 + 0.05 * uv_index * 0.1
                efficiency_score *= (1 - (cloud_cover*0.7 / 100))

                efficiency_score *= solar_generation_curve
                efficiency_score *= 1 - load_curve/2

            efficiency_scores.append({
                'epochtime': hour.get('time_epoch', 0),
                'value': round(efficiency_score, 2),
                'details': {
                    'cloud': -(cloud_cover*0.7 / 100),
                    'generation': solar_generation_curve,
                    'consumption': -load_curve/2
                }
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
    data = getData(zip_code)

    return getTimeFrame(data, input_data.split, input_data.dur, input_data.take_off)
