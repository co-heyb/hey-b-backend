## 1. 제품 개요

취미 활동을 공유하고 관련 취미키트를 구매할 수 있는 소셜 커머스 플랫폼

## 2. 목표와 가치 제안

- 비즈니스 목표
    - 취미 커뮤니티 형성을 통한 사용자 기반 확보
    - 취미키트 판매를 통한 수익 창출
    - 사용자 데이터 기반의 맞춤형 취미 추천
- 사용자 가치
    - 새로운 취미 발견 및 시작의 진입장벽 낮춤
    - 취미 활동 공유를 통한 성취감과 동기부여
    - 취미 커뮤니티를 통한 소속감 형성

## 3. 핵심 기능 상세

### 3.1 소셜 피드 시스템

- 게시물 작성
    - 이미지/동영상 첨부 (최대 10장, 동영상 최대 3분)
    - 해시태그 기능 (최대 10개)
    - 위치 정보 태그
- 인터랙션
    - 좋아요, 북마크 기능
    - 댓글 및 대댓글 (이미지 첨부 가능)
    - 게시물 공유 기능
- 피드 알고리즘
    - 사용자 관심사 기반 콘텐츠 추천
    - 팔로우 중인 사용자의 활동 우선 노출
    - 인기 콘텐츠 큐레이션

### 3.2 취미키트 커머스

- 상품 표시
    - 카테고리별 분류 시스템
    - 상세 정보 (재료 목록, 난이도, 소요시간)
    - 실시간 재고 현황
- 구매 프로세스
    - 장바구니 기능
    - 다양한 결제 수단 지원
    - 배송 추적 시스템
- 리뷰 시스템
    - 별점 평가 (5점 척도)
    - 포토/동영상 리뷰
    - 리뷰 신뢰도 점수 시스템

### 3.3 사용자 프로필

- 기본 정보 관리
    - 프로필 사진 및 배경
    - 자기소개
    - 관심 취미 태그
- 활동 내역
    - 작성 게시물 모아보기
    - 참여 중인 취미 활동
    - 구매 내역 및 리뷰
- 소셜 기능
    - 팔로워/팔로잉 관리
    - 1:1 메시지
    - 차단/신고 기능

## 4. 기술 요구사항

### 4.1 프론트엔드

- 반응형 웹 디자인 (모바일 최적화)
- 이미지 레이지 로딩 구현
- 실시간 알림 시스템 (WebSocket)
- 무한 스크롤 피드

### 4.2 백엔드

- 데이터베이스 설계
    - 사용자 정보 및 인증
    - 게시물 및 상호작용
    - 상품 및 주문 관리
- API 설계
    - RESTful API 구현
    - API 버전 관리
    - 요청 제한 (Rate Limiting)
- 성능 최적화
    - 캐싱 시스템 구축
    - 이미지 처리 및 저장
    - 검색 엔진 최적화

### 4.3 인프라

- 클라우드 인프라 구축
- CDN 설정
- 백업 및 복구 시스템
- 모니터링 및 로깅

## 5. 보안 요구사항

- 사용자 인증 및 권한 관리
    - 이메일/SNS 인증
    - 2단계 인증
    - 접근 권한 관리
- 데이터 보안
    - 개인정보 암호화
    - 결제 정보 보안
    - 데이터 백업
- 보안 모니터링
    - 로그 분석
    - 이상 행동 감지
    - 취약점 스캔

## 6. 성과 지표(KPI)

- 사용자 지표
    - DAU/MAU
    - 사용자 체류 시간
    - 재방문율
- 콘텐츠 지표
    - 게시물 작성 수
    - 댓글 및 상호작용 수
    - 공유 횟수
- 커머스 지표
    - 취미키트 판매량
    - 평균 주문 금액
    - 재구매율

## 7. 출시 전략

- 베타 테스트
    - 초기 사용자 그룹 선정
    - 피드백 수집 및 분석
    - 주요 기능 개선
- 마케팅 전략
    - SNS 채널 운영
    - 인플루언서 협업
    - 이벤트 및 프로모션
- 확장 계획
    - 신규 카테고리 확대
    - 오프라인 연계 이벤트
    - 파트너십 구축


## 8. 기술스택

**백엔드**:

- django, django ninja - 생산성있는 api개발과 어드민 페이지 개발
- Redis와 Celery - 실시간 업데이트 처리와 비동기 작업 큐잉에 효과적
- Docker - 개발 환경 컨테이너화 및 배포 자동화에 유용

**인증/보안**:

- OAuth2와 JWT - 인증 처리를 위한 안전한 방식

**모니터링/로깅**:

- Sentry - 에러 모니터링
- Elastic Stack - 효율적인 로깅 및 모니터링