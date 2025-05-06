FROM tiangolo/uvicorn-gunicorn-fastapi:latest

WORKDIR /src

COPY ./ /src

RUN pip install --upgrade pip && pip install -r requirements.in

ENTRYPOINT ["python3", "main.py"]
