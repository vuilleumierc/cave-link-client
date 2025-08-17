# Cave-Link data viewer

## Installation

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run 

```shell
uvicorn proxy_api:app --reload --port 5000 --host 0.0.0.0
```

The app will be available at http://localhost:5000/

## Build and run with Docker

```shell
docker build --tag cave-link-data-viewer:latest . && docker run -p 5000:5000 cave-link-data-viewer
```
