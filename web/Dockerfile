FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt


COPY ./app .

EXPOSE $PEACEFUL_FARM_SERVER_PORT

CMD ["python3", "-u", "./app.py"]
