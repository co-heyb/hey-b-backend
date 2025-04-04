#!/bin/sh

# 환경 변수가 설정되지 않은 경우 기본값 설정
if [ -z "$DEBUG" ]; then
    export DEBUG=True
fi

# 운영 환경에서는 정적 파일 수집
if [ "$DEBUG" = "False" ]; then
    echo "운영 모드에서 실행 중입니다. 정적 파일을 수집합니다..."
    python manage.py collectstatic --noinput
    
    # gunicorn으로 애플리케이션 실행
    echo "Gunicorn으로 애플리케이션을 시작합니다..."
    exec gunicorn heyb.wsgi:application --bind 0.0.0.0:8000
else
    # 개발 환경에서는 runserver 사용
    echo "개발 모드에서 실행 중입니다..."
    exec python manage.py runserver 0.0.0.0:8000
fi
