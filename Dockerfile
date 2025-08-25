FROM python:3.13-slim
LABEL authors="Egor"

WORKDIR /app
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY bot/ ./bot/
CMD ["python", "bot/main.py"]
