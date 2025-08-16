import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

BASE_URL = "https://www.cavelink.com/cl/da.php"

app = FastAPI()

app.mount("/static", StaticFiles(directory="ui"), name="static")


@app.get("/")
def serve_ui():
    print("Serving index.html")
    return FileResponse("ui/index.html", media_type="text/html")


@app.get("/cave-link-proxy/data")
async def read_cave_link_proxy(station: str, variable: str):
    """
    Proxy endpoint to fetch data from the Cave-Link API.
    This endpoint fetches data returns it in JSON format.
    """
    print("Fetching data from Cave-Link API")
    params = translate_query_params(station, variable)
    cl_response = requests.get(BASE_URL, params=params)

    data = parse_cl_response(cl_response.text)
    print(data)

    response = JSONResponse(
        content=data,
        status_code=200,
    )
    return response


def translate_query_params(station: str, variable: str) -> dict:
    params = {}
    match station:
        case "motiers":
            params["s"] = 106
            match variable:
                case "batterie":
                    params["g"] = 0
                    params["w"] = 0
                case "waterLevel":
                    params["g"] = 1
                    params["w"] = 101
                case "waterTemperature":
                    params["g"] = 1
                    params["w"] = 0
    return params


def parse_cl_response(content: str) -> dict:
    """
    Parse the Cave-Link response content into a dictionary.
    """
    lines = content.strip().split("<br>")
    metadata = lines[:2]
    data = [data_row_to_dict(row) for row in lines[2:] if row.strip()]
    return {"metadata": metadata, "data": data}


def data_row_to_dict(row: str) -> dict:
    """
    Convert a data row string into a dictionary.
    """
    parts = row.split(",")
    return {
        "timestamp": parts[0],
        "value": parts[1].strip(),
    }
