#!/bin/bash

# 스크립트 오류 시 중단
set -e

echo "===== 배포 시작 ====="

# 최신 코드 가져오기
echo "1. Git pull 실행"
git pull

# 운영 환경 설정 확인
echo "2. 환경 변수 설정 확인"
if [ ! -f .env.prod ]; then
    echo "오류: .env.prod 파일이 없습니다!"
    exit 1
fi

# Docker 이미지 빌드
echo "3. Docker 이미지 빌드"
docker-compose -f docker-compose.prod.yml build

# 정적 파일 수집
echo "4. 컨테이너 실행 및 서비스 시작"
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

echo "5. 마이그레이션 실행"
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

echo "===== 배포 완료 ====="
