const menuToggle = document.getElementById('menuToggle');
const mobileMenu = document.getElementById('mobileMenu');
const toTop = document.getElementById('to-top');
document.addEventListener("DOMContentLoaded", () => {
    const logo = document.querySelector('.logo-img.desktop');
    const path = window.location.pathname;

    if (logo && !path.endsWith("index.html") && path !== "/") {
        logo.src = "/static/logo/logo.png";
    }
});
menuToggle.addEventListener('click', () => {
    mobileMenu.style.display =
        mobileMenu.style.display === 'block' ? 'none' : 'block';
});

window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        toTop.classList.remove('d-none');
    } else {
        toTop.classList.add('d-none');
    }
});

toTop.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});



const readMore = document.getElementById('read-more');
const toShow = document.querySelectorAll('.to-show');

readMore.addEventListener("click", () => {

    readMore.classList.toggle("active");

    toShow.forEach(el => {
        el.classList.toggle('d-none');
    });

    readMore.textContent = readMore.classList.contains("active") 
        ? "Read Less" 
        : "Read More";
});