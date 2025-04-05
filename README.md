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
- [ ] CI/CD 파이프라인 구축
- [ ] 성능 최적화

## API 문서

API 문서는 다음 URL에서 확인할 수 있습니다:
- Swagger UI: /swagger/
- ReDoc: /redoc/ 