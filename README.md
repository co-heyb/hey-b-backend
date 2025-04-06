# HeyB 백엔드

HeyB 서비스의 백엔드 API 서버입니다.

## 개발 환경 설정

```bash
# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정 (.env 파일 참조)

# 마이그레이션 적용
python manage.py migrate

# 개발 서버 실행
python manage.py runserver
```

## 배포 환경

- Render: https://hey-b-backend.onrender.com/swagger/
- Kubernetes/ArgoCD: [배포 방법 참조](#kubernetes-배포-argocd)

## 할 일 목록

### API 배포

- [x] 사용자 API (users) 배포
- [ ] 소셜 API (social) 배포
  - [ ] 게시물 관리 API 구현 및 배포
  - [ ] 게시물 상호작용 API 구현 및 배포
  - [ ] 댓글 관리 API 구현 및 배포
  - [ ] 해시태그 관리 API 구현 및 배포
  - [ ] 피드 API 구현 및 배포
- [ ] 커머스 API (commerce) 배포
  - [ ] 카테고리 관리 API 구현 및 배포
  - [ ] 상품 관리 API 구현 및 배포
  - [ ] 장바구니 관리 API 구현 및 배포
  - [ ] 주문 관리 API 구현 및 배포
  - [ ] 리뷰 관리 API 구현 및 배포

### 기타 작업

- [x] 스웨거 문서화 설정
- [ ] 테스트 코드 작성
- [x] CI/CD 파이프라인 구축
- [ ] 성능 최적화

## API 문서

API 문서는 다음 URL에서 확인할 수 있습니다:
- Swagger UI: /swagger/
- ReDoc: /redoc/ 

## Kubernetes 배포 (ArgoCD)

이 프로젝트는, ArgoCD를 통해 Kubernetes 클러스터에 배포할 수 있습니다.

### 사전 요구사항

- Kubernetes 클러스터
- ArgoCD 설치됨
- GitHub Actions 실행 환경에 필요한 시크릿 설정:
  - `ARGOCD_SERVER`: ArgoCD 서버 URL
  - `ARGOCD_USERNAME`: ArgoCD 사용자 이름
  - `ARGOCD_PASSWORD`: ArgoCD 패스워드

### 배포 방법

1. GitHub 저장소를 복제하고 GitHub Actions 시크릿을 설정합니다.
2. 다음 파일들을 환경에 맞게 수정합니다:
   - `argocd/heyb-dev-application.yaml`: 저장소 URL 등 설정
   - `argocd/heyb-prod-application.yaml`: 저장소 URL 등 설정
   - `k8s/overlays/dev/secrets.yaml`: 개발 환경 시크릿 설정
   - `k8s/overlays/prod/secrets.yaml`: 운영 환경 시크릿 설정
3. GitHub Actions 워크플로우를 통해 배포:
   - 메인 브랜치로 푸시: 자동으로 개발 환경에 배포
   - 수동 워크플로우 실행: 개발 또는 운영 환경 선택 배포

### 수동 배포

```bash
# ArgoCD CLI 로그인
argocd login <ARGOCD_SERVER> --username <USERNAME> --password <PASSWORD> --insecure

# 애플리케이션 생성 (개발 환경)
IMAGE_REGISTRY=ghcr.io/yourusername IMAGE_TAG=latest envsubst < argocd/heyb-dev-application.yaml | argocd app create --upsert -f -

# 애플리케이션 동기화
argocd app sync heyb-dev --prune
```