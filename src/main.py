import uvicorn
from api import app
from config import APP_HOST, APP_PORT


def start_server():
    # Levanto la API
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)


if __name__ == "__main__":
    start_server()