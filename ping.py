from fastapi import FastAPI
from starlette.responses import Response

app = FastAPI()

@app.get("/ping")
def hello():
    return Response(content="pong", status_code=200, media_type="text/plain")