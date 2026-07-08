document.addEventListener('DOMContentLoaded', () => {
    const serviceSwiper = new Swiper('.service-swiper', {
        loop: true,
        slidesPerView: 4,
        spaceBetween: 30,
        speed: 4000, // higher = slower smooth movement
        autoplay: {
            delay: 0,
            disableOnInteraction: false,
        },
        // allowTouchMove: false,
        grabCursor:true,

        breakpoints: {
            0: {
                slidesPerView: 1.2,
                spaceBetween: 15,
            },
            576: {
                slidesPerView: 2,
                spaceBetween: 20,
            },
            768: {
                slidesPerView: 3,
                spaceBetween: 25,
            },
            1200: {
                slidesPerView: 2.8,
                spaceBetween: 30,
            }
        }
    });

    const gallerySwiper = new Swiper('.gallery-swiper', {
        loop: true,
        slidesPerView: 4,
        spaceBetween: 3,
        speed: 4000, // higher = slower smooth movement
        autoplay: {
            delay: 0,
            disableOnInteraction: false,
        },
        // allowTouchMove: false,
        grabCursor:true,

        breakpoints: {
            0: {
                slidesPerView: 1.2,
            },
            576: {
                slidesPerView: 2,
            },
            768: {
                slidesPerView: 3,
            },
            1200: {
                slidesPerView: 2.8,
                spaceBetween: 3,
            }
        }
    });
    const swiperContainer = document.querySelector('.service-swiper');

    swiperContainer.addEventListener('mouseenter', () => {
        serviceSwiper.autoplay.stop();
    });

    swiperContainer.addEventListener('mouseleave', () => {
        serviceSwiper.autoplay.start();
    });
});