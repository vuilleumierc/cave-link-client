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

@app.get("/cave-link-proxy")
async def read_cave_link_proxy():
    """Proxy endpoint to fetch data from the Cave-Link API.
    This endpoint fetches data returns it in JSON format.
    """
    print("Fetching data from Cave-Link API")
    # Default parameters
    params = {
        "s": 106,
        "g": 0,
        "w": 0,
        "l": 10,
    }
    cl_response = requests.get(BASE_URL, params=params)

    data = parse_cl_response(cl_response.text)
    print(data)

    response = JSONResponse(
        content=data,
        media_type="application/json",
        headers={
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        status_code=200,
    )
    return response

def parse_cl_response(content: str) -> dict:
    """
    Parse the Cave-Link response content into a dictionary.
    """
    lines = content.strip().split("<br>")
    metadata = lines[:2]
    data = [ data_row_to_dict(row) for row in lines[2:] if row.strip() ]
    return {
        "metadata": metadata,
        "data": data
    }

def data_row_to_dict(row: str) -> dict:
    """
    Convert a data row string into a dictionary.
    """
    parts = row.split(",")
    return {
        "timestamp": parts[0],
        "value": parts[1].strip(),
    }
