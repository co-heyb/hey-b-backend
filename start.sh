#!/bin/bash

# 배포 시간 표시 (디버깅용)
BUILD_TIME=$(date +%Y%m%d%H%M%S)
echo "배포 시간: $BUILD_TIME"

# 환경 변수 설정 (pod의 UID를 사용할 수 없는 경우)
if [ -z "$STATIC_VERSION" ]; then
    export STATIC_VERSION=$BUILD_TIME
fi
echo "정적 파일 버전: $STATIC_VERSION"

# Gunicorn 시작
echo "Gunicorn 시작 중..."
gunicorn heyb.wsgi:application --bind 0.0.0.0:$PORT 