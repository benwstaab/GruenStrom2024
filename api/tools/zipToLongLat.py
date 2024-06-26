from api.data.locationDic import location_dic


def getLongLat(zip_code):
    for loc in location_dic:
        if loc[2] == zip_code:
            return str(loc[4]) + "," + str(loc[5])
    raise NoPostalCode


class NoPostalCode(Exception):
    pass
