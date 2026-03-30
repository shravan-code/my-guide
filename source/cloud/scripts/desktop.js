// Cloud desktop interactivity (>=921px)
const cloudDesktop = (() => {
    const mql = window.matchMedia('(min-width: 921px)');
    const init = () => {
        if (!mql.matches) return;
        const menu = document.querySelector('.menu');
        if (!menu) return;

        const dropdowns = menu.querySelectorAll('.menu-dropdown');
        dropdowns.forEach((dd) => {
            dd.addEventListener('mouseenter', () => dd.classList.add('open'));
            dd.addEventListener('mouseleave', () => dd.classList.remove('open'));
        });
    };
    mql.addEventListener('change', (event) => {
        if (event.matches) init();
    });
    document.addEventListener('DOMContentLoaded', init);
    return { init };
})();
