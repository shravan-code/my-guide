const fs = require('fs');
const path = require('path');

const SOURCE_DIR = path.join(__dirname, 'source');

// Page metadata mapping
const PAGE_META = {
  'python-fundamentals.html': { title: 'Python Fundamentals', eyebrow: 'Core Skills', parent: 'python' },
  'python-oops.html': { title: 'Python OOP', eyebrow: 'Core Skills', parent: 'python' },
  'python-methods.html': { title: 'Python Methods', eyebrow: 'Core Skills', parent: 'python' },
  'memory-performance.html': { title: 'Memory & Performance', eyebrow: 'Core Skills', parent: 'python' },
  'spark-theory.html': { title: 'Spark Theory', eyebrow: 'Big Data', parent: 'spark' },
  'spark-architecture.html': { title: 'Spark Architecture', eyebrow: 'Big Data', parent: 'spark' },
  'spark-code.html': { title: 'Spark Code', eyebrow: 'Big Data', parent: 'spark' },
  'pandas-series.html': { title: 'Pandas Series', eyebrow: 'Data Processing', parent: 'pandas' },
  'pandas-dataframes.html': { title: 'Pandas DataFrames', eyebrow: 'Data Processing', parent: 'pandas' },
  'methods.html': { title: 'Methods Reference', eyebrow: 'Data Processing', parent: null },
  'numpy-arrays.html': { title: 'NumPy Arrays', eyebrow: 'Numerical Computing', parent: 'numpy' },
  'numpy-operations.html': { title: 'NumPy Operations', eyebrow: 'Numerical Computing', parent: 'numpy' },
  'numpy-basics.html': { title: 'NumPy Basics', eyebrow: 'Numerical Computing', parent: 'numpy' },
  'cloud-basics.html': { title: 'Cloud Basics', eyebrow: 'Cloud Platforms', parent: 'cloud' },
  'cloud-services.html': { title: 'Cloud Services', eyebrow: 'Cloud Platforms', parent: 'cloud' },
  'cloud-storage.html': { title: 'Cloud Storage', eyebrow: 'Cloud Platforms', parent: 'cloud' },
  'cloud-compute.html': { title: 'Cloud Compute', eyebrow: 'Cloud Platforms', parent: 'cloud' },
  'cloud-serverless.html': { title: 'Cloud Serverless', eyebrow: 'Cloud Platforms', parent: 'cloud' },
  'cloud-aws.html': { title: 'AWS', eyebrow: 'Cloud Platforms', parent: 'cloud' },
  'cloud-azure.html': { title: 'Azure', eyebrow: 'Cloud Platforms', parent: 'cloud' },
  'cloud-gcp.html': { title: 'GCP', eyebrow: 'Cloud Platforms', parent: 'cloud' },
  'cloud-topics.html': { title: 'Cloud Topics', eyebrow: 'Cloud Platforms', parent: 'cloud' },
  'data-types.html': { title: 'Data Types', eyebrow: 'Data Engineering', parent: 'data' },
  'data-formats.html': { title: 'Data Formats', eyebrow: 'Data Engineering', parent: 'data' },
  'data-quality.html': { title: 'Data Quality', eyebrow: 'Data Engineering', parent: 'data' },
  'data-pipeline.html': { title: 'Data Pipelines', eyebrow: 'Data Engineering', parent: 'data' },
  'sql-concepts.html': { title: 'SQL Concepts', eyebrow: 'Query Language', parent: 'sql' },
  'sql-joins.html': { title: 'SQL Joins', eyebrow: 'Query Language', parent: 'sql' },
  'sql-queries.html': { title: 'SQL Queries', eyebrow: 'Query Language', parent: 'sql' },
  'sql-windows.html': { title: 'SQL Windows', eyebrow: 'Query Language', parent: 'sql' },
  'sql-subqueries.html': { title: 'SQL Subqueries', eyebrow: 'Query Language', parent: 'sql' },
  'sql-modelling.html': { title: 'SQL Modelling', eyebrow: 'Query Language', parent: 'sql' },
  'sql-methods.html': { title: 'SQL Methods', eyebrow: 'Query Language', parent: 'sql' },
  'concepts.html': { title: 'API Concepts', eyebrow: 'API Development', parent: 'apis' },
  'types.html': { title: 'API Types', eyebrow: 'API Development', parent: 'apis' },
  'airflow.html': { title: 'Airflow', eyebrow: 'Data Tools', parent: 'tools' },
  'dbt.html': { title: 'dbt', eyebrow: 'Data Tools', parent: 'tools' },
  'kafka.html': { title: 'Kafka', eyebrow: 'Data Tools', parent: 'tools' },
  'libraries-hub.html': { title: 'Libraries Hub', eyebrow: 'Libraries', parent: 'libraries' },
};

