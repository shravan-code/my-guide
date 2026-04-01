# PowerShell script to REVERT the bad update and then re-apply correctly
# First revert by using git, then re-apply with correct depth calculation

$sourceDir = "d:\shra1\github\my-guide\source"

# Revert all HTML files to git state
Write-Host "Reverting HTML files..."

$htmlFiles = Get-ChildItem -Path $sourceDir -Recurse -Filter "*.html"

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    
    # Remove incorrectly added CSS link
    $content = $content -replace '  <link rel="stylesheet" href="[\.\/]*sidebar-nav\.css" />\r?\n', ''
    
    # Remove incorrectly added JS script
    $content = $content -replace '<script src="[\.\/]*sidebar-nav\.js"></script>\r?\n', ''
    
    # Restore body classes - remove home-with-sidebar that was added
    $content = $content -replace '<body class="home-with-sidebar with-sidebar"', '<body class="with-sidebar no-topbar"'
    $content = $content -replace '<body class="home-with-sidebar with-sidebar "', '<body class="with-sidebar no-topbar"'
    
    [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.UTF8Encoding]::new($false))
}

Write-Host "Reverted. Now re-applying with correct paths..."

# Re-read files and apply correctly
$htmlFiles = Get-ChildItem -Path $sourceDir -Recurse -Filter "*.html"

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    
    # Skip if somehow still has sidebar-nav references
    if ($content -match 'sidebar-nav\.css') {
        Write-Host "SKIP (still has sidebar-nav): $($file.Name)"
        continue
    }
    
    # Compute depth relative to source/ directory
    $relDir = $file.DirectoryName
    if ($relDir -eq $sourceDir) {
        # File directly in source/ (shouldn't happen for HTML but handle it)
        $depth = 0
    } else {
        $relPath = $relDir.Substring($sourceDir.Length + 1).Replace('\', '/')
        $depth = ($relPath -split '/').Count
    }
    
    # Build relative path prefix to source/ directory
    # depth=1 means source/cloud/ -> prefix is "../"
    # depth=2 means source/portfolios/projects/ -> prefix is "../../"
    $prefix = ''
    for ($i = 0; $i -lt $depth; $i++) {
        $prefix += '../'
    }
    if ($prefix -eq '') { $prefix = './' }
    
    Write-Host "Processing: $($file.DirectoryName.Substring($sourceDir.Length + 1))\$($file.Name) (depth=$depth, prefix=$prefix)"
    
    # 1. Add CSS link before </head>
    $cssLink = "  <link rel=`"stylesheet`" href=`"${prefix}sidebar-nav.css`" />"
    $content = $content -replace '(</head>)', "$cssLink`n`$1"
    
    # 2. Add JS script before </body>
    $jsScript = "<script src=`"${prefix}sidebar-nav.js`"></script>"
    $content = $content -replace '(</body>)', "$jsScript`n`$1"
    
    # 3. Update body class
    if ($content -match '<body\s+class="([^"]*)"') {
        $existingClasses = $Matches[1]
        # Remove 'no-topbar' class
        $newClasses = $existingClasses -replace '\bno-topbar\b', ''
        $newClasses = $newClasses.Trim()
        if ($newClasses -ne '') {
            $newClasses = "home-with-sidebar $newClasses"
        } else {
            $newClasses = "home-with-sidebar"
        }
        $newClasses = ($newClasses -replace '\s+', ' ').Trim()
        $content = $content -replace '<body\s+class="[^"]*"', "<body class=`"$newClasses`""
    }
    elseif ($content -match '<body>') {
        $content = $content -replace '<body>', '<body class="home-with-sidebar">'
    }
    
    [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.UTF8Encoding]::new($false))
    Write-Host "  Updated: $($file.Name)"
}

Write-Host "`nDone! All HTML files updated with correct paths."
