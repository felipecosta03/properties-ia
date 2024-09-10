import pickle
import json
import numpy as np
from datetime import datetime


__locations = None
__data_columns = None
__model = None
__scaler = None

def get_estimated_price(latitude, longitude,rooms, beds, bathrooms, surface_total, surface_covered, created_at,district, type):

    try:
        loc_index = __data_columns.index("district_"+district)
    except:
        loc_index = -1

    try:
        type_index = __data_columns.index("type_"+type)
    except:
        type_index = -1

    yesterday = datetime.fromisoformat(created_at)
    year = yesterday.year
    month = yesterday.month
    day = yesterday.day

    x = np.zeros(len(__data_columns))
    x[0] = latitude
    x[1] = longitude
    x[2] = rooms
    x[3] = beds
    x[4] = bathrooms
    x[5] = surface_total
    x[6] = surface_covered
    x[7] = year
    x[8] = month
    x[9] = day

    if loc_index>=0:
        x[loc_index] = 1

    if type_index >= 0:
        x[type_index] = 1

    x = __scaler.transform([x])
    x = x.reshape(1, -1)

    return np.round(__model.predict([x])[0],2)[0]


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global  __data_columns
    global __locations
    global __scaler

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)

    with open("./artifacts/scaler.sav", "rb") as f:
        __scaler = pickle.load(f)

    global __model
    if __model is None:
        with open('./artifacts/model.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")

def get_location_names():
    return __locations

def get_data_columns():
    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts()
    print(len(__data_columns))
    print(get_estimated_price(-34.546817,	-58.468238,	1.0,	2.0,	1.0,	24.0,	24.0,  "2021-01-01T00:00:00",	"Nuñez",	"APARTMENT"))
