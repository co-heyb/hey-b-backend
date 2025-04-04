#!/bin/bash

# 스크립트 오류 시 중단
set -e

echo "===== Koyeb 배포 준비 시작 ====="

# 임시 Dockerfile 생성
echo "1. 운영용 Dockerfile 준비"
if [ -f Dockerfile.bak ]; then
    echo "기존 Dockerfile 백업이 이미 존재합니다."
else
    if [ -f Dockerfile ]; then
        cp Dockerfile Dockerfile.bak
        echo "기존 Dockerfile을 Dockerfile.bak으로 백업했습니다."
    fi
fi

# Koyeb용 Dockerfile 적용
cp Dockerfile.koyeb Dockerfile
echo "Koyeb용 Dockerfile을 적용했습니다."

# 환경 변수 설정 확인
echo "2. 환경 변수 설정 확인"
if [ ! -f .env.prod ]; then
    echo "오류: .env.prod 파일이 없습니다!"
    exit 1
fi

echo "3. Git 변경사항 커밋 및 푸시"
git add Dockerfile
git commit -m "배포: Koyeb 환경에 맞게 Dockerfile 수정"
git push

echo "===== Koyeb 배포 준비 완료 ====="
echo "이제 Koyeb 대시보드에서 배포를 진행하세요."
echo "배포 후에는 ./restore-dockerfile.sh를 실행하여 개발용 Dockerfile을 복원할 수 있습니다."

# 복원 스크립트 생성
cat > restore-dockerfile.sh << 'EOL'
#!/bin/bash
if [ -f Dockerfile.bak ]; then
    mv Dockerfile.bak Dockerfile
    echo "개발용 Dockerfile을 복원했습니다."
else
    echo "백업된 Dockerfile이 없습니다."
fi
EOL

chmod +x restore-dockerfile.sh
