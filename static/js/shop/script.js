document.addEventListener('DOMContentLoaded', () => {
    const userPoint = document.getElementById("user_point");
    const userCharacter = document.getElementById("character");
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

    function createInfoContent(id, price, imgSrc, title, description, name) {
        return `
            <div class="info-content">
                <button class="close-btn">X</button>
                <p class="price">${price}P 이상 보유 시 사용 가능합니다.</p>
                <img src="${imgSrc}" alt="${title}">
                <h2>${title}</h2>
                <p>${description}</p>
                <button class="purchase-btn" data-price="${price}" data-name="${name}">사용하기</button>
            </div>
        `;
    }

    // 배경들
    const backgrounds = [
        { id: 'spring-background', price: '100', imgSrc: '../static/imgs/spring.png', title: '봄 배경', description: '이 배경은 봄의 따뜻한 감성을 표현한 배경입니다.' },
        { id: 'summer-background', price: '100', imgSrc: '../static/imgs/summer.png', title: '여름 배경', description: '시원한 여름의 배경입니다.' },
        { id: 'autumn-background', price: '100', imgSrc: '../static/imgs/autumn.png', title: '가을 배경', description: '가을의 따뜻한 색감을 담은 배경입니다.' },
        { id: 'winter-background', price: '100', imgSrc: '../static/imgs/winter.png', title: '겨울 배경', description: '차가운 겨울의 배경입니다.' },
        { id: 'blossoms-background', price: '200', imgSrc: '../static/imgs/blossoms.png', title: '꽃 배경', description: '화사한 꽃의 배경입니다.' },
        { id: 'gradient-background', price: '300', imgSrc: '../static/imgs/gradient.png', title: '그라데이션 배경', description: '부드러운 그라데이션 배경입니다.' },
        { id: 'wave-background', price: '4000', imgSrc: '../static/imgs/wave.png', title: '파도 배경', description: '동적인 파도 모양의 배경입니다.' },
    ];

    backgrounds.forEach(bg => {
        const element = document.getElementById(bg.id);
        element.addEventListener('click', () => {
            showInfo(createInfoContent(bg.id, bg.price, bg.imgSrc, bg.title, bg.description, bg.title));
        });
    });

    // 캐릭터들
    const characters = [
        { id: 'roi-character', price: '10', imgSrc: '../static/imgs/roi.png', name: 'roi', title: '로이', description: '작고 귀여운 외모로 사랑받는 작은 친구입니다.' },
        { id: 'dudu-character', price: '50', imgSrc: '../static/imgs/dudu.png', name: 'dudu', title: '두두', description: '지후야 이거 보면 기획 짜와라' },
        { id: 'jjini-character', price: '100', imgSrc: '../static/imgs/jjini.png', name: 'jjini', title: '찌니', description: '지후야 이거 보면 기획 짜와라' },
        { id: 'wingwing-character', price: '100', imgSrc: '../static/imgs/wingwing.png', name: 'wingwing', title: '윙윙', description: '지후야 이거 보면 기획 짜와라' },
        { id: 'jeombo-character', price: '200', imgSrc: '../static/imgs/jeombo.png', name: 'jeombo', title: '점보', description: '지후야 이거 보면 기획 짜와라' },
        { id: 'juno-character', price: '200', imgSrc: '../static/imgs/juno.png', name: 'juno', title: '주노', description: '캐릭터 설명 뭐라하지?' },
        { id: 'moka-character', price: '300', imgSrc: '../static/imgs/moka.png', name: 'moka', title: '모카', description: '캐릭터 설명 뭐라하지?' },
        { id: 'somi-character', price: '1000', imgSrc: '../static/imgs/somi.png', name: 'somi', title: '솜이', description: '지후야 이거 보면 기획 짜와라' },
        { id: 'runa-character', price: '2000', imgSrc: '../static/imgs/runa.png', name: 'runa', title: '루나', description: '캐릭터 설명 뭐라하지?' },
        { id: 'reona-character', price: '3000', imgSrc: '../static/imgs/reona.png', name: 'reona', title: '레오나', description: '캐릭터 설명 뭐라하지?' }
    ];
    

    characters.forEach(character => {
        const element = document.getElementById(character.id);
        element.addEventListener('click', () => {
            showInfo(createInfoContent(character.id, character.price, character.imgSrc, character.title, character.description, character.name));
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
            const price = parseInt(event.target.getAttribute('data-price'));
            const name = event.target.getAttribute('data-name'); // 수정된 부분
            let user_point = parseInt(userPoint.value);
            
            if (user_point >= price) {
                // userPoint.value = user_point - price; // 포인트 차감
                userCharacter.value = name; // 선택된 캐릭터 저장
                alert(`${name} 캐릭터가 적용되었습니다!`); // 적용된 캐릭터 이름 표시
            } else {
                alert(`포인트가 부족합니다.`);
            }
            hideInfo();
        }
    });

    // 돌아가기 버튼 이벤트 리스너
    // document.getElementById('back-btn').addEventListener('click', () => {
    //     history.back(); // 돌아가기 URL 설정
    // });
});
