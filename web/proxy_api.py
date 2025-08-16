import math
import requests

from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd

BASE_URL = "https://www.cavelink.com/cl/da.php"

app = FastAPI()

app.mount("/static", StaticFiles(directory="ui"), name="static")


@app.get("/")
def serve_ui():
    print("Serving index.html")
    return FileResponse("ui/index.html", media_type="text/html")


@app.get("/cave-link-proxy")
async def read_cave_link_proxy(
    station: str, variable: str, start: str, end: str | None = None
):
    """
    Proxy endpoint to fetch data from the Cave-Link API.
    This endpoint fetches data returns it in JSON format.
    """
    start_date = pd.Timestamp(start, tz="Europe/Zurich")
    end_date = pd.Timestamp(end, tz="Europe/Zurich") if end else None
    params = translate_query_params(station, variable, start_date)

    print(f"Doing GET request to {BASE_URL} with params: {params}")
    cl_response = requests.get(BASE_URL, params=params)

    data = parse_cl_response(cl_response.text, start_date, end_date)

    response = JSONResponse(
        content=data,
        status_code=200,
    )
    return response


def translate_query_params(station: str, variable: str, start: pd.Timestamp) -> dict:
    nb_days = math.ceil((pd.Timestamp.now(tz="Europe/Zurich") - start).days) + 1
    params = {}
    match station:
        case "motiers":
            params["s"] = 106
            match variable:
                case "batterie":
                    params["g"] = 0
                    params["w"] = 0
                    params["l"] = nb_days * 12
                case "waterLevel":
                    params["g"] = 1
                    params["w"] = 101
                    params["l"] = nb_days * 48
                case "waterTemperature":
                    params["g"] = 1
                    params["w"] = 0
                    params["l"] = nb_days * 48
    return params


def parse_cl_response(
    content: str, start: pd.Timestamp, end: pd.Timestamp | None = None
) -> dict:
    """
    Parse the Cave-Link response content into a dictionary.
    """
    lines = content.strip().split("<br>")

    metadata = lines[:2]

    keys, values = zip(*[(row.split(",", 1)) for row in lines[2:] if row.strip()])
    timestamps = [parse_custom_datetime(dt) for dt in keys]
    dataframe = pd.DataFrame({"timestamp": keys, "value": values}, index=timestamps)

    dataframe = dataframe[dataframe.index.floor("d") >= start]
    if end:
        dataframe = dataframe[dataframe.index.floor("d") <= end]

    return {"metadata": metadata, "data": dataframe.to_dict(orient="list")}

def parse_custom_datetime(date_str: str) -> pd.Timestamp:
    """
    Parse from custom Cave-Link date format to a pandas Timestamp
    """
    date, time = date_str.split(" ")
    d, m, y = date.split(".")
    h, mi = time.split(":")
    return pd.Timestamp(year=int(y), month=int(m), day=int(d), hour=int(h), minute=int(mi), tz="Europe/Zurich")
