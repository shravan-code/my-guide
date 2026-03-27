from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, Response, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title="Data Guide API", version="1.0.0")

# Base directory for HTML files
BASE_DIR = Path(__file__).parent

# Mount source directory under a different path for static assets
app.mount("/_static/source", StaticFiles(directory=BASE_DIR / "source"), name="source")
app.mount("/assets", StaticFiles(directory=BASE_DIR / "assets"), name="assets")


# ============ Serve JSON files from cheatsheets ============
@app.get("/comparison-data.json", include_in_schema=False)
async def comparison_data():
    """Serve comparison data JSON file."""
    return FileResponse(BASE_DIR / "source" / "cheatsheets" / "comparison-data.json")


@app.get("/cheatsheets/comparison-data.json", include_in_schema=False)
async def cheatsheets_comparison_data():
    """Serve comparison data JSON file from cheatsheets folder."""
    return FileResponse(BASE_DIR / "source" / "cheatsheets" / "comparison-data.json")


# ============ HTML Path to Clean URL Mapping ============
# Maps /source/xxx/yyy.html to /clean-url
HTML_REDIRECTS = {
    # Main
    "/source/index.html": "/",
    # Python
    "/source/python/index.html": "/python",
    "/source/python/python-fundamentals.html": "/python-fundamentals",
    "/source/python/python-oops.html": "/python-oops",
    "/source/python/methods.html": "/python-methods",
    "/source/python/memory-performance.html": "/python-memory-performance",
    # Pandas
    "/source/pandas/index.html": "/pandas",
    "/source/pandas/pandas-series.html": "/pandas-series",
    "/source/pandas/pandas-dataframes.html": "/pandas-dataframes",
    "/source/pandas/methods.html": "/pandas-methods",
    # NumPy
    "/source/numpy/index.html": "/numpy",
    "/source/numpy/numpy-basics.html": "/numpy-basics",
    "/source/numpy/numpy-arrays.html": "/numpy-arrays",
    "/source/numpy/numpy-operations.html": "/numpy-operations",
    "/source/numpy/methods.html": "/numpy-methods",
    # SQL
    "/source/sql/index.html": "/sql",
    "/source/sql/sql-concepts.html": "/sql-concepts",
    "/source/sql/sql-joins.html": "/sql-joins",
    "/source/sql/sql-methods.html": "/sql-methods",
    "/source/sql/sql-modelling.html": "/sql-modelling",
    "/source/sql/sql-queries.html": "/sql-queries",
    "/source/sql/sql-subqueries.html": "/sql-subqueries",
    "/source/sql/sql-windows.html": "/sql-windows",
    # Spark
    "/source/spark/index.html": "/spark",
    "/source/spark/spark-theory.html": "/spark-theory",
    "/source/spark/spark-code.html": "/spark-code",
    "/source/spark/spark-architecture.html": "/spark-architecture",
    # Cloud
    "/source/cloud/index.html": "/cloud",
    "/source/cloud/cloud-basics.html": "/cloud-basics",
    "/source/cloud/cloud-services.html": "/cloud-services",
    "/source/cloud/cloud-compute.html": "/cloud-compute",
    "/source/cloud/cloud-storage.html": "/cloud-storage",
    "/source/cloud/cloud-serverless.html": "/cloud-serverless",
    "/source/cloud/cloud-topics.html": "/cloud-topics",
    "/source/cloud/cloud-aws.html": "/cloud-aws",
    "/source/cloud/cloud-azure.html": "/cloud-azure",
    "/source/cloud/cloud-gcp.html": "/cloud-gcp",
    # Data
    "/source/data/index.html": "/data",
    "/source/data/data-types.html": "/data-types",
    "/source/data/data-formats.html": "/data-formats",
    "/source/data/data-quality.html": "/data-quality",
    "/source/data/data-pipeline.html": "/data-pipeline",
    # Roadmaps
    "/source/roadmaps/roadmap.html": "/roadmaps",
    "/source/roadmaps/python-roadmap.html": "/python-roadmap",
    "/source/roadmaps/sql-roadmap.html": "/sql-roadmap",
    "/source/roadmaps/spark-roadmap.html": "/spark-roadmap",
    "/source/roadmaps/ml-engineer-roadmap.html": "/ml-engineer-roadmap",
    "/source/roadmaps/ai-engineer-roadmap.html": "/ai-engineer-roadmap",
    # Cheatsheets
    "/source/cheatsheets/cheatsheet.html": "/cheatsheets",
    "/source/cheatsheets/compare.html": "/cheatsheets-compare",
    "/source/cheatsheets/python-cheatsheet.html": "/python-cheatsheet",
    "/source/cheatsheets/numpy-cheatsheet.html": "/numpy-cheatsheet",
    "/source/cheatsheets/pandas-cheatsheet.html": "/pandas-cheatsheet",
    "/source/cheatsheets/spark-cheatsheet.html": "/spark-cheatsheet",
    "/source/cheatsheets/postgresql-cheatsheet.html": "/postgresql-cheatsheet",
    # Portfolio
    "/source/portfolios/portfolio.html": "/portfolio",
}


