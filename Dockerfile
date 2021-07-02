FROM python:3.9-slim

WORKDIR /opt
RUN apt update && apt install -y make build-essential
COPY . .
RUN python -m pip install -r requirements.txt --no-cache-dir --no-deps
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]