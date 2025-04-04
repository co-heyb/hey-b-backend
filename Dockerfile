FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 스크립트에 실행 권한 부여
RUN chmod +x entrypoint.sh

EXPOSE 8000

# entrypoint.sh 스크립트를 사용하여 환경에 따라 다른 명령 실행
ENTRYPOINT ["/app/entrypoint.sh"] 