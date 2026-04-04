document.addEventListener("DOMContentLoaded", () => {
    const searchInputs = document.querySelectorAll('.search-input');
    if (!searchInputs.length) return;

    // Create dropdown container
    const dropdown = document.createElement('div');
    dropdown.className = 'search-dropdown';
    Object.assign(dropdown.style, {
        position: 'absolute',
        top: '100%',
        left: 0,
        right: 0,
        background: 'var(--surface-container-lowest)',
        border: '1px solid var(--outline-variant)',
        borderRadius: 'var(--radius-md)',
        maxHeight: '300px',
        overflowY: 'auto',
        zIndex: 1000,
        display: 'none',
        boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
        marginTop: '8px'
    });

    searchInputs.forEach(input => {
        const parent = input.parentElement;
        parent.style.position = 'relative';
        parent.appendChild(dropdown);

        input.addEventListener('input', (e) => {
            const query = e.target.value.trim().toLowerCase();
            if(!query) {
                dropdown.style.display = 'none';
                return;
            }
            
            // grab headers
            const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4'));
            
            dropdown.innerHTML = '';
            let matched = 0;

            headings.forEach(h => {
                const text = (h.textContent || '').trim();
                // Avoid empty headers or visually hidden
                if(text && text.toLowerCase().includes(query)) {
                    matched++;
                    const item = document.createElement('div');
                    Object.assign(item.style, {
                        padding: '12px 16px',
                        cursor: 'pointer',
                        borderBottom: '1px solid var(--surface-container)',
                        color: 'var(--on-surface)',
                        fontSize: '0.875rem',
                        transition: 'background 0.2s ease'
                    });
                    item.textContent = text;
                    item.addEventListener('mouseover', () => item.style.background = 'var(--surface-container-high)');
                    item.addEventListener('mouseout', () => item.style.background = 'transparent');
                    item.addEventListener('click', () => {
                        h.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        dropdown.style.display = 'none';
                        input.value = '';
                    });
                    dropdown.appendChild(item);
                }
            });

            if(matched > 0) {
                dropdown.style.display = 'block';
            } else {
                dropdown.style.display = 'none';
            }
        });

        document.addEventListener('click', (e) => {
            if(!parent.contains(e.target)) {
                dropdown.style.display = 'none';
            }
        });
    });
});
