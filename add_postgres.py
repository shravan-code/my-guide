import re

PATH = r"D:\shra1\github\my-guide\spark\pyspark-code-guide.html"

with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()


def e(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ─── PostgreSQL queries for each section's code block ───────────────────────

PGSQL = {
    "read-write": """SELECT
    o.order_id, o.customer_id, o.event_date, o.amount
FROM orders o;

SELECT * FROM orders
WHERE amount > 100
ORDER BY event_date;""",
    "csv": """-- Read: import CSV into table
CREATE TABLE sales (id INT, region TEXT, amount NUMERIC);
COPY sales FROM '/data/sales.csv' WITH (FORMAT csv, HEADER true);

-- Write: export to CSV
COPY (SELECT * FROM sales ORDER BY id) TO '/tmp/sales_out.csv'
    WITH (FORMAT csv, HEADER true);""",
    "json": """-- Read: extract JSON fields
SELECT raw->>'event' AS event, raw->>'value' AS value
FROM events, jsonb_array_elements(raw::jsonb) WITH ORDINALITY AS arr(raw);

-- Write: export as JSON
SELECT json_build_object('id', id, 'region', region) AS json_row
FROM sales;""",
    "parquet": """-- PostgreSQL 16+: native Parquet read
SELECT * FROM read_parquet('/lake/raw/orders/*.parquet');

-- Write Parquet via COPY
COPY sales TO '/lake/curated/orders/'
    WITH (FORMAT parquet, COMPRESSION 'snappy');""",
    "avro": """-- PostgreSQL: requires avro_fdw or Python avro library
SELECT * FROM read_avro('/lake/raw/events_avro/*.avro');
-- Write: serialize via Python (avro library)""",
    "cloud-io": """-- AWS S3
SELECT aws_s3.table_import_from_s3(
    'sales', 'order_id,region,amount', '(format csv, header)',
    'de-bucket', 'sales/orders/', 'us-east-1'
);

-- Azure Blob
COPY sales FROM
    'https://storage.blob.core.windows.net/container/orders/sales.csv';

-- GCP GCS
\\! gsutil cp gs://my-bucket/orders/*.parquet /tmp/
COPY sales FROM '/tmp/orders.parquet' WITH (FORMAT parquet);""",
    "cloud-libs": """-- Delta Lake
SELECT * FROM delta_log WHERE version = 0;
-- Time-travel via version column (manual) or native (Enterprise)

-- Hudi
INSERT INTO orders (id, region, amount, ts)
VALUES (1, 'APAC', 120.0, 1709280000)
ON CONFLICT (id) DO UPDATE SET amount = EXCLUDED.amount;

-- Iceberg
SELECT * FROM orders VERSION AS OF 1234567890;  -- Enterprise""",
    "excel-compression": """-- Excel via odbc_fdw
SELECT * FROM foreign_excel_sheet;

-- Write: CSV then convert to XLSX via Python
COPY sales TO '/tmp/report.csv' WITH (FORMAT csv, HEADER true);

-- Gzip
\\copy sales FROM PROGRAM 'gzip -d -c /data/sales.csv.gz' WITH (FORMAT csv);
COPY sales TO PROGRAM 'gzip > /tmp/sales.csv.gz' WITH (FORMAT csv);""",
    "columns-ref": """-- String column: use name directly
SELECT order_id, region, amount FROM df;

-- Column expression
SELECT order_id, region, amount * 1.1 AS scaled_amount FROM df;""",
    "columns-select": """SELECT order_id, region, amount FROM df;

SELECT order_id, region,
    amount AS amount_usd,
    amount * 0.9 AS amount_eur
FROM df;""",
}

# ─── REPLACEMENT: find </div> followed by <pre class="code"> in sections 1-12 ───
# Pattern: in concept sections (1-12), the two-col tables close, then a pre.code appears
# We replace:   </div>\n      <pre class="code">...with...
#              </div>\n      <div class="two-col"><div class="panel"><h3>PySpark</h3><pre...>...+PG panel</div></div>

# Find all occurrences of: </div>\n      <pre class="code">
# and convert them to two-col


def make_two_col(pyspark_code, postgres_code):
    return (
        '<div class="two-col">'
        '<div class="panel"><h3>PySpark</h3>'
        f'<pre class="code"><code>{e(pyspark_code)}</code></pre></div>'
        '<div class="panel"><h3>PostgreSQL</h3>'
        f'<pre class="code"><code>{e(postgres_code)}</code></pre></div>'
        "</div>"
    )


# Pattern: closing div of the two-col tables, followed by a code block
# The closing div is </div> (but we need to be specific about which div)
# Looking at the structure: </div>\n      <pre class="code">
# This is the div that closes the tables two-col

count = 0

# Approach: find all <pre class="code"> blocks that are NOT inside a two-col
# and are NOT inside a join-block (join blocks have their own handling)
# These are the "bare" code blocks in sections 1-12

# Strategy: scan for section IDs 1-12, find bare pre.code after table two-col


def replace_bare_code(match):
    global count
    pre_block = match.group(0)

    # Extract the code content
    code_match = re.search(r"<code>(.*?)</code>", pre_block, re.DOTALL)
    if not code_match:
        return pre_block

    raw_code = code_match.group(1)
    # Unescape HTML entities for the code
    code = (
        raw_code.replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&amp;", "&")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
    )

    # Determine which section this belongs to based on surrounding context
    # Find the nearest section h2 before this pre block
    preceding_h2 = re.search(r"<h2>\d+\) [^<]+</h2>", content[: match.start()])

    # Default PostgreSQL
    pg = PGSQL.get("read-write", "-- PostgreSQL equivalent\nSELECT * FROM df;")

    if preceding_h2:
        h2_text = preceding_h2.group(0)
        if "Introduction" in h2_text:
            pg = "-- No direct equivalent — PySpark creates a distributed session\nSELECT 1 AS placeholder;"
        elif "SparkSession" in h2_text:
            pg = "-- SparkSession = PostgreSQL connection pooling + session config\n-- PostgreSQL: SET statement_timeout = '30s';"
        elif "Reading and Writing" in h2_text:
            pg = PGSQL["read-write"]
        elif "CSV" in h2_text:
            pg = PGSQL["csv"]
        elif "JSON" in h2_text:
            pg = PGSQL["json"]
        elif "Parquet" in h2_text:
            pg = PGSQL["parquet"]
        elif "Avro" in h2_text:
            pg = PGSQL["avro"]
        elif "Cloud" in h2_text:
            pg = PGSQL["cloud-io"]
        elif "Common Cloud" in h2_text:
            pg = PGSQL["cloud-libs"]
        elif "Excel" in h2_text:
            pg = PGSQL["excel-compression"]
        elif "Refer" in h2_text:
            pg = PGSQL["columns-ref"]
        elif "Select" in h2_text:
            pg = PGSQL["columns-select"]

    new_two_col = make_two_col(code, pg)
    count += 1
    return new_two_col


# Find all bare <pre class="code"> that appear after </div> (closing two-col)
# These are standalone code blocks NOT inside a two-col

# Pattern: look for </div>\n      <pre class="code">
# We need to be careful: only replace ones that close the table two-col

# Strategy: in the content, find each </div> that closes a two-col containing tables,
# and replace the following pre.code block

# Better approach: look for all <pre class="code"> in concept sections that are NOT already
# wrapped in a two-col panel (i.e., not preceded by a two-col opening div for code)

# The structure we want to change:
#   </div>   <- closes table two-col
#   <pre class="code">  <- bare code block
# We change to:
#   </div>
#   <div class="two-col">  <- opens code two-col
#     <div class="panel"><h3>PySpark</h3><pre class="code">...</pre></div>
#     <div class="panel"><h3>PostgreSQL</h3><pre class="code">PG...</pre></div>
#   </div>

# Pattern to match: </div> followed by newline + spaces + <pre class="code">
# BUT NOT: </div> followed by </div> (already inside a two-col)

pattern = re.compile(
    r'(</div>)\s*\n(<pre class="code"><code>.*?</code></pre>)', re.DOTALL
)


def replace_match(m):
    global count
    closing_div = m.group(1)
    pre_block = m.group(2)

    # Extract code
    code_match = re.search(r"<code>(.*?)</code>", pre_block, re.DOTALL)
    if not code_match:
        return m.group(0)

    raw_code = code_match.group(1)
    code = (
        raw_code.replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&amp;", "&")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
    )

    # Find which section based on preceding h2
    pos = m.start()
    h2_matches = list(re.finditer(r"<h2>\d+\) [^<]+</h2>", content[:pos]))
    pg = "-- PostgreSQL equivalent\nSELECT * FROM df;"

    if h2_matches:
        last_h2 = h2_matches[-1].group(0)
        if "Introduction" in last_h2:
            pg = "-- SparkSession is PySpark's entry point; PostgreSQL uses connection pooling\n-- No direct equivalent — PySpark creates a distributed session\nSELECT 1 AS placeholder;"
        elif "SparkSession" in last_h2:
            pg = "-- PostgreSQL: configure connection pools and session settings\nSET statement_timeout = '30s';\nSET max_connections = 100;"
        elif "Reading and Writing" in last_h2:
            pg = PGSQL["read-write"]
        elif "CSV" in last_h2:
            pg = PGSQL["csv"]
        elif "JSON" in last_h2:
            pg = PGSQL["json"]
        elif "Parquet" in last_h2:
            pg = PGSQL["parquet"]
        elif "Avro" in last_h2:
            pg = PGSQL["avro"]
        elif "Cloud" in last_h2:
            pg = PGSQL["cloud-io"]
        elif "Common Cloud" in last_h2:
            pg = PGSQL["cloud-libs"]
        elif "Excel" in last_h2:
            pg = PGSQL["excel-compression"]
        elif "Refer" in last_h2:
            pg = PGSQL["columns-ref"]
        elif "Select" in last_h2:
            pg = PGSQL["columns-select"]

    new_block = make_two_col(code, pg)
    count += 1
    return closing_div + "\n      " + new_block


new_content = pattern.sub(replace_match, content)
print(f"Replaced {count} bare code blocks with PySpark+PostgreSQL two-col")

# ─── ADD PostgreSQL to join sub-sections that don't have it yet ──────────────

JOIN_PG = {
    "Cross Join — Cartesian Product": """SELECT a.id, a.val, b.flag, b.score
FROM df_a a
CROSS JOIN df_b b;""",
    "Broadcast (Map-Side) Join — for Small Tables": """-- PostgreSQL: small tables use hash join automatically
SET enable_hashjoin = on;
SET enable_seqscan = on;  -- allow seq scan for small tables""",
    "Self Join — Hierarchical Data": """SELECT e.emp_id, e.name, e.manager_id, m.name AS mgr_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id;""",
    "Multi-Column Join": """SELECT o.order_id, o.region, o.product_id, d.discount
FROM orders o
JOIN discounts d USING (region, product_id);""",
}

join_count = 0
for join_name, pg_sql in JOIN_PG.items():
    # Find the join block with this heading
    # The pattern: <h3>JOIN_NAME</h3> ... <pre class="code">PySpark...</pre>
    # We need to find if there's already a PostgreSQL panel after
    h3_pattern = re.compile(
        r"(<h3>"
        + re.escape(join_name)
        + r'</h3>.*?<pre class="code"><code>.*?</code></pre>)',
        re.DOTALL,
    )
    h3_match = h3_pattern.search(new_content)
    if not h3_match:
        print(f"  Not found: {join_name}")
        continue

    # Check if PostgreSQL already exists within ~600 chars after the PySpark block
    py_end = h3_match.end()
    check_region = new_content[py_end : py_end + 600]
    if "PostgreSQL" in check_region and "JOIN" in check_region.upper():
        print(f"  Already has PG: {join_name}")
        continue

    # Check if it's inside a join-block that might already have it
    # For cross join, self join, multicol join - they may already have PG added

    # Just insert PG panel after the PySpark block
    pg_block = (
        '<div class="two-col" style="margin-top:0.3rem">'
        '<div class="panel"><h3>PostgreSQL</h3>'
        f'<pre class="code"><code>{e(pg_sql)}</code></pre></div>'
        "</div>"
    )

    # Find the end of the PySpark pre block
    pre_close = new_content.find("</pre>", py_end)
    if pre_close > 0:
        insert_pos = pre_close + len("</pre>")
        # Check what's after
        after = new_content[insert_pos : insert_pos + 20]
        new_content = new_content[:insert_pos] + pg_block + new_content[insert_pos:]
        join_count += 1
        print(f"  Added PG: {join_name}")

print(f"\nAdded PG to {join_count} join sections")

# ─── Fix section 17 (Nulls): fillna/dropna alias section ────────────────────
null_alias_h3 = "fillna / dropna Aliases"
h3_pattern = re.compile(
    r"(<h3>"
    + re.escape(null_alias_h3)
    + r'</h3>.*?<pre class="code"><code>.*?</code></pre>)',
    re.DOTALL,
)
h3_match = h3_pattern.search(new_content)
if h3_match:
    py_end = h3_match.end()
    check = new_content[py_end : py_end + 400]
    if "PostgreSQL" not in check:
        pg_block = (
            '<div class="two-col" style="margin-top:0.3rem">'
            '<div class="panel"><h3>PostgreSQL</h3>'
            '<pre class="code"><code>SELECT COALESCE(col, default_val) AS col FROM df;\n'
            "-- equivalent to fillna; drop is handled by WHERE col IS NOT NULL</code></pre></div>"
            "</div>"
        )
        pre_close = new_content.find("</pre>", py_end)
        if pre_close > 0:
            new_content = (
                new_content[: pre_close + 6] + pg_block + new_content[pre_close + 6 :]
            )
            print("Added PG: fillna/dropna aliases")

# ─── Fix section 17: Null-Safe Join section ───────────────────────────────────
nsj_h3 = "Null-Safe Join — &lt;=&gt; (SPARK-18525)"
h3_pattern = re.compile(
    r"(<h3>" + re.escape(nsj_h3) + r'</h3>.*?<pre class="code"><code>.*?</code></pre>)',
    re.DOTALL,
)
h3_match = h3_pattern.search(new_content)
if h3_match:
    py_end = h3_match.end()
    check = new_content[py_end : py_end + 400]
    if "PostgreSQL" not in check:
        pg_block = (
            '<div class="two-col" style="margin-top:0.3rem">'
            '<div class="panel"><h3>PostgreSQL</h3>'
            '<pre class="code"><code>SELECT a.id, a.region AS region_a, b.code\n'
            "FROM df_a a\n"
            "LEFT JOIN df_b b ON a.region IS NOT DISTINCT FROM b.region;</code></pre></div>"
            "</div>"
        )
        pre_close = new_content.find("</pre>", py_end)
        if pre_close > 0:
            new_content = (
                new_content[: pre_close + 6] + pg_block + new_content[pre_close + 6 :]
            )
            print("Added PG: Null-Safe Join")

# ─── Fix section 18-23: ensure all sub-sections have PostgreSQL ───────────────
# The datetime, math, string, window sections already have PostgreSQL panels
# but let me verify and fill any gaps

SECTIONS_TO_CHECK = ["datetime", "math", "string", "window", "lead-lag", "rows-between"]
for section_id in SECTIONS_TO_CHECK:
    section_match = re.search(
        r'<section[^>]+id="' + section_id + r'"[^>]*>(.*?)</section>',
        new_content,
        re.DOTALL,
    )
    if section_match:
        section_content = section_match.group(1)
        # Find all h3 sub-headings and check each has PostgreSQL
        h3s = re.findall(r"<h3>(.*?)</h3>", section_content)

        # Count PySpark blocks (they have 'from pyspark' or specific function names)
        py_blocks = len(re.findall(r"<h3>PySpark</h3>", section_content))
        pg_blocks = len(re.findall(r"<h3>PostgreSQL</h3>", section_content))
        print(f"  {section_id}: {py_blocks} PySpark, {pg_blocks} PostgreSQL")

# ─── Fix section 17 (Nulls) sub-sections ─────────────────────────────────────
null_section = re.search(
    r'<section[^>]+id="nulls"[^>]*>(.*?)</section>', new_content, re.DOTALL
)
if null_section:
    null_content = null_section.group(1)
    py_blocks = len(re.findall(r"<h3>PySpark</h3>", null_content))
    pg_blocks = len(re.findall(r"<h3>PostgreSQL</h3>", null_content))
    print(f"  nulls: {py_blocks} PySpark, {pg_blocks} PostgreSQL")

# ─── SAVE ─────────────────────────────────────────────────────────────────────
with open(PATH, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"\nSaved to {PATH}")
print(f"Total file size: {len(new_content)} bytes")
