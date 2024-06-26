import requests

from api.tools.zipToLongLat import getLongLat

greenIndexURL = "https://gruenstromindex.de/v2.0/"
weatherURL = "http://api.weatherapi.com/v1/"
weatherKey = "d245de62cb2340f587384015242206"


def stromRechnerEndPoint(zip_code: str):
    """
    Fetches green energy prediction data based on zip code.

    Parameters:
    - zip_code (str): Postal code for the location.

    Returns:
    - dict: JSON response data from the API.
    """
    response = requests.get(greenIndexURL + "gsi/prediction", params={"zip": zip_code})
    return request_check(response)


def stromRechnerWeatherEndPoint(zip_code: str):
    """
    Fetches weather forecast data.

    Returns:
    - dict: JSON response data from the API.
    """
    try:
        q = getLongLat(zip_code)
    except Exception:
        q = "auto:ip"

    response = requests.get(weatherURL + "forecast.json", params={"key": weatherKey, "q": q, "days": 3})

    return request_check(response)


def request_check(resp: requests.Response):
    """
    Checks the response status and raises an exception if not OK.

    Parameters:
    - resp (requests.Response): Response object from requests.

    Returns:
    - dict: JSON response data if response is OK.

    Raises:
    - BackendServerException: If response is not OK.
    """
    resp.raise_for_status()
    return resp.json()


class BackendServerException(Exception):
    pass
