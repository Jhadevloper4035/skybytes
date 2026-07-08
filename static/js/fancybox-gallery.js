
Fancybox.bind("[data-fancybox]", {
    // General
    animated: true,
    showClass: "f-fadeIn",
    hideClass: "f-fadeOut",
    dragToClose: true,
    closeButton: "top",

    // Navigation
    infinite: true,
    keyboard: {
        Escape: "close",
        Delete: "close",
        Backspace: "close",
        PageUp: "next",
        PageDown: "prev",
        ArrowUp: "prev",
        ArrowDown: "next",
        ArrowRight: "next",
        ArrowLeft: "prev",
    },

    // Images
    Images: {
        // zoom: true,
    },

    // Thumbnails
    Thumbs: {
        autoStart: false,
    },

    // Toolbar
    Toolbar: {
        display: {
            left: [],

            middle: [
                "counter",
            ],

            right: [
                "zoom",
                "slideshow",
                "fullscreen",
                "thumbs",
                "close",
            ],
        },
    },

    // Caption
    caption: function (fancybox, slide) {
        return slide.caption || "";
    },


});