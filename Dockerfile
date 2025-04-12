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

# 스크립트에 실행 권한 부여
RUN chmod +x start.sh

# 정적 파일 수집 (빌드 타임에 미리 수집)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# 시작 스크립트로 실행
CMD ["./start.sh"] 