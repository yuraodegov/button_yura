FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y gcc

RUN pip install pytest flask

EXPOSE 5000

CMD ["python", "simulator/server.py"]