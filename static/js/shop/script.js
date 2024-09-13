document.addEventListener('DOMContentLoaded', () => {
    const spring = document.getElementById('spring-background');
    const springBackgroundInfo = document.getElementById('spring-background-info');
    const wrap = document.querySelector('.wrap');

    spring.addEventListener('click', () => {
        // 새로운 div 생성
        const newDiv = document.createElement('div'); 
        newDiv.className = 'spring-background-showbox';

        // 내용물 추가
        newDiv.innerHTML = `
            <div class="spring-background-content">
                <h2>봄 배경 정보</h2>
                <p>이 배경은 봄의 따뜻한 감성을 표현한 배경입니다.</p>
                <button id="close-btn">닫기</button>
            </div>
        `;

        // wrap의 overflow 숨기기
        wrap.classList.add('overflow-hidden');

        // 새로운 div 추가
        springBackgroundInfo.appendChild(newDiv);

        // 닫기 버튼 기능 추가
        const closeBtn = document.getElementById('close-btn');
        closeBtn.addEventListener('click', () => {
            springBackgroundInfo.removeChild(newDiv);
            wrap.classList.remove('overflow-hidden'); // wrap의 overflow 복원
        });
    });
});