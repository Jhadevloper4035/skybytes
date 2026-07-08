const cards = document.querySelectorAll('.accordion-card');
let activeIndex = 0;

function updateActiveCard(index) {
    if (window.innerWidth >= 768) {
        cards.forEach((card, i) => {
            card.classList.toggle('active', i === index);
        });
        activeIndex = index;
    }
}



cards.forEach((card, index) => {
    card.addEventListener('mouseenter', () => {
        updateActiveCard(index);
    });
});

window.addEventListener('resize', () => {
    if (window.innerWidth < 768) {
        stopRotation();
        cards.forEach(c => c.classList.remove('active'));
    } else {
        updateActiveCard(0);
        startRotation();
    }
});
