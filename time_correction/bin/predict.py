from datetime import datetime
import sys
import json
from bootstrap import root_dir

from catboost import CatBoostRegressor

from utils.osrm import get_nearest_sync
import asyncio
import pandas as pd

loop = asyncio.get_event_loop()


# Шаблон функци для обработки данных
def process(main_id_locality, lat_s, lon_s, lat_f, lon_f, center_lat, center_lon, eda, eta, dt_s):
    # тут будет код, который будет делать прогноз
    model = CatBoostRegressor()
    model.load_model(root_dir+'/data/model.cbm', 'cbm')

    features = [
        'main_id_locality',  # cat
        'EDA',  # float
        'd_la_cla',
        'd_dla_cla',
        'd_lo_clo',
        'd_dlo_clo',
        'ES',
        'day',
        'hour',
    ]

    df = pd.DataFrame(columns=features)
    df.loc[1] = [main_id_locality,     # main_id_locality
                 eda,                  # EDA
                 lat_s - center_lat,   # d_la_cla
                 lat_f - center_lat,   # d_dla_cla
                 lon_s - center_lon,   # d_lo_clo
                 lon_f - center_lon,   # d_dlo_clo
                 eda / eta,            # ES
                 dt_s.weekday(),       # day
                 dt_s.hour]            # hour

    pred = model.predict(df)
    rta = eta*1+pred
    return rta
    # return get_nearest_sync(lat, lng)


# Читаем данные из аргументов
#main_id_locality, lat_s, lon_s, lat_f, lon_f, center_lat, center_lon, eda, eta, dt_s
main_id_locality =sys.argv[1]
lat_s = sys.argv[2]
lon_s = sys.argv[3]
lat_f = sys.argv[4]
lon_f = sys.argv[5]
center_lat = sys.argv[6]
center_lon = sys.argv[7]
eda = sys.argv[8]
eta = sys.argv[9]
dt_s = sys.argv[10]

try:
    result = process(int(main_id_locality),
                     float(lat_s),
                     float(lon_s),
                     float(lat_f),
                     float(lon_f),
                     float(center_lat),
                     float(center_lon),
                     float(eda),
                     float(eta),
                     datetime.strptime(dt_s, "%Y-%m-%d %H:%M:%S"))
    print(json.dumps({
        "result": result,
        "error": ""
    }))
except Exception as e:
    print(json.dumps({
        "result": [],
        "error": e.args[0]
    }))
