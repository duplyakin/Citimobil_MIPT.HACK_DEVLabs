import asyncio
import aiohttp
import json
import polyline

async def get_route(departure, destination):
    lat1, lng1 = departure
    lat2, lng2 = destination
    url = f"http://router.project-osrm.org/route/v1/driving/{lng1},{lat1};{lng2},{lat2}?steps=true"

    async with aiohttp.ClientSession() as session:
        response = await session.request("GET", url=url)
        data = await response.read() if response.status == 200 else None
        tmp = json.loads(data)
        for r in tmp["routes"]:
            r["geometry"]= polyline.decode(r["geometry"])
            for l in r["legs"]:
                for s in l["steps"]:
                    s["geometry"]=  polyline.decode( s["geometry"])

    return tmp


def get_route_sync(departure, destination):
    return asyncio.run(get_route(departure, destination))


async def get_nearest(lat, lng):

    url = f"http://router.project-osrm.org/nearest/v1/driving/{lng},{lat}?number=1"

    async with aiohttp.ClientSession() as session:
        response = await session.request("GET", url=url)
        data = await response.read() if response.status == 200 else None

    return json.loads(data)


def get_nearest_sync(lat, lng):
    return asyncio.run(get_nearest(lat, lng))
