// Python desktop interactivity (>= 921px)
const pythonDesktop = (() => {
    const mql = window.matchMedia('(min-width: 921px)');
    const init = () => {
        if (!mql.matches) return;
        const activeItem = document.querySelector('nav.menu a.active');
        if (activeItem) {
            activeItem.scrollIntoView({ block: 'nearest' });
        }
    };
    mql.addEventListener('change', (event) => {
        if (event.matches) init();
    });
    document.addEventListener('DOMContentLoaded', init);
    return { init };
})();
