document.addEventListener('DOMContentLoaded', () => {
    const spring = document.getElementById('spring-background');
    const springBackgroundInfo = document.getElementById('spring-background-info');
    const wrap = document.querySelector('.wrap');

    spring.addEventListener('click', () => {
        // 새로운 div 생성
        const newDiv = document.createElement('div'); 
        newDiv.className = 'spring-background-showbox';

        // 내용물 추가 (이미지 포함, 구매 버튼 추가)
        newDiv.innerHTML = `
            <div class="spring-background-content">
                <button id="close-btn">X</button>
                <p class="price">1000 Point</p>
                <img src="../static/imgs/background_1.png" alt="봄 배경 이미지">
                <h2>봄 배경 정보</h2>
                <p>이 배경은 봄의 따뜻한 감성을 표현한 배경입니다.</p>
                <button class="purchase-btn">구매하기</button>
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

        // 구매하기 버튼 이벤트 추가
        const purchaseBtn = document.querySelector('.purchase-btn');
        purchaseBtn.addEventListener('click', () => {
            alert('봄 배경이 구매되었습니다!');
        });
    });
});