// Get relative path to shared.css based on file location
function getSharedCssPath(filePath) {
  const relative = path.relative(SOURCE_DIR, filePath);
  const depth = relative.split(path.sep).length - 1;
  return '../'.repeat(depth) + 'shared.css';
}

// Get relative path to index.html based on file location
function getIndexHtmlPath(filePath) {
  const relative = path.relative(SOURCE_DIR, filePath);
  const parts = relative.split(path.sep);
  const parentDir = parts[0];
  const depth = parts.length - 1;
  // depth 1 = same dir as index (e.g. python/fundamentals.html -> index.html)
  // depth 2 = one level deeper (e.g. portfolios/projects/x.html -> ../portfolios/index.html)
  if (depth === 1) {
    return 'index.html';
  }
  return '../'.repeat(depth - 1) + parentDir + '/index.html';
}

// Extract content between <main> and </main> from existing file
function extractMainContent(html) {
  const mainMatch = html.match(/<main[^>]*>([\s\S]*?)<\/main>/i);
  if (!mainMatch) return null;
  
  let content = mainMatch[1];
  
  // Remove page-wrap wrapper if present
  const pageWrapMatch = content.match(/<div\s+class="page-wrap"[^>]*>([\s\S]*)<\/div>/i);
  if (pageWrapMatch) {
    content = pageWrapMatch[1];
  }
  
  return content.trim();
}

// Extract title from existing file
function extractTitle(html) {
  const titleMatch = html.match(/<title>(.*?)<\/title>/i);
  if (titleMatch) {
    const title = titleMatch[1].replace('*d@ta# | ', '').replace(' | Data Sheets', '');
    return title;
  }
  return 'Page';
}

// Extract eyebrow from existing file
function extractEyebrow(html) {
  const eyebrowMatch = html.match(/<p\s+class="eyebrow"[^>]*>(.*?)<\/p>/i);
  if (eyebrowMatch) {
    return eyebrowMatch[1];
  }
  return null;
}

// Extract description from existing file
function extractDescription(html) {
  const descMatch = html.match(/<p\s+class="hero-copy"[^>]*>(.*?)<\/p>/i);
  if (descMatch) {
    return descMatch[1].replace('A focused guide to ', '').replace('A complete guide to ', '').replace(/\.$/, '');
  }
  return null;
}

