# Batch convert legacy pages to new design system
# This script replaces the old head/body/footer shell with the new Architectural Scholar design

param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath,
    
    [Parameter(Mandatory=$true)]
    [string]$PageTitle,
    
    [Parameter(Mandatory=$true)]
    [string]$BackLabel,
    
    [Parameter(Mandatory=$true)]
    [string]$BackHref,
    
    [string]$PageDescription = ""
)

$content = Get-Content $FilePath -Raw

# Extract topic sections (the actual content between hero and page-wrap close)
$heroEnd = $content.IndexOf("</section>`r`n`r`n      <!-- Section 1")
if ($heroEnd -eq -1) {
    $heroEnd = $content.IndexOf("</section>`n`n      <!-- Section 1")
}
if ($heroEnd -eq -1) {
    # Try finding first topic-section
    $heroEnd = $content.IndexOf('<section class="topic-section"')
}
$pageWrapClose = $content.IndexOf("    </div>`r`n  </main>")
if ($pageWrapClose -eq -1) {
    $pageWrapClose = $content.IndexOf("    </div>`n  </main>")
}

if ($heroEnd -eq -1 -or $pageWrapClose -eq -1) {
    Write-Error "Could not find content boundaries in $FilePath"
    exit 1
}

# Find the actual start of first topic-section
$contentStart = $content.IndexOf('<section class="topic-section"', $heroEnd)
if ($contentStart -eq -1) {
    $contentStart = $content.IndexOf("<!-- Section 1", $heroEnd)
}

$contentBody = $content.Substring($contentStart, $pageWrapClose - $contentStart)
# Clean up leading whitespace (reduce from 6-space indent to 4-space)
$contentBody = $contentBody -replace '(?m)^      ', '    '

$newPage = @"
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Data Guide | $PageTitle</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" />
  <link rel="stylesheet" href="../shared.css" />
</head>

<body class="topic-page">
  <header class="top-nav">
    <div class="top-nav-inner">
      <a href="../../index.html" class="brand">
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
        <a href="../portfolios/portfolio.html" class="user-avatar">
          <img src="../../assets/images/profile-pic.jpeg" alt="User profile" />
        </a>
      </div>
    </div>
  </header>

  <main class="main-content">
    <header class="page-header page-header--row">
      <a href="$BackHref" class="back-link back-link--round" aria-label="$BackLabel">
        <span class="material-symbols-outlined">arrow_back</span>
      </a>
      <div class="page-header-inner">
        <h1>$PageTitle</h1>
        <p>$PageDescription</p>
      </div>
    </header>

    $contentBody

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
  </main>

  <script>
    function toggleTheme() {
      const html = document.documentElement;
      const themeIcon = document.getElementById('themeIcon');
      if (html.classList.contains('dark')) {
        html.classList.remove('dark');
        localStorage.setItem('theme', 'light');
        themeIcon.textContent = 'dark_mode';
      } else {
        html.classList.add('dark');
        localStorage.setItem('theme', 'dark');
        themeIcon.textContent = 'light_mode';
      }
    }
    (function() {
      const savedTheme = localStorage.getItem('theme');
      const themeIcon = document.getElementById('themeIcon');
      if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
        themeIcon.textContent = 'light_mode';
      } else {
        themeIcon.textContent = 'dark_mode';
      }
    })();
  </script>
</body>
</html>
"@

Set-Content -Path $FilePath -Value $newPage -NoNewline
Write-Output "Converted: $FilePath"
