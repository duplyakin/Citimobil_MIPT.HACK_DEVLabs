from bootstrap import root_dir
from aiohttp import web
from concurrent.futures import ProcessPoolExecutor
import asyncio
import sys
import json


executor = ProcessPoolExecutor()
app = web.Application()


def handle_response(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'content-type, authorization'

    return response


async def hello(request):
    return web.Response(text="Hello!")


async def get_result(request):
    # reading request

    main_id_locality = request.rel_url.query['main_id_locality']
    lat_s = request.rel_url.query['lat_s']
    lon_s = request.rel_url.query['lon_s']
    lat_f = request.rel_url.query['lat_f']
    lon_f = request.rel_url.query['lon_f']
    center_lat = request.rel_url.query['center_lat']
    center_lon = request.rel_url.query['center_lon']
    eda = request.rel_url.query['eda']
    eta = request.rel_url.query['eta']
    dt_s = request.rel_url.query['dt_s']
    # Create the subprocess; redirect the standard output into a pipe.
    process = await asyncio.create_subprocess_exec(
        sys.executable, root_dir + "/bin/predict.py", main_id_locality, lat_s, lon_s, lat_f, lon_f, center_lat, center_lon, eda, eta, dt_s,
        stdout=asyncio.subprocess.PIPE)

    # Read one line of output.
    line = await process.stdout.readline()
    result = json.loads(line.decode('ascii').rstrip())

    # Wait for the subprocess exit.
    await process.wait()

    return handle_response(web.json_response(result))


app.add_routes(
    [
        web.get('/', hello),
        web.get('/predict', get_result)
    ]
)

web.run_app(app, port=5000)
