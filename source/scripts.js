
document.addEventListener("DOMContentLoaded", () => {
    // ------------------------------------------
    // 1. UNIVERSAL SEARCH AUTOCOMPLETE
    // ------------------------------------------
    const searchInputs = document.querySelectorAll('.search-input');
    if (searchInputs.length > 0) {
        const dropdown = document.createElement('div');
        dropdown.className = 'search-dropdown';
        Object.assign(dropdown.style, {
            position: 'absolute', top: '100%', left: 0, right: 0,
            background: 'var(--surface-container-lowest)',
            border: '1px solid var(--outline-variant)',
            borderRadius: 'var(--radius-md)', maxHeight: '300px',
            overflowY: 'auto', zIndex: 1000, display: 'none',
            boxShadow: '0 8px 24px rgba(0,0,0,0.12)', marginTop: '8px'
        });

        searchInputs.forEach(input => {
            const parent = input.parentElement;
            parent.style.position = 'relative';
            parent.appendChild(dropdown);

            input.addEventListener('input', (e) => {
                const query = e.target.value.trim().toLowerCase();
                if(!query) { dropdown.style.display = 'none'; return; }
                const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4'));
                dropdown.innerHTML = '';
                let matched = 0;
                headings.forEach(h => {
                    const text = (h.textContent || '').trim();
                    if(text && text.toLowerCase().includes(query)) {
                        matched++;
                        const item = document.createElement('div');
                        Object.assign(item.style, {
                            padding: '12px 16px', cursor: 'pointer',
                            borderBottom: '1px solid var(--surface-container)',
                            color: 'var(--on-surface)', fontSize: '0.875rem',
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
                dropdown.style.display = (matched > 0) ? 'block' : 'none';
            });
            document.addEventListener('click', (e) => {
                if(!parent.contains(e.target)) dropdown.style.display = 'none';
            });
        });
    }
});

// ------------------------------------------
// 2. COLLAPSIBLE SECTIONS FOR COMPARE PAGES
// ------------------------------------------
window.initializeCollapsibleSections = function(container, selector) {
    const headings = container.querySelectorAll(selector);
    headings.forEach(heading => {
        heading.style.cursor = 'pointer';
        heading.style.display = 'flex';
        heading.style.justifyContent = 'space-between';
        heading.style.alignItems = 'center';
        heading.style.padding = '0.75rem 1rem';
        heading.style.background = 'var(--surface-container)';
        heading.style.borderRadius = 'var(--radius-md)';
        heading.style.marginBottom = '0.5rem';
        
        let nextEl = heading.nextElementSibling;
        const contentEls = [];
        const headingTag = heading.tagName.toLowerCase();
        const getLevel = tag => parseInt(tag.substring(1));
        const currentLevel = getLevel(headingTag);
        
        while (nextEl) {
            const nextTag = nextEl.tagName.toLowerCase();
            if (nextTag.match(/^h[1-6]$/) && getLevel(nextTag) <= currentLevel) break;
            contentEls.push(nextEl);
            nextEl = nextEl.nextElementSibling;
        }
        
        const wrapper = document.createElement('div');
        wrapper.className = 'collapsible-content';
        wrapper.style.display = 'none'; 
        wrapper.style.padding = '1rem';
        heading.parentNode.insertBefore(wrapper, contentEls[0]);
        contentEls.forEach(el => wrapper.appendChild(el));
        
        const icon = document.createElement('span');
        icon.className = 'material-symbols-outlined';
        icon.textContent = 'expand_more';
        icon.style.transition = 'transform 0.3s ease';
        heading.appendChild(icon);
        
        heading.addEventListener('click', () => {
            const isHidden = wrapper.style.display === 'none';
            wrapper.style.display = isHidden ? 'block' : 'none';
            icon.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
        });
    });
};

// ------------------------------------------
// 3. MOBILE DRAWER LOGIC
// ------------------------------------------
window.toggleDrawer = function() {
    const drawer = document.querySelector('.drawer');
    const overlay = document.querySelector('.drawer-overlay');
    if (drawer && overlay) {
        drawer.classList.toggle('open');
        overlay.classList.toggle('open');
        document.body.classList.toggle('drawer-open');
    }
};

window.closeDrawer = function() {
    const drawer = document.querySelector('.drawer');
    const overlay = document.querySelector('.drawer-overlay');
    if (drawer && overlay) {
        drawer.classList.remove('open');
        overlay.classList.remove('open');
        document.body.classList.remove('drawer-open');
    }
};

// ------------------------------------------
// 4. THEME TOGGLE LOGIC
// ------------------------------------------
window.toggleTheme = function() {
    const html = document.documentElement;
    const isDark = html.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    
    // Update icon
    const themeIcon = document.getElementById('themeIcon');
    if (themeIcon) {
        themeIcon.textContent = isDark ? 'light_mode' : 'dark_mode';
    }
};

// Initialize theme and events on load
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const isDark = savedTheme === 'dark' || (!savedTheme && prefersDark);
    
    if (isDark) {
        document.documentElement.classList.add('dark');
        const themeIcon = document.getElementById('themeIcon');
        if (themeIcon) {
            themeIcon.textContent = 'light_mode';
        }
    }

    // Scroll to Top visibility
    const scrollToTopBtn = document.getElementById('scrollToTop');
    if (scrollToTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                scrollToTopBtn.classList.add('visible');
            } else {
                scrollToTopBtn.classList.remove('visible');
            }
        });

        scrollToTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
});


// ------------------------------------------
// 5. PROVIDER TABS LOGIC
// ------------------------------------------
window.showProvider = function(provider) {
    document.querySelectorAll('.provider-tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.provider-content').forEach(content => content.classList.remove('active'));
    
    // Find the tab button
    const tabs = document.querySelectorAll('.provider-tab');
    tabs.forEach(tab => {
        if (tab.getAttribute('onclick')?.includes(`'${provider}'`)) {
            tab.classList.add('active');
        }
    });
    
    const content = document.getElementById(`${provider}-content`);
    if (content) content.classList.add('active');
};

