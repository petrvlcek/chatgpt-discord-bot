FROM python:3.11-slim-bullseye

RUN apt update && apt install -y jq curl

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app ./app

EXPOSE 8000

WORKDIR $APP_HOME/app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]