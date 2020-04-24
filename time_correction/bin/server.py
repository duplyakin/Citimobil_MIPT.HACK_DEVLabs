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
    lat = request.rel_url.query['lat']
    lng = request.rel_url.query['lng']

    # Create the subprocess; redirect the standard output into a pipe.
    process = await asyncio.create_subprocess_exec(
        sys.executable, root_dir + "/bin/predict.py", lat, lng,
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
