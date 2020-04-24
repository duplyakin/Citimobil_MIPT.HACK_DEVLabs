import sys
import json
from utils.osrm import get_nearest_sync
import asyncio

loop = asyncio.get_event_loop()


# Шаблон функци для обработки данных
def process(lat, lng):
    # тут будет код, который будет делать прогноз
    # пока просто получаем ближайший адрес
    return get_nearest_sync(lat, lng)


# Читаем данные из аргументов
lat = sys.argv[1]
lng = sys.argv[2]

try:
    result = process(lat, lng)
    print(json.dumps({
        "result": result,
        "error": ""
    }))
except Exception as e:
    print(json.dumps({
        "result": [],
        "error": e.args[0]
    }))
