document.addEventListener('DOMContentLoaded', () => {
    const infoBox = document.createElement('div');
    infoBox.className = 'info-box';
    document.body.appendChild(infoBox);

    function showInfo(contentHtml) {
        infoBox.innerHTML = contentHtml;
        infoBox.style.display = 'flex';
    }

    function hideInfo() {
        infoBox.style.display = 'none';
    }

    function createInfoContent(id, price, imgSrc, title, description) {
        return `
            <div class="info-content">
                <button class="close-btn">X</button>
                <p class="price">${price} Point</p>
                <img src="${imgSrc}" alt="${title}">
                <h2>${title}</h2>
                <p>${description}</p>
                <button class="purchase-btn">구매하기</button>
            </div>
        `;
    }

    // 배경들
    const backgrounds = [
        { id: 'spring-background', price: '1000', imgSrc: '../static/imgs/background_1.png', title: '봄 배경', description: '이 배경은 봄의 따뜻한 감성을 표현한 배경입니다.' },
        // 추가 배경 데이터 삽입
    ];

    backgrounds.forEach(bg => {
        const element = document.getElementById(bg.id);
        element.addEventListener('click', () => {
            showInfo(createInfoContent(bg.id, bg.price, bg.imgSrc, bg.title, bg.description));
        });
    });

    // 캐릭터들
    const characters = [
        { id: 'roi-character', price: '1000', imgSrc: '../static/imgs/roi.png', title: '로이', description: '캐릭터 설명 뭐라하지?' },
        { id: 'dudu-character', price: '1200', imgSrc: '../static/imgs/dudu.png', title: '두두', description: '지후야 이거 보면 기획 짜와라' },
        { id: 'reona-character', price: '1200', imgSrc: '../static/imgs/reona.png', title: '레오나', description: '캐릭터 설명 뭐라하지?' },
        { id: 'jeombo-character', price: '1200', imgSrc: '../static/imgs/jeombo.png', title: '점보', description: '지후야 이거 보면 기획 짜와라' },
        { id: 'runa-character', price: '1200', imgSrc: '../static/imgs/runa.png', title: '루나', description: '캐릭터 설명 뭐라하지?' },
        { id: 'somi-character', price: '1200', imgSrc: '../static/imgs/somi.png', title: '솜이', description: '지후야 이거 보면 기획 짜와라' },
        { id: 'juno-character', price: '1200', imgSrc: '../static/imgs/juno.png', title: '주노', description: '캐릭터 설명 뭐라하지?' },
        { id: 'jjini-character', price: '1200', imgSrc: '../static/imgs/jjini.png', title: '찌니', description: '지후야 이거 보면 기획 짜와라' },
        { id: 'moka-character', price: '1200', imgSrc: '../static/imgs/moka.png', title: '모카', description: '캐릭터 설명 뭐라하지?' },
        { id: 'wingwing-character', price: '1200', imgSrc: '../static/imgs/wingwing.png', title: '윙윙', description: '지후야 이거 보면 기획 짜와라' },
    ];

    characters.forEach(character => {
        const element = document.getElementById(character.id);
        element.addEventListener('click', () => {
            showInfo(createInfoContent(character.id, character.price, character.imgSrc, character.title, character.description));
        });
    });

    // 닫기 버튼 이벤트 리스너 추가
    infoBox.addEventListener('click', (event) => {
        if (event.target.classList.contains('close-btn')) {
            hideInfo();
        }
    });

    // 구매하기 버튼 이벤트 리스너 추가
    infoBox.addEventListener('click', (event) => {
        if (event.target.classList.contains('purchase-btn')) {
            alert('구매가 완료되었습니다!');
            hideInfo();
        }
    });

    // 돌아가기 버튼 이벤트 리스너
    document.getElementById('back-btn').addEventListener('click', () => {
        history.back(); // 돌아가기 URL 설정
    });
});
