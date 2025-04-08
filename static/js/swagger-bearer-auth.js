// Bearer 접두사 자동 추가 스크립트
window.addEventListener('load', function() {
  // 스웨거 UI가 로드된 후 실행
  setTimeout(function() {
    // 원래의 Authorize 함수를 저장
    const originalAuthorize = window.ui.authActions.authorize;
    
    // Authorize 함수를 오버라이드
    window.ui.authActions.authorize = function(payload) {
      // Bearer 접두사 자동 추가
      const newPayload = {...payload};
      
      if (newPayload.Bearer && !newPayload.Bearer.value.startsWith('Bearer ')) {
        newPayload.Bearer.value = 'Bearer ' + newPayload.Bearer.value;
      }
      
      // 원래 함수 호출
      return originalAuthorize(newPayload);
    };
    
    // 입력 필드에 이벤트 리스너 추가
    const observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        if (mutation.addedNodes.length) {
          const authInputs = document.querySelectorAll('.auth-container input');
          
          authInputs.forEach(function(input) {
            // 이미 처리된 입력 필드는 건너뛰기
            if (input.dataset.processed) return;
            
            // 입력 필드 처리 표시
            input.dataset.processed = 'true';
            
            // placeholder 변경
            if (input.placeholder === 'api_key') {
              input.placeholder = '토큰만 입력하세요 (Bearer 접두사 없이)';
            }
            
            // Bearer 접두사가 있으면 제거
            input.addEventListener('input', function(e) {
              if (e.target.value.startsWith('Bearer ')) {
                e.target.value = e.target.value.substring(7);
              }
            });
          });
        }
      });
    });
    
    // DOM 변경 감시 시작
    observer.observe(document.body, { childList: true, subtree: true });
  }, 1000);
});

// Swagger UI를 위한 커스텀 스크립트
// HTTP 요청을 HTTPS로 강제 변환
(function() {
  // 페이지 로드 완료 후 실행
  window.addEventListener('load', function() {
    // 개발 환경 여부 확인 (localhost 또는 127.0.0.1)
    const isLocalhost = window.location.hostname === 'localhost' || 
                        window.location.hostname === '127.0.0.1' ||
                        window.location.hostname.startsWith('192.168.');
    
    // 개발 환경이 아니고 HTTP 프로토콜인 경우에만 HTTPS로 리다이렉트
    if (window.location.protocol === 'http:' && !isLocalhost) {
      window.location.href = window.location.href.replace('http:', 'https:');
      return;
    }

    // 개발 환경이 아닌 경우에만 HTTPS 관련 처리
    if (!isLocalhost) {
      // API 요청 인터셉터 설정
      const originalFetch = window.fetch;
      window.fetch = function(url, options) {
        // HTTP URL을 HTTPS로 변환
        if (typeof url === 'string' && url.startsWith('http:')) {
          url = url.replace('http:', 'https:');
        }
        return originalFetch(url, options);
      };

      // Swagger UI가 로드되었을 때 추가 설정
      const intervalId = setInterval(function() {
        if (window.ui) {
          clearInterval(intervalId);
          
          // Swagger UI 구성 후크
          const original = window.ui.initOAuth;
          window.ui.initOAuth = function(conf) {
            // 모든 API 요청을 HTTPS로 설정
            if (window.ui.getConfigs) {
              const configs = window.ui.getConfigs();
              configs.schemes = ['https'];
              
              // URL이 있고 HTTP로 시작하는 경우에만 변경
              if (configs.url && configs.url.startsWith('http:')) {
                configs.url = configs.url.replace('http:', 'https:');
              }
            }
            original(conf);
          };
        }
      }, 100);
    }
  });
})(); 