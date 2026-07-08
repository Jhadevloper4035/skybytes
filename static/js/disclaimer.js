
document.addEventListener('DOMContentLoaded', () => {
    const disclaimerContainer = document.getElementById('disclaimer-main');
    const disclaimerClose = document.querySelector('.disclaimer-footer');
    const isAgreed = localStorage.getItem("disclaimer");
    if (!isAgreed) {
        setTimeout(() => {
            disclaimerContainer.classList.remove('d-none');
        }, 3000);
    }
    disclaimerClose.addEventListener('click', () => {
        localStorage.setItem('disclaimer',"agreed");
        disclaimerContainer.classList.add('d-none');
    })
})