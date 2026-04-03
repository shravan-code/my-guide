# Batch convert all legacy sub-pages to new design system
# This script reads each file, extracts the topic-section content,
# and wraps it in the new Architectural Scholar shell

$basePath = "d:\shra1\github\my-guide"

# Define all files to convert with their metadata
# Format: Path, Title, Description, BackHref, Category (for nav depth)
$pages = @(
    # SQL sub-pages (source/sql/)
    @{P="source\sql\sql-concepts.html"; T="SQL Concepts"; D="Fundamentals, data types, and RDBMS basics."; B="index.html"}
    @{P="source\sql\sql-modelling.html"; T="Data Modelling"; D="Normalization, star schema, and snowflake design patterns."; B="index.html"}
    @{P="source\sql\sql-queries.html"; T="SQL Queries"; D="SELECT, WHERE, GROUP BY, ORDER BY - essential query patterns."; B="index.html"}
    @{P="source\sql\sql-methods.html"; T="SQL Methods"; D="String, date, and aggregate functions for data manipulation."; B="index.html"}
    @{P="source\sql\sql-joins.html"; T="SQL Joins"; D="INNER, LEFT, RIGHT, and FULL joins explained with examples."; B="index.html"}
    @{P="source\sql\sql-subqueries.html"; T="Subqueries"; D="Nested queries, CTEs, and correlated subqueries."; B="index.html"}
    @{P="source\sql\sql-windows.html"; T="Window Functions"; D="ROW_NUMBER, RANK, LAG, LEAD - analytical window functions."; B="index.html"}
    
    # Python sub-pages (source/python/)
    @{P="source\python\index.html"; T="Python"; D="Master Python from fundamentals to advanced patterns."; B="../../index.html"; Hub=$true}
    @{P="source\python\python-fundamentals.html"; T="Python Fundamentals"; D="Variables, data types, control flow, and core syntax."; B="index.html"}
    @{P="source\python\python-methods.html"; T="Python Methods"; D="Built-in functions, string methods, and list operations."; B="index.html"}
    @{P="source\python\python-oops.html"; T="Object-Oriented Python"; D="Classes, inheritance, polymorphism, and design patterns."; B="index.html"}
    @{P="source\python\memory-performance.html"; T="Memory & Performance"; D="Memory management, optimization, and profiling techniques."; B="index.html"}
    
    # NumPy sub-pages (source/numpy/)
    @{P="source\numpy\index.html"; T="NumPy"; D="Numerical computing with Python's powerful array library."; B="../../index.html"; Hub=$true}
    @{P="source\numpy\numpy-basics.html"; T="NumPy Basics"; D="Array creation, data types, and fundamental operations."; B="index.html"}
    @{P="source\numpy\numpy-arrays.html"; T="NumPy Arrays"; D="Array indexing, slicing, reshaping, and broadcasting."; B="index.html"}
    @{P="source\numpy\numpy-operations.html"; T="NumPy Operations"; D="Mathematical operations, linear algebra, and statistics."; B="index.html"}
    @{P="source\numpy\methods.html"; T="NumPy Methods"; D="Essential NumPy methods and functions reference."; B="index.html"}
    
    # Pandas sub-pages (source/pandas/)
    @{P="source\pandas\index.html"; T="Pandas"; D="Data analysis and manipulation with Python DataFrames."; B="../../index.html"; Hub=$true}
    @{P="source\pandas\pandas-series.html"; T="Pandas Series"; D="One-dimensional labeled arrays - the building block of DataFrames."; B="index.html"}
    @{P="source\pandas\pandas-dataframes.html"; T="Pandas DataFrames"; D="Two-dimensional labeled data structures for tabular data."; B="index.html"}
    @{P="source\pandas\methods.html"; T="Pandas Methods"; D="Essential Pandas methods and functions reference."; B="index.html"}
    
    # Spark sub-pages (source/spark/)
    @{P="source\spark\index.html"; T="Apache Spark"; D="Distributed data processing at scale."; B="../../index.html"; Hub=$true}
    @{P="source\spark\spark-theory.html"; T="Spark Theory"; D="RDDs, DAGs, partitioning, and Spark internals."; B="index.html"}
    @{P="source\spark\spark-architecture.html"; T="Spark Architecture"; D="Cluster managers, executors, and deployment modes."; B="index.html"}
    @{P="source\spark\spark-code.html"; T="Spark Code"; D="PySpark DataFrames, transformations, and actions."; B="index.html"}
    
    # APIs sub-pages (source/apis/)
    @{P="source\apis\index.html"; T="APIs"; D="Understanding API design, types, and best practices."; B="../../index.html"; Hub=$true}
    @{P="source\apis\concepts.html"; T="API Concepts"; D="REST, GraphQL, gRPC - core API concepts and patterns."; B="index.html"}
    @{P="source\apis\types.html"; T="API Types"; D="Different API architectures and when to use each."; B="index.html"}
    
    # Tools sub-pages (source/tools/)
    @{P="source\tools\airflow.html"; T="Apache Airflow"; D="Workflow orchestration and scheduling for data pipelines."; B="index.html"}
    @{P="source\tools\dbt.html"; T="dbt"; D="Data transformation tool for analytics engineering."; B="index.html"}
    @{P="source\tools\kafka.html"; T="Apache Kafka"; D="Distributed event streaming platform for real-time data."; B="index.html"}
    
    # Cheatsheets sub-pages (source/cheatsheets/)
    @{P="source\cheatsheets\python-cheatsheet.html"; T="Python Cheatsheet"; D="Quick reference for Python syntax, methods, and patterns."; B="cheatsheet.html"}
    @{P="source\cheatsheets\postgresql-cheatsheet.html"; T="PostgreSQL Cheatsheet"; D="Quick reference for PostgreSQL queries, commands, and functions."; B="cheatsheet.html"}
    @{P="source\cheatsheets\pandas-cheatsheet.html"; T="Pandas Cheatsheet"; D="Quick reference for Pandas DataFrame operations and methods."; B="cheatsheet.html"}
    @{P="source\cheatsheets\numpy-cheatsheet.html"; T="NumPy Cheatsheet"; D="Quick reference for NumPy array operations and functions."; B="cheatsheet.html"}
    @{P="source\cheatsheets\spark-cheatsheet.html"; T="Spark Cheatsheet"; D="Quick reference for PySpark DataFrame operations and SQL."; B="cheatsheet.html"}
    @{P="source\cheatsheets\compare.html"; T="Comparison Tables"; D="Side-by-side comparison of key technologies and concepts."; B="cheatsheet.html"}
    
    # Roadmaps sub-pages (source/roadmaps/)
    @{P="source\roadmaps\data-engineer-roadmap.html"; T="Data Engineer Roadmap"; D="Step-by-step guide to becoming a data engineer."; B="roadmap.html"}
    @{P="source\roadmaps\python-roadmap.html"; T="Python Roadmap"; D="Learning path from Python basics to advanced patterns."; B="roadmap.html"}
    @{P="source\roadmaps\sql-roadmap.html"; T="SQL Roadmap"; D="Learning path from SQL basics to advanced queries."; B="roadmap.html"}
    @{P="source\roadmaps\spark-roadmap.html"; T="Spark Roadmap"; D="Learning path for Apache Spark and PySpark."; B="roadmap.html"}
    @{P="source\roadmaps\ml-engineer-roadmap.html"; T="ML Engineer Roadmap"; D="Step-by-step guide to machine learning engineering."; B="roadmap.html"}
    @{P="source\roadmaps\ai-engineer-roadmap.html"; T="AI Engineer Roadmap"; D="Learning path for AI engineering and LLM applications."; B="roadmap.html"}
    
    # Differences sub-pages (source/differences/)
    @{P="source\differences\differences-overview.html"; T="Overview"; D="Key technology comparisons at a glance."; B="differences-hub.html"}
    @{P="source\differences\differences-python.html"; T="Python Differences"; D="Key Python comparisons - list vs tuple, args vs kwargs, and more."; B="differences-hub.html"}
    @{P="source\differences\differences-sql.html"; T="SQL Differences"; D="Key SQL comparisons - WHERE vs HAVING, JOIN types, and more."; B="differences-hub.html"}
    @{P="source\differences\differences-pandas.html"; T="Pandas Differences"; D="Key Pandas comparisons - apply vs map, merge vs join, and more."; B="differences-hub.html"}
    @{P="source\differences\differences-numpy.html"; T="NumPy Differences"; D="Key NumPy comparisons - array vs list, copy vs view, and more."; B="differences-hub.html"}
    @{P="source\differences\differences-spark.html"; T="Spark Differences"; D="Key Spark comparisons - RDD vs DataFrame, Spark SQL vs DataFrames, and more."; B="differences-hub.html"}
    @{P="source\differences\differences-airflow.html"; T="Airflow Differences"; D="Key Airflow comparisons - DAG vs Task, operators vs sensors, and more."; B="differences-hub.html"}
    @{P="source\differences\differences-kafka.html"; T="Kafka Differences"; D="Key Kafka comparisons - topic vs partition, producer vs consumer, and more."; B="differences-hub.html"}
    @{P="source\differences\differences-dbt.html"; T="dbt Differences"; D="Key dbt comparisons - model vs source, ref vs source, and more."; B="differences-hub.html"}
    @{P="source\differences\differences-aws.html"; T="AWS Differences"; D="Key AWS service comparisons - S3 vs EBS, Lambda vs ECS, and more."; B="differences-hub.html"}
    @{P="source\differences\differences-cloud.html"; T="Cloud Differences"; D="AWS vs Azure vs GCP service comparisons."; B="differences-hub.html"}
    @{P="source\differences\differences-data-modelling.html"; T="Data Modelling Differences"; D="Star vs snowflake, OLAP vs OLTP, and schema comparisons."; B="differences-hub.html"}
    @{P="source\differences\differences-databricks.html"; T="Databricks Differences"; D="Key Databricks comparisons - notebook vs job, Delta vs Parquet, and more."; B="differences-hub.html"}
    
    # Portfolio pages (source/portfolios/)
    @{P="source\portfolios\portfolio.html"; T="Portfolio"; D="Data engineering projects and experience."; B="../../index.html"}
    @{P="source\portfolios\projects\projects-experienced.html"; T="Professional Projects"; D="Industry experience and enterprise data engineering projects."; B="../portfolio.html"; Deep=$true}
    @{P="source\portfolios\projects\projects-self.html"; T="Personal Projects"; D="Self-taught projects and open-source contributions."; B="../portfolio.html"; Deep=$true}
)

