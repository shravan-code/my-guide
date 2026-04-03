import os
import re

base_path = r"d:\shra1\github\my-guide"
files = [
    "source/apis/index.html",
    "source/numpy/index.html",
    "source/pandas/index.html",
    "source/python/index.html",
    "source/spark/index.html"
]

for f in files:
    path = os.path.join(base_path, f)
    # Restore the original file from git to read cleanly
    os.system(f"git checkout -- {f}")
    
    with open(path, "r", encoding="utf-8") as file:
        raw = file.read()
        
    depth = f.count('/')
    rel_path = "../" * depth
    if depth == 0: rel_path = "./"
    
    # Extract Title
    title_match = re.search(r'<title>[^|]*\|\s*(.*?)</title>', raw, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "Data Guide"
    
    # Extract Hero info
    eyebrow_match = re.search(r'(?si)<p class="eyebrow">(.*?)</p>', raw)
    eyebrow = eyebrow_match.group(1).strip() if eyebrow_match else ""
    
    h1_match = re.search(r'(?si)<h1>(.*?)</h1>', raw)
    h1 = h1_match.group(1).strip() if h1_match else title
    
    hero_copy_match = re.search(r'(?si)<p class="hero-copy">(.*?)</p>', raw)
    hero_copy = hero_copy_match.group(1).strip() if hero_copy_match else ""
    
    # Extract Inspire section content
    inspire_match = re.search(r'(?si)<section class="inspire">\s*(.*?)\s*</section>', raw)
    inspire_content = inspire_match.group(1).strip() if inspire_match else ""
    
    # Extract Tracks sections and convert
    tracks_html = ""
    tracks_matches = re.finditer(r'(?si)<section class="tracks">\s*(.*?)\s*</section>', raw)
    for tm in tracks_matches:
        track_data = tm.group(1)
        
        t_title_match = re.search(r'(?si)<h2>(.*?)</h2>', track_data)
        t_title = t_title_match.group(1).strip() if t_title_match else ""
        
        tracks_html += f'\n    <section>\n      <h2 class="section-title">{t_title}</h2>\n      <div class="section-grid">\n'
        
        card_matches = re.finditer(r'(?si)<a href="([^"]+)"[^>]*>(.*?)</a>', track_data)
        for cm in card_matches:
            href = cm.group(1)
            inner = cm.group(2)
            
            c_title_match = re.search(r'(?si)<h3[^>]*>(.*?)</h3>', inner)
            c_title = c_title_match.group(1).strip() if c_title_match else ""
            
            c_desc_match = re.search(r'(?si)<p[^>]*>(.*?)</p>', inner)
            c_desc = c_desc_match.group(1).strip() if c_desc_match else ""
            
            c_lower = c_title.lower()
            icon = "article"
            if "theory" in c_lower or "concept" in c_lower: icon = "lightbulb"
            elif "code" in c_lower or "method" in c_lower or "function" in c_lower: icon = "code"
            elif "architecture" in c_lower or "struct" in c_lower: icon = "architecture"
            elif "type" in c_lower or "data" in c_lower or "table" in c_lower or "frame" in c_lower: icon = "data_object"
            elif "roadmap" in c_lower or "path" in c_lower: icon = "map"
            
            tracks_html += f'        <a href="{href}" class="section-card">\n          <span class="material-symbols-outlined">{icon}</span>\n          <h3>{c_title}</h3>\n          <p>{c_desc}</p>\n        </a>\n'
        
        tracks_html += '      </div>\n    </section>\n'
        
    new_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Data Guide | {h1}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
  <link rel="stylesheet" href="{rel_path}shared.css" />
</head>

<body class="topic-page topic-index">
  <header class="top-nav">
    <div class="top-nav-inner">
      <a href="{rel_path}index.html" class="brand">
        <div class="brand-icon">
          <span class="material-symbols-outlined">architecture</span>
        </div>
        <span class="brand-text">Data Sheets</span>
      </a>

      <div class="nav-center">
        <div class="search-bar">
          <span class="material-symbols-outlined">search</span>
          <input type="text" class="search-input" placeholder="Search architecture, patterns, or cloud..." />
        </div>
      </div>

      <div class="nav-right">
        <button class="nav-icon-btn" id="themeToggle" onclick="toggleTheme()">
          <span class="material-symbols-outlined" id="themeIcon">dark_mode</span>
        </button>
        <a href="{rel_path}portfolios/portfolio.html" class="user-avatar">
          <img src="{rel_path}assets/images/profile-pic.jpeg" alt="User profile" />
        </a>
      </div>
    </div>
  </header>

  <main class="main-content">
    <a href="{rel_path}index.html" class="back-link">
      <span class="material-symbols-outlined">arrow_back</span>
      Back to Home
    </a>

    <header class="page-header">
      <p class="eyebrow">{eyebrow}</p>
      <h1>{h1}</h1>
      <p>{hero_copy}</p>
    </header>

    <section class="inspire">
      {inspire_content}
    </section>
{tracks_html}
  </main>

  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-left">
        <span class="footer-brand">Data Sheets</span>
        <p class="footer-copyright">&copy; 2026 Data Sheets. All rights reserved.</p>
      </div>
      <div class="footer-links">
        <a href="#">Documentation</a>
        <a href="#">Privacy</a>
        <a href="#">Terms</a>
        <a href="#">Support</a>
      </div>
    </div>
  </footer>

  <script>
    function toggleTheme() {{
      const html = document.documentElement;
      const themeIcon = document.getElementById('themeIcon');
      if (html.classList.contains('dark')) {{
        html.classList.remove('dark');
        localStorage.setItem('theme', 'light');
        themeIcon.textContent = 'dark_mode';
      }} else {{
        html.classList.add('dark');
        localStorage.setItem('theme', 'dark');
        themeIcon.textContent = 'light_mode';
      }}
    }}
    (function() {{
      const savedTheme = localStorage.getItem('theme');
      const themeIcon = document.getElementById('themeIcon');
      if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
        document.documentElement.classList.add('dark');
        themeIcon.textContent = 'light_mode';
      }} else {{
        themeIcon.textContent = 'dark_mode';
      }}
    }})();
  </script>
</body>
</html>"""
    
    with open(path, "w", encoding="utf-8") as file:
        file.write(new_html)
    print(f"RECONVERTED: {f}")
