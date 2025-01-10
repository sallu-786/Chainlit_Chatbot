from fastapi import FastAPI
from chainlit.utils import mount_chainlit
import uvicorn

app = FastAPI()


@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}

mount_chainlit(app=app, target="cl_app2.py", path="/codepilot")
