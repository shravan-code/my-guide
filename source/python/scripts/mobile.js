// Python mobile interactivity (<= 920px)
const pythonMobile = (() => {
    const mql = window.matchMedia('(max-width: 920px)');
    const init = () => {
        if (!mql.matches) return;
        const links = document.querySelectorAll('.menu a');
        links.forEach((link) => {
            link.addEventListener('click', () => {
                const overlay = document.getElementById('mobile-menu-overlay');
                const mobileMenu = document.getElementById('mobile-menu');
                if (overlay) overlay.classList.remove('active');
                if (mobileMenu) mobileMenu.classList.remove('open');
            });
        });
    };

    mql.addEventListener('change', (event) => {
        if (event.matches) init();
    });
    document.addEventListener('DOMContentLoaded', init);
    return { init };
})();
