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