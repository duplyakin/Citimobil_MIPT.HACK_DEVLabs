from utils.osrm import get_nearest_sync, get_route_sync
import json

departure = [55.752289, 37.592289]
destination = [55.836469, 37.659025]

route = get_route_sync(departure, destination)
print(json.dumps(route, ensure_ascii=False,indent=2))

nearest = get_nearest_sync(*departure)
print(json.dumps(nearest, ensure_ascii=False,indent=2))

pass