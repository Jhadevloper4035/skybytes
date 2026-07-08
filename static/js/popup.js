document.addEventListener("DOMContentLoaded", () => {
    const popUp = document.getElementById('popUp');
    const popupBox = document.querySelector('.popup-form');
    const closeBtn = document.querySelector('.popup-close');
    const openBtn = document.querySelectorAll('.open-popup');
    const leadForm = document.getElementById('leadForm');
    const leadProjectSlug = document.getElementById('leadProjectSlug');
    const leadSource = document.getElementById('leadSource');
    const leadFormError = document.getElementById('leadFormError');
    const currentPage = window.location.pathname;

    if (currentPage.includes("projects.html")) {
        setTimeout(() => {
            popUp.classList.remove('d-none');
        }, 3000);
    }

    function closePopup() {
        popUp.classList.add('d-none');
    }

    function resetForm() {
        if (leadForm) {
            leadForm.reset();
            leadFormError.style.display = 'none';
            const submitBtn = document.getElementById('leadSubmitBtn');
            if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'REQUEST A CALL BACK'; }
        }
    }

    closeBtn.addEventListener('click', () => { closePopup(); resetForm(); });
    popUp.addEventListener('click', (e) => {
        if (!popupBox.contains(e.target)) { closePopup(); resetForm(); }
    });
    document.addEventListener('keydown', (e) => {
        if (e.key === "Escape") { closePopup(); resetForm(); }
    });

    if (openBtn) {
        openBtn.forEach(btn => btn.addEventListener('click', () => {
            resetForm();
            // Set source from data attribute (default: website)
            const src = btn.dataset.source || 'website';
            if (leadSource) leadSource.value = src;
            // Set project slug from page-level variable
            if (leadProjectSlug && window.currentProjectSlug) {
                leadProjectSlug.value = window.currentProjectSlug;
            }
            popUp.classList.remove('d-none');
        }));
    }

    // AJAX form submission
    if (leadForm) {
        leadForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const url = window.submitLeadUrl;
            if (!url) {
                leadFormError.style.display = 'block';
                leadFormError.querySelector('p').textContent = 'Something went wrong. Please try again later.';
                return;
            }

            const name = document.getElementById('name').value.trim();
            const phone = document.getElementById('phone').value.trim();
            if (!name || !phone) {
                leadFormError.style.display = 'block';
                leadFormError.querySelector('p').textContent = 'Please enter your name and phone number.';
                return;
            }

            const submitBtn = document.getElementById('leadSubmitBtn');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';

            const formData = new FormData(leadForm);

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    const formBox = leadForm.closest('.form-box');
                    if (formBox) {
                        formBox.innerHTML = '<div style="padding:40px 20px;text-align:center;"><h3 style="color:#1a6e8e;">Thank You!</h3><p style="color:#555;margin-top:12px;">We have received your enquiry. Our team will contact you shortly.</p></div>';
                    }
                    setTimeout(closePopup, 3000);
                } else {
                    leadFormError.style.display = 'block';
                    leadFormError.querySelector('p').textContent = data.error || 'Something went wrong. Please try again.';
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'REQUEST A CALL BACK';
                }
            })
            .catch(() => {
                leadFormError.style.display = 'block';
                leadFormError.querySelector('p').textContent = 'Network error. Please try again.';
                submitBtn.disabled = false;
                submitBtn.textContent = 'REQUEST A CALL BACK';
            });
        });
    }
});