# ============ Common Requests ============
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Return empty 204 for favicon requests."""
    return Response(status_code=204)


@app.get("/index.html", include_in_schema=False)
async def index_html():
    """Redirect /index.html to / for compatibility."""
    return RedirectResponse(url="/")


# Catch-all for /source/* paths
@app.get("/source/{full_path:path}", include_in_schema=False)
async def source_redirect(request: Request, full_path: str):
    """Redirect /source/xxx.html to clean URLs, other files to /_static/source/."""
    path = f"/source/{full_path}"
    if full_path.endswith(".html") and path in HTML_REDIRECTS:
        return RedirectResponse(url=HTML_REDIRECTS[path], status_code=301)
    # For CSS, JS, images - redirect to static mount
    return RedirectResponse(url=f"/_static/source/{full_path}", status_code=301)


def get_clean_url(file_stem: str, section: str = "") -> str:
    """Convert a file name to a clean URL.
    Format: /section-topic (e.g., /roadmaps-python, /sql-joins)
    """
    # Handle special cases
    if file_stem == "index":
        return f"/{section}" if section else "/"
    if file_stem == "roadmap" and section == "roadmaps":
        return "/roadmaps"
    if file_stem == "cheatsheet" and section == "cheatsheets":
        return "/cheatsheets"
    if file_stem == "compare" and section == "cheatsheets":
        return "/cheatsheets-compare"

    # If file_stem already starts with the section name, don't duplicate
    # e.g., cloud-gcp in cloud section -> /cloud-gcp (not /cloud-cloud-gcp)
    if section and file_stem.startswith(section + "-"):
        return f"/{file_stem}"

    # For files like python-roadmap.html in roadmaps folder, extract just "python"
    # For files like sql-joins.html in sql folder, use "sql-joins"
    topic = file_stem

    # Check if file_stem contains the section name as prefix
    # e.g., python-roadmap in roadmaps folder -> just use "python"
    if section:
        # Remove section suffix from filename (e.g., python-roadmap -> python when in roadmaps)
        section_suffixes = {
            "roadmaps": ["-roadmap"],
            "cheatsheets": ["-cheatsheet"],
        }
        if section in section_suffixes:
            for suffix in section_suffixes[section]:
                if topic.endswith(suffix):
                    topic = topic[: -len(suffix)]
                    break

    # Always prefix with section name
    if section:
        return f"/{section}-{topic}"
    return f"/{topic}"


def read_html_file(file_path: Path) -> str:
    """Read and return HTML file content with rewritten paths."""
    import re

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Rewrite ALL relative CSS paths: ../xxx.css or ../../xxx.css -> /source/xxx.css
        content = re.sub(
            r'href="(\.\./)+((?:styles|python|spark|roadmaps|cheatsheets|sql|pandas|numpy|cloud|data|portfolios|hub|design-tokens)[^"]*\.css)"',
            r'href="/source/\2"',
            content,
        )

        # Rewrite source/xxx.css (for home page) -> /source/xxx.css
        content = re.sub(
            r'href="source/([^"]+\.css)"',
            r'href="/source/\1"',
            content,
        )

        # Rewrite same-directory CSS files like roadmap.css, spark.css -> /source/section/xxx.css
        section = file_path.parent.name
        if section and section != ".":
            content = re.sub(
                r'href="([a-z-]+\.css)"',
                rf'href="/source/{section}/\1"',
                content,
            )
            # Rewrite same-directory JS files like cheatsheets.js -> /source/section/xxx.js
            content = re.sub(
                r'src="([a-z-]+\.js)"',
                rf'src="/source/{section}/\1"',
                content,
            )

        # Rewrite ALL relative JS paths
        content = re.sub(
            r'src="(\.\./)+((?:app|spark|python|cheatsheets|sql|pandas|numpy|cloud|data)[^"]*\.js)"',
            r'src="/source/\2"',
            content,
        )

        # Rewrite source/xxx.js (for home page) -> /source/xxx.js
        content = re.sub(
            r'src="source/([^"]+\.js)"',
            r'src="/source/\1"',
            content,
        )

        # Rewrite relative JSON paths like comparison-data.json -> /comparison-data.json
        content = re.sub(
            r'(fetch\(["\'])comparison-data\.json',
            r"\1/comparison-data.json",
            content,
        )

        # Rewrite ../../index.html -> / (or ../index.html -> /)
        content = re.sub(r'href="(\.\./)+index\.html"', 'href="/"', content)

        # Rewrite ../../portfolios/portfolio.html -> /portfolio
        content = re.sub(
            r'href="(\.\./)+portfolios/portfolio\.html"', 'href="/portfolio"', content
        )

        # Rewrite index.html (same directory) -> / (for root index.html)
        content = re.sub(r'href="index\.html"', 'href="/"', content)

        # Rewrite source/xxx/index.html -> /section (for home page links)
        def rewrite_source_index(match):
            section = match.group(1)
            return f'href="/{section}"'

        content = re.sub(
            r'href="source/([a-z]+)/index\.html"', rewrite_source_index, content
        )

        # Rewrite all same-directory .html links -> clean URLs
        # Pattern: href="filename.html" (not preceded by / or ../)
        def rewrite_html_link(match):
            full_match = match.group(0)
            filename = match.group(1)

            # Skip if it's already a clean URL or absolute path
            if filename.startswith("/") or "://" in filename:
                return full_match

            # Get the section from file path
            section = file_path.parent.name

            # Get clean URL
            clean_url = get_clean_url(filename.replace(".html", ""), section)
            return f'href="{clean_url}"'

        content = re.sub(r'href="([a-zA-Z0-9_-]+\.html)"', rewrite_html_link, content)

        return content
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="HTML file not found")


# ============ Main Pages ============
@app.get("/", response_class=HTMLResponse, summary="Home Page")
async def home():
    """Serve the main index page."""
    return read_html_file(BASE_DIR / "index.html")


@app.get("/portfolio", response_class=HTMLResponse, summary="Portfolio Page")
async def portfolio():
    """Serve the portfolio page."""
    return read_html_file(BASE_DIR / "source" / "portfolios" / "portfolio.html")


# ============ Python Section ============
@app.get("/python", response_class=HTMLResponse, summary="Python Home")
async def python_home():
    """Serve Python section home."""
    return read_html_file(BASE_DIR / "source" / "python" / "index.html")


@app.get(
    "/python-fundamentals", response_class=HTMLResponse, summary="Python Fundamentals"
)
async def python_fundamentals():
    """Serve Python fundamentals page."""
    return read_html_file(BASE_DIR / "source" / "python" / "python-fundamentals.html")


@app.get("/python-oops", response_class=HTMLResponse, summary="Python OOPs")
async def python_oops():
    """Serve Python OOPs page."""
    return read_html_file(BASE_DIR / "source" / "python" / "python-oops.html")


@app.get("/python-methods", response_class=HTMLResponse, summary="Python Methods")
async def python_methods():
    """Serve Python methods page."""
    return read_html_file(BASE_DIR / "source" / "python" / "methods.html")


@app.get(
    "/python-memory-performance",
    response_class=HTMLResponse,
    summary="Python Memory & Performance",
)
async def python_memory_performance():
    """Serve Python memory and performance page."""
    return read_html_file(BASE_DIR / "source" / "python" / "memory-performance.html")


# ============ Pandas Section ============
@app.get("/pandas", response_class=HTMLResponse, summary="Pandas Home")
async def pandas_home():
    """Serve Pandas section home."""
    return read_html_file(BASE_DIR / "source" / "pandas" / "index.html")


@app.get("/pandas-series", response_class=HTMLResponse, summary="Pandas Series")
async def pandas_series():
    """Serve Pandas Series page."""
    return read_html_file(BASE_DIR / "source" / "pandas" / "pandas-series.html")


@app.get("/pandas-dataframes", response_class=HTMLResponse, summary="Pandas DataFrames")
async def pandas_dataframes():
    """Serve Pandas DataFrames page."""
    return read_html_file(BASE_DIR / "source" / "pandas" / "pandas-dataframes.html")


@app.get("/pandas-methods", response_class=HTMLResponse, summary="Pandas Methods")
async def pandas_methods():
    """Serve Pandas Methods page."""
    return read_html_file(BASE_DIR / "source" / "pandas" / "methods.html")


# ============ NumPy Section ============
@app.get("/numpy", response_class=HTMLResponse, summary="NumPy Home")
async def numpy_home():
    """Serve NumPy section home."""
    return read_html_file(BASE_DIR / "source" / "numpy" / "index.html")


@app.get("/numpy-basics", response_class=HTMLResponse, summary="NumPy Basics")
async def numpy_basics():
    """Serve NumPy Basics page."""
    return read_html_file(BASE_DIR / "source" / "numpy" / "numpy-basics.html")


@app.get("/numpy-arrays", response_class=HTMLResponse, summary="NumPy Arrays")
async def numpy_arrays():
    """Serve NumPy Arrays page."""
    return read_html_file(BASE_DIR / "source" / "numpy" / "numpy-arrays.html")


@app.get("/numpy-operations", response_class=HTMLResponse, summary="NumPy Operations")
async def numpy_operations():
    """Serve NumPy Operations page."""
    return read_html_file(BASE_DIR / "source" / "numpy" / "numpy-operations.html")


@app.get("/numpy-methods", response_class=HTMLResponse, summary="NumPy Methods")
async def numpy_methods():
    """Serve NumPy Methods page."""
    return read_html_file(BASE_DIR / "source" / "numpy" / "methods.html")


# ============ SQL Section ============
@app.get("/sql", response_class=HTMLResponse, summary="SQL Home")
async def sql_home():
    """Serve SQL section home."""
    return read_html_file(BASE_DIR / "source" / "sql" / "index.html")


@app.get("/sql-concepts", response_class=HTMLResponse, summary="SQL Concepts")
async def sql_concepts():
    """Serve SQL Concepts page."""
    return read_html_file(BASE_DIR / "source" / "sql" / "sql-concepts.html")


@app.get("/sql-joins", response_class=HTMLResponse, summary="SQL Joins")
async def sql_joins():
    """Serve SQL Joins page."""
    return read_html_file(BASE_DIR / "source" / "sql" / "sql-joins.html")


@app.get("/sql-methods", response_class=HTMLResponse, summary="SQL Methods")
async def sql_methods():
    """Serve SQL Methods page."""
    return read_html_file(BASE_DIR / "source" / "sql" / "sql-methods.html")


@app.get("/sql-modelling", response_class=HTMLResponse, summary="SQL Modelling")
async def sql_modelling():
    """Serve SQL Modelling page."""
    return read_html_file(BASE_DIR / "source" / "sql" / "sql-modelling.html")


@app.get("/sql-queries", response_class=HTMLResponse, summary="SQL Queries")
async def sql_queries():
    """Serve SQL Queries page."""
    return read_html_file(BASE_DIR / "source" / "sql" / "sql-queries.html")


@app.get("/sql-subqueries", response_class=HTMLResponse, summary="SQL Subqueries")
async def sql_subqueries():
    """Serve SQL Subqueries page."""
    return read_html_file(BASE_DIR / "source" / "sql" / "sql-subqueries.html")


@app.get("/sql-windows", response_class=HTMLResponse, summary="SQL Windows")
async def sql_windows():
    """Serve SQL Windows page."""
    return read_html_file(BASE_DIR / "source" / "sql" / "sql-windows.html")


# ============ Spark Section ============
@app.get("/spark", response_class=HTMLResponse, summary="Spark Home")
async def spark_home():
    """Serve Spark section home."""
    return read_html_file(BASE_DIR / "source" / "spark" / "index.html")


@app.get("/spark-theory", response_class=HTMLResponse, summary="Spark Theory")
async def spark_theory():
    """Serve Spark Theory page."""
    return read_html_file(BASE_DIR / "source" / "spark" / "spark-theory.html")


@app.get("/spark-code", response_class=HTMLResponse, summary="Spark Code")
async def spark_code():
    """Serve Spark Code page."""
    return read_html_file(BASE_DIR / "source" / "spark" / "spark-code.html")


@app.get(
    "/spark-architecture", response_class=HTMLResponse, summary="Spark Architecture"
)
async def spark_architecture():
    """Serve Spark Architecture page."""
    return read_html_file(BASE_DIR / "source" / "spark" / "spark-architecture.html")


# ============ Cloud Section ============
@app.get("/cloud", response_class=HTMLResponse, summary="Cloud Home")
async def cloud_home():
    """Serve Cloud section home."""
    return read_html_file(BASE_DIR / "source" / "cloud" / "index.html")


@app.get("/cloud-basics", response_class=HTMLResponse, summary="Cloud Basics")
async def cloud_basics():
    """Serve Cloud Basics page."""
    return read_html_file(BASE_DIR / "source" / "cloud" / "cloud-basics.html")


@app.get("/cloud-services", response_class=HTMLResponse, summary="Cloud Services")
async def cloud_services():
    """Serve Cloud Services page."""
    return read_html_file(BASE_DIR / "source" / "cloud" / "cloud-services.html")


@app.get("/cloud-compute", response_class=HTMLResponse, summary="Cloud Compute")
async def cloud_compute():
    """Serve Cloud Compute page."""
    return read_html_file(BASE_DIR / "source" / "cloud" / "cloud-compute.html")


@app.get("/cloud-storage", response_class=HTMLResponse, summary="Cloud Storage")
async def cloud_storage():
    """Serve Cloud Storage page."""
    return read_html_file(BASE_DIR / "source" / "cloud" / "cloud-storage.html")


@app.get("/cloud-serverless", response_class=HTMLResponse, summary="Cloud Serverless")
async def cloud_serverless():
    """Serve Cloud Serverless page."""
    return read_html_file(BASE_DIR / "source" / "cloud" / "cloud-serverless.html")


@app.get("/cloud-topics", response_class=HTMLResponse, summary="Cloud Topics")
async def cloud_topics():
    """Serve Cloud Topics page."""
    return read_html_file(BASE_DIR / "source" / "cloud" / "cloud-topics.html")


@app.get("/cloud-aws", response_class=HTMLResponse, summary="Cloud AWS")
async def cloud_aws():
    """Serve Cloud AWS page."""
    return read_html_file(BASE_DIR / "source" / "cloud" / "cloud-aws.html")


@app.get("/cloud-azure", response_class=HTMLResponse, summary="Cloud Azure")
async def cloud_azure():
    """Serve Cloud Azure page."""
    return read_html_file(BASE_DIR / "source" / "cloud" / "cloud-azure.html")


@app.get("/cloud-gcp", response_class=HTMLResponse, summary="Cloud GCP")
async def cloud_gcp():
    """Serve Cloud GCP page."""
    return read_html_file(BASE_DIR / "source" / "cloud" / "cloud-gcp.html")


# ============ Data Section ============
@app.get("/data", response_class=HTMLResponse, summary="Data Home")
async def data_home():
    """Serve Data section home."""
    return read_html_file(BASE_DIR / "source" / "data" / "index.html")


@app.get("/data-types", response_class=HTMLResponse, summary="Data Types")
async def data_types():
    """Serve Data Types page."""
    return read_html_file(BASE_DIR / "source" / "data" / "data-types.html")


@app.get("/data-formats", response_class=HTMLResponse, summary="Data Formats")
async def data_formats():
    """Serve Data Formats page."""
    return read_html_file(BASE_DIR / "source" / "data" / "data-formats.html")


@app.get("/data-quality", response_class=HTMLResponse, summary="Data Quality")
async def data_quality():
    """Serve Data Quality page."""
    return read_html_file(BASE_DIR / "source" / "data" / "data-quality.html")


@app.get("/data-pipeline", response_class=HTMLResponse, summary="Data Pipeline")
async def data_pipeline():
    """Serve Data Pipeline page."""
    return read_html_file(BASE_DIR / "source" / "data" / "data-pipeline.html")


# ============ Roadmaps Section ============
@app.get("/roadmaps", response_class=HTMLResponse, summary="Roadmaps Home")
async def roadmaps_home():
    """Serve Roadmaps section home."""
    return read_html_file(BASE_DIR / "source" / "roadmaps" / "roadmap.html")


@app.get("/roadmaps-python", response_class=HTMLResponse, summary="Python Roadmap")
async def roadmaps_python():
    """Serve Python Roadmap page."""
    return read_html_file(BASE_DIR / "source" / "roadmaps" / "python-roadmap.html")


@app.get("/roadmaps-sql", response_class=HTMLResponse, summary="SQL Roadmap")
async def roadmaps_sql():
    """Serve SQL Roadmap page."""
    return read_html_file(BASE_DIR / "source" / "roadmaps" / "sql-roadmap.html")


@app.get("/roadmaps-spark", response_class=HTMLResponse, summary="Spark Roadmap")
async def roadmaps_spark():
    """Serve Spark Roadmap page."""
    return read_html_file(BASE_DIR / "source" / "roadmaps" / "spark-roadmap.html")


@app.get(
    "/roadmaps-ml-engineer", response_class=HTMLResponse, summary="ML Engineer Roadmap"
)
async def roadmaps_ml_engineer():
    """Serve ML Engineer Roadmap page."""
    return read_html_file(BASE_DIR / "source" / "roadmaps" / "ml-engineer-roadmap.html")


@app.get(
    "/roadmaps-ai-engineer", response_class=HTMLResponse, summary="AI Engineer Roadmap"
)
async def roadmaps_ai_engineer():
    """Serve AI Engineer Roadmap page."""
    return read_html_file(BASE_DIR / "source" / "roadmaps" / "ai-engineer-roadmap.html")


# ============ Cheatsheets Section ============
@app.get("/cheatsheets", response_class=HTMLResponse, summary="Cheatsheets Home")
async def cheatsheets_home():
    """Serve Cheatsheets section home."""
    return read_html_file(BASE_DIR / "source" / "cheatsheets" / "cheatsheet.html")


@app.get(
    "/cheatsheets-compare", response_class=HTMLResponse, summary="Compare Cheatsheets"
)
async def cheatsheets_compare():
    """Serve Compare Cheatsheets page."""
    return read_html_file(BASE_DIR / "source" / "cheatsheets" / "compare.html")


@app.get(
    "/cheatsheets-python", response_class=HTMLResponse, summary="Python Cheatsheet"
)
async def cheatsheets_python():
    """Serve Python Cheatsheet page."""
    return read_html_file(
        BASE_DIR / "source" / "cheatsheets" / "python-cheatsheet.html"
    )


@app.get("/cheatsheets-numpy", response_class=HTMLResponse, summary="NumPy Cheatsheet")
async def cheatsheets_numpy():
    """Serve NumPy Cheatsheet page."""
    return read_html_file(BASE_DIR / "source" / "cheatsheets" / "numpy-cheatsheet.html")


@app.get(
    "/cheatsheets-pandas", response_class=HTMLResponse, summary="Pandas Cheatsheet"
)
async def cheatsheets_pandas():
    """Serve Pandas Cheatsheet page."""
    return read_html_file(
        BASE_DIR / "source" / "cheatsheets" / "pandas-cheatsheet.html"
    )


@app.get("/cheatsheets-spark", response_class=HTMLResponse, summary="Spark Cheatsheet")
async def cheatsheets_spark():
    """Serve Spark Cheatsheet page."""
    return read_html_file(BASE_DIR / "source" / "cheatsheets" / "spark-cheatsheet.html")


@app.get(
    "/cheatsheets-postgresql",
    response_class=HTMLResponse,
    summary="PostgreSQL Cheatsheet",
)
async def cheatsheets_postgresql():
    """Serve PostgreSQL Cheatsheet page."""
    return read_html_file(
        BASE_DIR / "source" / "cheatsheets" / "postgresql-cheatsheet.html"
    )


# ============ API Info ============
@app.get("/api", summary="API Information")
async def api_info():
    """Get API information and available endpoints."""
    return {
        "title": "Data Guide API",
        "version": "1.0.0",
        "endpoints": {
            "home": "/",
            "portfolio": "/portfolio",
            "python": [
                "/python",
                "/python-fundamentals",
                "/python-oops",
                "/python-methods",
                "/python-memory-performance",
            ],
            "pandas": [
                "/pandas",
                "/pandas-series",
                "/pandas-dataframes",
                "/pandas-methods",
            ],
            "numpy": [
                "/numpy",
                "/numpy-basics",
                "/numpy-arrays",
                "/numpy-operations",
                "/numpy-methods",
            ],
            "sql": [
                "/sql",
                "/sql-concepts",
                "/sql-joins",
                "/sql-methods",
                "/sql-modelling",
                "/sql-queries",
                "/sql-subqueries",
                "/sql-windows",
            ],
            "spark": ["/spark", "/spark-theory", "/spark-code", "/spark-architecture"],
            "cloud": [
                "/cloud",
                "/cloud-basics",
                "/cloud-services",
                "/cloud-compute",
                "/cloud-storage",
                "/cloud-serverless",
                "/cloud-topics",
                "/cloud-aws",
                "/cloud-azure",
                "/cloud-gcp",
            ],
            "data": [
                "/data",
                "/data-types",
                "/data-formats",
                "/data-quality",
                "/data-pipeline",
            ],
            "roadmaps": [
                "/roadmaps",
                "/roadmaps-python",
                "/roadmaps-sql",
                "/roadmaps-spark",
                "/roadmaps-ml-engineer",
                "/roadmaps-ai-engineer",
            ],
            "cheatsheets": [
                "/cheatsheets",
                "/cheatsheets-compare",
                "/cheatsheets-python",
                "/cheatsheets-numpy",
                "/cheatsheets-pandas",
                "/cheatsheets-spark",
                "/cheatsheets-postgresql",
            ],
        },
    }


if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 50)
    print("Data Guide API Server")
    print("=" * 50)
    print(f"  Server:    http://localhost:8000")
    print(f"  API Docs:  http://localhost:8000/docs")
    print(f"  ReDoc:     http://localhost:8000/redoc")
    print("=" * 50 + "\n")

    uvicorn.run(app, host="127.0.0.1", port=8000)
