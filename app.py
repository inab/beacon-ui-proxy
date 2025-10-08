import os
from flask import Flask, request, Response, jsonify
import requests
from urllib.parse import urljoin
#from environs import Env

app = Flask(__name__)

REAL_API_BASE = os.getenv("REAL_API_BASE")
PROXY_BASE_PATH = os.getenv("PROXY_BASE_PATH")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS").split(",")

TIMEOUT = float(os.getenv("UPSTREAM_TIMEOUT", "60"))

def _cors_headers(resp: Response) -> Response:
    origin = request.headers.get("Origin")
    if origin and origin in ALLOWED_ORIGINS:
        resp.headers["Access-Control-Allow-Origin"] = origin
        resp.headers["Access-Control-Allow-Credentials"] = "true"
        resp.headers["Vary"] = "Origin"
    resp.headers["Access-Control-Expose-Headers"] = "Content-Type, Content-Length"
    return resp

@app.route("/health", methods=["GET"])
def health():
    return jsonify(ok=True)

@app.route(f"{PROXY_BASE_PATH}/", defaults={"path": ""}, methods=["OPTIONS"])
@app.route(f"{PROXY_BASE_PATH}/<path:path>", methods=["OPTIONS"])
def preflight(path):
    resp = Response(status=204)
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,PATCH,DELETE,OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = request.headers.get(
        "Access-Control-Request-Headers", "Authorization, Content-Type"
    )
    return _cors_headers(resp)

@app.route(f"{PROXY_BASE_PATH}/", defaults={"path": ""}, methods=["GET","POST","PUT","PATCH","DELETE"])
@app.route(f"{PROXY_BASE_PATH}/<path:path>", methods=["GET","POST","PUT","PATCH","DELETE"])
def proxy(path):
    upstream_url = urljoin(REAL_API_BASE.rstrip("/") + "/", path)

    headers = {}
    for k, v in request.headers.items():
        lk = k.lower()
        if lk in ("host", "content-length", "origin"):
            continue
        headers[k] = v

    data = request.get_data() if request.method not in ("GET", "HEAD") else None

    try:
        r = requests.request(
            method=request.method,
            url=upstream_url,
            params=request.args,
            headers=headers,
            data=data,
            timeout=TIMEOUT,
            stream=True,
        )
    except requests.RequestException as e:
        resp = jsonify(error="Proxy error", detail=str(e))
        resp.status_code = 502
        return _cors_headers(resp)

    excluded = {"transfer-encoding", "content-encoding", "content-length", "connection"}
    resp = Response(
        r.raw.read(decode_content=False),
        status=r.status_code,
    )
    for k, v in r.headers.items():
        if k.lower() not in excluded:
            resp.headers[k] = v

    return _cors_headers(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
