FROM python:3.12-alpine AS build

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.12-alpine

WORKDIR /app

COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

COPY . .

CMD ["uvicorn", "proxy_api:app", "--log-config", "log_conf.yaml", "--host", "0.0.0.0", "--port", "5000"]
