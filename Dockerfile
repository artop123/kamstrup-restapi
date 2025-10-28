FROM python:3.9-slim-buster

WORKDIR /app

COPY app/requirements.txt .
COPY app/restapi.py .
COPY app/kamstrup_modbus.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "restapi.py"]