// Build new HTML for content pages
function buildContentPage(filePath, content, meta) {
  const sharedCss = getSharedCssPath(filePath);
  const title = meta.title || extractTitle(content);
  const eyebrow = meta.eyebrow || extractEyebrow(content) || 'Guide';
  const description = meta.description || extractDescription(content) || title;
  
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${title} | Data Sheets</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
  <link rel="stylesheet" href="${sharedCss}" />
  <style>
    /* Page-specific styles */
    .content-section { margin-bottom: var(--space-8); }
    .content-section h2 { font-size: 1.5rem; margin-bottom: var(--space-4); }
    .content-section h3 { font-size: 1.2rem; margin: var(--space-4) 0 var(--space-2); }
    .content-section p { margin-bottom: var(--space-4); line-height: 1.7; }
    .content-section ul, .content-section ol { padding-left: 1.25rem; margin-bottom: var(--space-4); }
    .content-section li { margin-bottom: var(--space-2); color: var(--on-surface-variant); }
    .content-section code { background: var(--surface-container); padding: var(--space-1) var(--space-2); border-radius: var(--radius-sm); font-size: 0.85rem; font-family: 'Courier New', monospace; color: var(--primary); }
    .content-section pre { background: var(--surface-container); padding: var(--space-4); border-radius: var(--radius-lg); overflow-x: auto; margin-bottom: var(--space-4); }
    .content-section pre code { background: none; padding: 0; color: var(--on-surface); }
    .content-section table { width: 100%; border-collapse: collapse; margin-bottom: var(--space-4); }
    .content-section th, .content-section td { padding: var(--space-2) var(--space-3); border: 1px solid var(--outline-variant); text-align: left; }
    .content-section th { background: var(--surface-container); font-weight: 600; }
  </style>
</head>
<body>
  <header class="top-nav">
    <div class="top-nav-inner">
      <div class="brand">
        <a href="${getIndexHtmlPath(filePath)}" class="brand">
          <div class="brand-icon"><span class="material-symbols-outlined">architecture</span></div>
          <span class="brand-text">Data Sheets</span>
        </a>
      </div>
      <div class="nav-right">
        <button class="nav-icon-btn" onclick="history.back()">
          <span class="material-symbols-outlined">arrow_back</span>
        </button>
        <button class="nav-icon-btn" id="themeToggle" onclick="toggleTheme()">
          <span class="material-symbols-outlined" id="themeIcon">dark_mode</span>
        </button>
        <div class="user-avatar">
          <img src="../../assets/images/profile-pic.jpeg" alt="User profile" />
        </div>
      </div>
    </div>
  </header>

  <main class="main-content">
    <a href="${getIndexHtmlPath(filePath)}" class="back-link">
      <span class="material-symbols-outlined">arrow_back</span>
      Back to ${eyebrow}
    </a>

    <header class="page-header">
      <p class="eyebrow">${eyebrow}</p>
      <h1>${title}</h1>
      <p>${description}</p>
    </header>

    <div class="content-card">
      ${content}
    </div>

    <footer class="footer">
      <span class="footer-brand">Data Sheets</span>
      <div class="footer-links">
        <a href="../../index.html">Home</a>
        <a href="../portfolios/portfolio.html">Profile</a>
        <a href="../roadmaps/roadmap.html">Roadmap</a>
      </div>
    </footer>
  </main>

  <button id="scrollToTop" class="scroll-to-top" aria-label="Scroll to top">
    <span class="material-symbols-outlined">arrow_upward</span>
  </button>

  <script>
    (function() {
      const saved = localStorage.getItem('theme');
      if (saved === 'dark') document.documentElement.classList.add('dark');
    })();
    function toggleTheme() {
      const html = document.documentElement;
      const icon = document.getElementById('themeIcon');
      if (html.classList.contains('dark')) {
        html.classList.remove('dark');
        icon.textContent = 'dark_mode';
        localStorage.setItem('theme', 'light');
      } else {
        html.classList.add('dark');
        icon.textContent = 'light_mode';
        localStorage.setItem('theme', 'dark');
      }
    }
    (function() {
      const saved = localStorage.getItem('theme');
      const icon = document.getElementById('themeIcon');
      icon.textContent = saved === 'dark' ? 'light_mode' : 'dark_mode';
    })();
    const stt = document.getElementById('scrollToTop');
    window.addEventListener('scroll', () => { stt.classList.toggle('visible', window.pageYOffset > 400); });
    stt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  </script>
</body>
</html>`;
}

// Process all HTML files
function processFiles() {
  const files = [];
  
  function walkDir(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walkDir(fullPath);
      } else if (entry.name.endsWith('.html') && entry.name !== 'index.html') {
        files.push(fullPath);
      }
    }
  }
  
  walkDir(SOURCE_DIR);
  
  console.log(`Found ${files.length} HTML files to process`);
  
  let processed = 0;
  let skipped = 0;
  
  for (const filePath of files) {
    try {
      const html = fs.readFileSync(filePath, 'utf8');
      const content = extractMainContent(html);
      
      if (!content) {
        console.log(`  SKIP (no main content): ${path.relative(SOURCE_DIR, filePath)}`);
        skipped++;
        continue;
      }
      
      const fileName = path.basename(filePath);
      const meta = PAGE_META[fileName] || {
        title: extractTitle(html),
        eyebrow: extractEyebrow(html) || 'Guide',
        parent: null
      };
      
      const newHtml = buildContentPage(filePath, content, meta);
      fs.writeFileSync(filePath, newHtml, 'utf8');
      
      console.log(`  OK: ${path.relative(SOURCE_DIR, filePath)}`);
      processed++;
    } catch (err) {
      console.error(`  ERROR: ${path.relative(SOURCE_DIR, filePath)} - ${err.message}`);
    }
  }
  
  console.log(`\nDone! Processed: ${processed}, Skipped: ${skipped}`);
}

processFiles();
