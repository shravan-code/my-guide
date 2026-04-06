
document.addEventListener("DOMContentLoaded", () => {
    const toolOptions = document.getElementById('toolOptions');
    const categoryOptions = document.getElementById('categoryOptions');
    const comparisonContainer = document.getElementById('comparisonContainer');
    const selectionSummary = document.getElementById('selectionSummary');
    const comparisonFilters = document.getElementById('comparisonFilters');
    const emptyState = document.getElementById('emptyState');

    let comparisonData = [];
    let selectedTools = [];
    let selectedCategories = [];

    // 1. Fetch Data
    fetch('comparison-data.json')
        .then(response => response.json())
        .then(data => {
            comparisonData = data;
            initializeFilters();
        })
        .catch(err => console.error('Error loading comparison data:', err));

    function initializeFilters() {
        // Extract all unique tools from first category scenarios
        const tools = Object.keys(comparisonData[0].scenarios[0]).filter(k => k !== 'scenario');
        
        // Populate Tools
        tools.forEach(tool => {
            const group = document.createElement('div');
            group.className = 'checkbox-group';
            
            const input = document.createElement('input');
            input.type = 'checkbox';
            input.id = `tool-${tool}`;
            input.value = tool;
            input.className = 'pill-input';
            input.checked = false; // Default off
            
            const label = document.createElement('label');
            label.htmlFor = `tool-${tool}`;
            label.className = 'tool-label';
            label.textContent = tool.charAt(0).toUpperCase() + tool.slice(1);
            
            group.appendChild(input);
            group.appendChild(label);
            toolOptions.appendChild(group);
        });

        // Populate Categories
        comparisonData.forEach((cat, idx) => {
            const group = document.createElement('div');
            group.className = 'checkbox-group';
            
            const input = document.createElement('input');
            input.type = 'checkbox';
            input.id = `cat-${idx}`;
            input.value = idx;
            input.className = 'pill-input';
            input.checked = false; // Default off
            
            const label = document.createElement('label');
            label.htmlFor = `cat-${idx}`;
            label.className = 'category-label';
            label.textContent = cat.category;
            
            group.appendChild(input);
            group.appendChild(label);
            categoryOptions.appendChild(group);
        });

        updateSummary();
        renderComparisons();
    }

    function updateSummary() {
        const toolCount = Array.from(toolOptions.querySelectorAll('input:checked')).length;
        const catCount = Array.from(categoryOptions.querySelectorAll('input:checked')).length;
        selectionSummary.textContent = `${toolCount} tools · ${catCount} categories selected`;
    }

    function renderComparisons() {
        const activeTools = Array.from(toolOptions.querySelectorAll('input:checked')).map(i => i.value);
        const activeCatIndices = Array.from(categoryOptions.querySelectorAll('input:checked')).map(i => parseInt(i.value));

        comparisonContainer.innerHTML = '';

        if (activeTools.length === 0 || activeCatIndices.length === 0) {
            emptyState.hidden = false;
            return;
        }
        emptyState.hidden = true;

        activeCatIndices.forEach(idx => {
            const cat = comparisonData[idx];
            const section = document.createElement('section');
            section.className = 'comparison-section reveal in';
            
            const title = document.createElement('h2');
            title.className = 'comparison-title';
            title.textContent = cat.category;
            section.appendChild(title);

            const grid = document.createElement('div');
            grid.className = 'comparison-grid';

            cat.scenarios.forEach(scenario => {
                const scenarioStack = document.createElement('div');
                scenarioStack.className = 'scenario-card';

                const name = document.createElement('div');
                name.className = 'scenario-name';
                name.textContent = scenario.scenario;
                scenarioStack.appendChild(name);

                const toolGrid = document.createElement('div');
                toolGrid.className = 'tool-grid';

            activeTools.forEach(tool => {
                const toolCard = document.createElement('div');
                toolCard.className = 'tool-cell';
                
                const header = document.createElement('div');
                header.className = 'tool-cell-header';
                header.innerHTML = `<div class="tool-chip">${tool.toUpperCase()}</div>`;
                
                const codeBlock = document.createElement('div');
                codeBlock.className = 'code-block';
                
                const code = document.createElement('code');
                code.className = 'code-cell';
                const val = scenario[tool] || 'N/A';
                code.innerHTML = highlightCode(val);
                
                codeBlock.appendChild(code);
                toolCard.appendChild(header);
                toolCard.appendChild(codeBlock);
                toolGrid.appendChild(toolCard);
            });

                scenarioStack.appendChild(toolGrid);
                grid.appendChild(scenarioStack);
            });

            section.appendChild(grid);
            comparisonContainer.appendChild(section);
        });
    }

    comparisonFilters.addEventListener('submit', (e) => {
        e.preventDefault();
        updateSummary();
        renderComparisons();
        window.scrollTo({ top: comparisonContainer.offsetTop - 100, behavior: 'smooth' });
    });

    function highlightCode(text) {
        if (!text || text === 'N/A') return text;
        
        let html = text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        const placeholders = [];
        
        // 1. Strings
        html = html.replace(/(['"])(?:(?!\1|\\).|\\.)*\1/g, (match) => {
            const id = `__STR_${placeholders.length}__`;
            placeholders.push({ id, content: `<span class="string">${match}</span>` });
            return id;
        });
        
        // 2. Comments
        html = html.replace(/(#.*$|--.*$|\/\/.*$)/gm, (match) => {
            const id = `__COM_${placeholders.length}__`;
            placeholders.push({ id, content: `<span class="comment">${match}</span>` });
            return id;
        });

        // 3. Decorators
        html = html.replace(/(@\w+)/g, '<span class="decorator">$1</span>');
        
        // 4. Keywords
        const keywords = /\b(def|class|if|else|elif|for|while|return|import|as|from|try|except|with|None|True|False|lambda|SELECT|FROM|WHERE|GROUP BY|ORDER BY|JOIN|LEFT|RIGHT|INNER|ON|CREATE|TABLE|INSERT|INTO|VALUES|UPDATE|SET|DELETE|DROP|ALTER|ADD|CONSTRAINT|PRIMARY|KEY|FOREIGN|REFERENCES|NOT|NULL|UNIQUE|DEFAULT|CHECK|INDEX|VIEW|PROCEDURE|FUNCTION|TRIGGER|DATABASE|USE|SHOW|DESCRIBE|EXPLAIN|LIMIT|OFFSET|FETCH|UNION|ALL|INTERSECT|EXCEPT|CASE|WHEN|THEN|END|CAST|COALESCE|NULLIF|EXTRACT|DATE|TIME|TIMESTAMP|INTERVAL|BOOLEAN|INTEGER|REAL|DOUBLE|PRECISION|CHAR|VARCHAR|TEXT|BLOB|CLOB|XML|ARRAY|MAP|STRUCT|JSON|BYTEA|SERIAL|BIGSERIAL|SMALLSERIAL|UUID|INET|CIDR|MACADDR|BOX|CIRCLE|LINE|LSEG|PATH|POINT|POLYGON|TSQUERY|TSVECTOR|VARBIT|BIT|VARYING|WITHOUT|WITH|ZONE)\b/gi;
        html = html.replace(keywords, '<span class="keyword">$&</span>');
        
        // 5. Functions
        html = html.replace(/(\w+)(?=\()/g, '<span class="function">$1</span>');
        
        // 6. Numbers
        html = html.replace(/\b(\d+)\b/g, '<span class="number">$&</span>');
        
        placeholders.forEach(p => {
            html = html.replace(p.id, p.content);
        });
        
        return html;
    }

    comparisonFilters.addEventListener('reset', () => {
        setTimeout(() => {
            updateSummary();
            renderComparisons();
        }, 10);
    });
});
