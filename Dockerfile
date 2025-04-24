FROM python:3.11-slim

RUN pip install paho-mqtt

WORKDIR /app
COPY ewpe-smart-mqtt.py /app/
COPY config.yaml /app/

CMD ["python", "/app/ewpe-smart-mqtt.py", "/app/config.yaml"]