$okCount = 0
$skipCount = 0

foreach ($page in $pages) {
    $path = Join-Path $basePath $page.P
    
    if (-not (Test-Path $path)) {
        Write-Host "NOT FOUND: $($page.P)"
        $skipCount++
        continue
    }
    
    $lines = [System.IO.File]::ReadAllLines($path)
    
    # Check if already converted
    if (($lines[0..14] -join " ") -match 'shared\.css') {
        Write-Host "ALREADY: $($page.P)"
        $skipCount++
        continue
    }
    
    # Find first topic-section line (or first section/content div)
    $startLine = -1
    $endLine = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match 'class="topic-section"' -and $startLine -eq -1) {
            if ($i -gt 0 -and $lines[$i-1] -match '<!-- Section|<!-- ') { $startLine = $i - 1 }
            else { $startLine = $i }
        }
        if ($lines[$i].Trim() -eq '</div>' -and $i+1 -lt $lines.Count -and $lines[$i+1].Trim() -eq '</main>') {
            $endLine = $i - 1
        }
    }
    
    if ($startLine -eq -1 -or $endLine -eq -1) {
        Write-Host "SKIP: $($page.P) (markers not found: start=$startLine end=$endLine)"
        $skipCount++
        continue
    }
    
    $contentLines = $lines[$startLine..$endLine]
    $content = ($contentLines -join "`n") -replace '(?m)^      ', '    '
    
    # Determine depth-specific paths
    $homeHref = "../../index.html"
    $avatarSrc = "../../assets/images/profile-pic.jpeg"
    $portfolioHref = "../portfolios/portfolio.html"
    $cssHref = "../shared.css"
    
    if ($page.Deep) {
        $homeHref = "../../../index.html"
        $avatarSrc = "../../../assets/images/profile-pic.jpeg"
        $portfolioHref = "../../portfolios/portfolio.html"
        $cssHref = "../../shared.css"
    }

    $head = "<!DOCTYPE html>`n<html lang=`"en`">`n<head>`n  <meta charset=`"UTF-8`" />`n  <meta name=`"viewport`" content=`"width=device-width, initial-scale=1.0`" />`n  <title>Data Guide | $($page.T)</title>`n  <link rel=`"preconnect`" href=`"https://fonts.googleapis.com`" />`n  <link rel=`"preconnect`" href=`"https://fonts.gstatic.com`" crossorigin />`n  <link href=`"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap`" rel=`"stylesheet`" />`n  <link rel=`"stylesheet`" href=`"https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0`" />`n  <link rel=`"stylesheet`" href=`"https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap`" />`n  <link rel=`"stylesheet`" href=`"$cssHref`" />`n</head>`n`n<body class=`"topic-page`">`n  <header class=`"top-nav`">`n    <div class=`"top-nav-inner`">`n      <a href=`"$homeHref`" class=`"brand`">`n        <div class=`"brand-icon`">`n          <span class=`"material-symbols-outlined`">architecture</span>`n        </div>`n        <span class=`"brand-text`">Data Sheets</span>`n      </a>`n      <div class=`"nav-center`">`n        <div class=`"search-bar`">`n          <span class=`"material-symbols-outlined`">search</span>`n          <input type=`"text`" class=`"search-input`" placeholder=`"Search architecture, patterns, or cloud...`" />`n        </div>`n      </div>`n      <div class=`"nav-right`">`n        <button class=`"nav-icon-btn`" id=`"themeToggle`" onclick=`"toggleTheme()`">`n          <span class=`"material-symbols-outlined`" id=`"themeIcon`">dark_mode</span>`n        </button>`n        <a href=`"$portfolioHref`" class=`"user-avatar`">`n          <img src=`"$avatarSrc`" alt=`"User profile`" />`n        </a>`n      </div>`n    </div>`n  </header>`n`n  <main class=`"main-content`">`n    <header class=`"page-header page-header--row`">`n      <a href=`"$($page.B)`" class=`"back-link back-link--round`" aria-label=`"Back`">`n        <span class=`"material-symbols-outlined`">arrow_back</span>`n      </a>`n      <div class=`"page-header-inner`">`n        <h1>$($page.T)</h1>`n        <p>$($page.D)</p>`n      </div>`n    </header>`n`n    "

    $foot = "`n`n    <footer class=`"footer`">`n      <div class=`"footer-inner`">`n        <div class=`"footer-left`">`n          <span class=`"footer-brand`">Data Sheets</span>`n          <p class=`"footer-copyright`">© 2026 Data Sheets. All rights reserved.</p>`n        </div>`n        <div class=`"footer-links`">`n          <a href=`"#`">Documentation</a>`n          <a href=`"#`">Privacy</a>`n          <a href=`"#`">Terms</a>`n          <a href=`"#`">Support</a>`n        </div>`n      </div>`n    </footer>`n  </main>`n`n  <script>`n    function toggleTheme() {`n      var html = document.documentElement;`n      var themeIcon = document.getElementById('themeIcon');`n      if (html.classList.contains('dark')) {`n        html.classList.remove('dark');`n        localStorage.setItem('theme', 'light');`n        themeIcon.textContent = 'dark_mode';`n      } else {`n        html.classList.add('dark');`n        localStorage.setItem('theme', 'dark');`n        themeIcon.textContent = 'light_mode';`n      }`n    }`n    (function() {`n      var savedTheme = localStorage.getItem('theme');`n      var themeIcon = document.getElementById('themeIcon');`n      if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {`n        document.documentElement.classList.add('dark');`n        themeIcon.textContent = 'light_mode';`n      } else {`n        themeIcon.textContent = 'dark_mode';`n      }`n    })();`n  </script>`n</body>`n</html>"

    $result = $head + $content + $foot
    [System.IO.File]::WriteAllText($path, $result, [System.Text.UTF8Encoding]::new($false))
    $okCount++
    Write-Host "OK: $($page.P)"
}

Write-Host "`nDone! Converted: $okCount, Skipped: $skipCount"
