// Cloud mobile interactivity (<=920px)
const cloudMobile = (() => {
    const mql = window.matchMedia('(max-width: 920px)');
    const init = () => {
        if (!mql.matches) return;
        const mobileButtons = document.querySelectorAll('.track-grid a, .menu a');
        mobileButtons.forEach((btn) => {
            btn.addEventListener('click', () => {
                document.body.style.overflow = '';
            });
        });
    };
    mql.addEventListener('change', (event) => {
        if (event.matches) init();
    });
    document.addEventListener('DOMContentLoaded', init);
    return { init };
})();
