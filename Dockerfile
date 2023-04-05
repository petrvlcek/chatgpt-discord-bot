FROM python:3.10

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app $APP_HOME/app

ENV PYTHONPATH=$APP_HOME/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]