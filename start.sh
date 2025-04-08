#!/bin/bash

# 배포 시간 표시 (디버깅용)
BUILD_TIME=$(date +%Y%m%d%H%M%S)
echo "배포 시간: $BUILD_TIME"

# 환경 변수 설정 (pod의 UID를 사용할 수 없는 경우)
if [ -z "$STATIC_VERSION" ]; then
    export STATIC_VERSION=$BUILD_TIME
fi
echo "정적 파일 버전: $STATIC_VERSION"

# 정적 파일 디렉토리가 비어있지 않다면 초기화
if [ "$(ls -A /app/staticfiles 2>/dev/null)" ]; then
    echo "정적 파일 디렉토리 초기화 중..."
    rm -rf /app/staticfiles/*
fi

# 정적 파일 수집
echo "정적 파일 수집 중..."
python manage.py collectstatic --noinput

# Gunicorn 시작
echo "Gunicorn 시작 중..."
gunicorn heyb.wsgi:application --bind 0.0.0.0:$PORT 