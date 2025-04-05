#!/bin/bash

# 스크립트 오류 시 중단
set -e

echo "===== Render 배포 준비 시작 ====="

# Git 업데이트
echo "1. Git 변경사항 커밋"
git add Dockerfile render.yaml
git commit -m "배포: Render 배포 설정 추가"
git push

echo "===== Render 배포 준비 완료 ====="
echo "이제 Render 대시보드에서 다음 중 한 가지 방법으로 배포를 진행하세요:"
echo ""
echo "1. Blueprint 방식 (권장):"
echo "   - Render 대시보드에서 'New Blueprint' 선택"
echo "   - GitHub 레포지토리 연결 후 배포"
echo ""
echo "2. 수동 설정 방식:"
echo "   - 각 서비스를 개별적으로 생성"
echo "   - 각 서비스마다 환경 변수 직접 설정"
echo ""
echo "주의: Render 무료 플랜에서는 일부 서비스가 사용량 제한이 있을 수 있습니다."
