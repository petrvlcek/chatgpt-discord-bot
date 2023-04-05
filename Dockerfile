FROM python:3.11-slim-bullseye

RUN apt update && apt install -y jq

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY main.py .
COPY app ./app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]