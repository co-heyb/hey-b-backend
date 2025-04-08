FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 정적 파일 수집
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# gunicorn으로 실행
CMD gunicorn heyb.wsgi:application --bind 0.0.0.0:$PORT 