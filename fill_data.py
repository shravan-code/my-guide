import re

PATH = r"D:\shra1\github\my-guide\spark\pyspark-code-guide.html"

with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

# ─── DATA DEFINITIONS ───────────────────────────────────────────────────────

DATA = {
    # ── SECTION 4: CSV ──
    "csv_read": {
        "input_cols": ["id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120"),
            ("2", "EMEA", "90"),
            ("3", "APAC", "220"),
        ],
        "output_cols": ["id", "region", "amount"],
        "output_rows": [
            (1, "APAC", 120.0),
            (2, "EMEA", 90.0),
            (3, "APAC", 220.0),
        ],
        "pyspark": """sales_csv = (spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("/data/sales.csv"))

sales_csv.printSchema()
sales_csv.show()""",
        "postgres": """CREATE TABLE sales (id INTEGER, region TEXT, amount NUMERIC);
COPY sales FROM '/data/sales.csv' WITH (FORMAT csv, HEADER true);

SELECT * FROM sales;""",
    },
    "csv_write": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", "EMEA", "90.0"),
            ("3", "APAC", "220.0"),
        ],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [
            (1, "APAC", 120.0),
            (2, "EMEA", 90.0),
            (3, "APAC", 220.0),
        ],
        "pyspark": """df = spark.createDataFrame([
    (1, "APAC", 120.0),
    (2, "EMEA", 90.0),
    (3, "APAC", 220.0),
], ["order_id", "region", "amount"])

df.write.mode("overwrite").option("header", True).csv("/tmp/sales_out")""",
        "postgres": """CREATE TABLE sales (order_id SERIAL, region TEXT, amount NUMERIC);
INSERT INTO sales (region, amount) VALUES
    ('APAC', 120.0), ('EMEA', 90.0), ('APAC', 220.0);

COPY (SELECT order_id, region, amount FROM sales) TO '/tmp/sales_out.csv'
    WITH (FORMAT csv, HEADER true);""",
    },
    # ── SECTION 5: JSON ──
    "json_read": {
        "input_cols": ["event", "value"],
        "input_rows": [
            ('{"event":"click","value":1}', '{"event":"view","value":5}'),
            ('{"event":"purchase","value":50}', '{"event":"signup","value":1}'),
        ],
        "output_cols": ["event", "value"],
        "output_rows": [
            ("click", 1),
            ("view", 5),
            ("purchase", 50),
            ("signup", 1),
        ],
        "pyspark": """events = (spark.read
    .option("multiLine", False)
    .json("/data/events.json"))

events.printSchema()
events.show(truncate=False)""",
        "postgres": """-- PostgreSQL reads JSON using jsonb_each / jsonb_array_elements
SELECT e.event, e.value
FROM events,
     jsonb_array_elements(raw::jsonb) WITH ORDINALITY AS arr(e);""",
    },
    "json_write": {
        "input_cols": ["id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", "EMEA", "90.0"),
        ],
        "output_cols": ["id", "region", "amount"],
        "output_rows": [
            (1, "APAC", 120.0),
            (2, "EMEA", 90.0),
        ],
        "pyspark": """df = spark.createDataFrame([
    (1, "APAC", 120.0),
    (2, "EMEA", 90.0),
], ["id", "region", "amount"])

df.write.mode("overwrite").json("/tmp/out_json")""",
        "postgres": """SELECT json_build_object(
    'id', id, 'region', region, 'amount', amount
) AS json_row
FROM sales;""",
    },
    # ── SECTION 6: PARQUET ──
    "parquet_read": {
        "input_cols": ["order_id", "customer_id", "event_date", "amount"],
        "input_rows": [
            ("101", "C1", "2026-03-01", "180.0"),
            ("102", "C2", "2026-03-01", "90.0"),
        ],
        "output_cols": ["order_id", "customer_id", "event_date", "amount"],
        "output_rows": [
            (101, "C1", "2026-03-01", 180.0),
            (102, "C2", "2026-03-01", 90.0),
        ],
        "pyspark": """orders_parquet = spark.read.parquet("/lake/raw/orders_parquet")
orders_parquet.printSchema()
orders_parquet.show()""",
        "postgres": """-- PostgreSQL: use parquet_fdw or convert with pg_to_parquet
SELECT * FROM read_parquet('/lake/raw/orders_parquet/*.parquet');""",
    },
    "parquet_write": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", "EMEA", "90.0"),
        ],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [
            (1, "APAC", 120.0),
            (2, "EMEA", 90.0),
        ],
        "pyspark": """df = spark.createDataFrame([
    (1, "APAC", 120.0),
    (2, "EMEA", 90.0),
], ["order_id", "region", "amount"])

df.write.mode("overwrite").parquet("/lake/curated/orders")""",
        "postgres": """-- PostgreSQL: write to parquet via COPY + Python
SELECT save_parquet('SELECT * FROM sales', '/lake/curated/orders');""",
    },
    # ── SECTION 7: AVRO ──
    "avro_read": {
        "input_cols": ["event_id", "user_id", "ts", "action"],
        "input_rows": [
            ("e1", "u1", "1709280000", "click"),
            ("e2", "u2", "1709280060", "view"),
        ],
        "output_cols": ["event_id", "user_id", "ts", "action"],
        "output_rows": [
            ("e1", "u1", 1709280000, "click"),
            ("e2", "u2", 1709280060, "view"),
        ],
        "pyspark": """events_avro = (spark.read
    .format("avro")
    .load("/lake/raw/events_avro"))

events_avro.printSchema()
events_avro.show()""",
        "postgres": """-- PostgreSQL: use avro_fdw or decode with Python library
SELECT * FROM read_avro('/lake/raw/events_avro/*.avro');""",
    },
    "avro_write": {
        "input_cols": ["event_id", "user_id", "action"],
        "input_rows": [
            ("e1", "u1", "click"),
            ("e2", "u2", "view"),
        ],
        "output_cols": ["event_id", "user_id", "action"],
        "output_rows": [
            ("e1", "u1", "click"),
            ("e2", "u2", "view"),
        ],
        "pyspark": """df = spark.createDataFrame([
    ("e1", "u1", "click"),
    ("e2", "u2", "view"),
], ["event_id", "user_id", "action"])

df.write.mode("overwrite").format("avro").save("/lake/curated/events")""",
        "postgres": """-- PostgreSQL: write Avro via Python (avro library)
import avro.schema, avro.datafile
-- Serialize rows to Avro and write to file""",
    },
    # ── SECTION 8: CLOUD ──
    "aws_s3": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", "EMEA", "90.0"),
        ],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [
            (1, "APAC", 120.0),
            (2, "EMEA", 90.0),
        ],
        "pyspark": """aws_path = "s3a://de-bucket/sales/orders"

df = spark.read.parquet(aws_path)
df.write.mode("overwrite").parquet("s3a://de-bucket/curated/orders")""",
        "postgres": """-- PostgreSQL: use S3 extension (postgres_fdw, aws_s3)
SELECT aws_s3.table_import_from_s3(
    'sales', 'order_id,region,amount', '(format csv, header)',
    'de-bucket', 'sales/orders/', 'us-east-1'
);""",
    },
    "azure_adls": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", "EMEA", "90.0"),
        ],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [
            (1, "APAC", 120.0),
            (2, "EMEA", 90.0),
        ],
        "pyspark": """# Set spark config:
# spark.read.parquet("abfss://container@account.dfs.core.windows.net/path")
# Requires: hadoop-azure, azure-storage jars

df = spark.read.parquet(
    "abfss://data@myaccount.dfs.core.windows.net/orders/"
)
df.write.mode("overwrite").parquet(
    "abfss://data@myaccount.dfs.core.windows.net/curated/orders"
)""",
        "postgres": """-- PostgreSQL: use azure_fdw or COPY with AzCopy
COPY sales FROM 'https://storage.blob.core.windows.net/container/orders/'
    WITH (FORMAT parquet);""",
    },
    "gcp_gcs": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", "EMEA", "90.0"),
        ],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [
            (1, "APAC", 120.0),
            (2, "EMEA", 90.0),
        ],
        "pyspark": """# Requires: spark.hadoop.google.cloud.auth.service.account.json.keyfile=/path/key.json
df = spark.read.parquet("gs://my-bucket/orders/")
df.write.mode("overwrite").parquet("gs://my-bucket/curated/orders")""",
        "postgres": """-- PostgreSQL: use gcs_fdw or gsutil to download + COPY
\! gsutil cp gs://my-bucket/orders/*.parquet /tmp/
COPY sales FROM '/tmp/orders.parquet' WITH (FORMAT parquet);""",
    },
    # ── SECTION 9: CLOUD LIBS ──
    "delta_table": {
        "input_cols": ["id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", "EMEA", "90.0"),
        ],
        "output_cols": ["id", "region", "amount", "version"],
        "output_rows": [
            (1, "APAC", 120.0, 0),
            (2, "EMEA", 90.0, 0),
            (1, "APAC", 150.0, 1),
        ],
        "pyspark": """from delta.tables import DeltaTable

dt = DeltaTable.forPath(spark, "/delta/orders")

# Read as streaming (live view)
df = spark.readStream.format("delta")
    .option("startingVersion", 0)
    .load("/delta/orders")

# Time-travel: read version 0
df_v0 = spark.read.format("delta")
    .option("versionAsOf", 0)
    .load("/delta/orders")

# Upsert (merge)
dt.alias("target").merge(
    updates_df.alias("source"),
    "target.id = source.id"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()""",
        "postgres": """-- PostgreSQL: use temporal tables or version column
CREATE TABLE orders (id SERIAL, region TEXT, amount NUMERIC, version INTEGER DEFAULT 0);

INSERT INTO orders (region, amount, version) VALUES ('APAC', 120.0, 0);
-- Version tracking via trigger
SELECT * FROM orders WHERE version = 0;  -- time-travel""",
    },
    "hudi": {
        "input_cols": ["id", "region", "amount", "ts"],
        "input_rows": [
            ("1", "APAC", "120.0", "1709280000"),
            ("2", "EMEA", "90.0", "1709280000"),
        ],
        "output_cols": ["id", "region", "amount", "ts", "hoodie_commit_time"],
        "output_rows": [
            (1, "APAC", 120.0, 1709280000, "20240101120000"),
            (2, "EMEA", 90.0, 1709280000, "20240101120000"),
        ],
        "pyspark": """df = (spark.read.format("hudi")
    .load("hoodie/path/"))

df.write.format("hudi") \\
    .option("hoodie.table.name", "orders") \\
    .option("hoodie.datasource.write.recordkey", "id") \\
    .option("hoodie.datasource.write.precombine.field", "ts") \\
    .mode("append") \\
    .save("hoodie/path/")""",
        "postgres": """-- PostgreSQL: use native INSERT ON CONFLICT for upserts
INSERT INTO orders (id, region, amount, ts)
VALUES (1, 'APAC', 120.0, '2024-03-01')
ON CONFLICT (id) DO UPDATE SET
    amount = EXCLUDED.amount, ts = EXCLUDED.ts;""",
    },
    "iceberg": {
        "input_cols": ["id", "region", "amount", "ts"],
        "input_rows": [
            ("1", "APAC", "120.0", "2024-03-01"),
            ("2", "EMEA", "90.0", "2024-03-01"),
        ],
        "output_cols": ["id", "region", "amount", "ts", "snapshot_id"],
        "output_rows": [
            (1, "APAC", 120.0, "2024-03-01", 1234567890),
            (2, "EMEA", 90.0, "2024-03-01", 1234567890),
        ],
        "pyspark": """df = (spark.read.format("iceberg")
    .load("s3://warehouse/db/orders"))

df.write.format("iceberg") \\
    .mode("overwrite") \\
    .option("write.format.default", "parquet") \\
    .saveAsTable("db.orders")

# Time-travel
df_old = spark.read.format("iceberg")
    .option("snapshot-id", 1234567890)
    .load("s3://warehouse/db/orders")""",
        "postgres": """-- PostgreSQL: native table versioning via branching
CREATE TABLE orders (id SERIAL, region TEXT, amount NUMERIC, ts TIMESTAMP);
-- Snapshot isolation is built-in with VACUUM time travel (Enterprise)
SELECT * FROM orders AS OF SYSTEM TIME '-1s';""",
    },
    # ── SECTION 10: EXCEL / COMPRESSION ──
    "excel_read": {
        "input_cols": ["id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", "EMEA", "90.0"),
        ],
        "output_cols": ["id", "region", "amount"],
        "output_rows": [
            (1, "APAC", 120.0),
            (2, "EMEA", 90.0),
        ],
        "pyspark": """excel_df = (spark.read
    .format("com.crealytics.spark.excel")
    .option("sheetName", "Sales")
    .option("useHeader", True)
    .option("inferSchema", True)
    .load("/data/sales.xlsx"))

excel_df.show()""",
        "postgres": """-- PostgreSQL: use pg_excel or read via odbc_fdw
CREATE EXTENSION odbc_fdw;
CREATE SERVER excel_srv FOREIGN DATA WRAPPER odbc_fdw
    OPTIONS (dsn 'Excel Files');

SELECT * FROM foreign_table;""",
    },
    "excel_write": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", "EMEA", "90.0"),
        ],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [
            (1, "APAC", 120.0),
            (2, "EMEA", 90.0),
        ],
        "pyspark": """df = spark.createDataFrame([
    (1, "APAC", 120.0),
    (2, "EMEA", 90.0),
], ["order_id", "region", "amount"])

(df.write
    .format("com.crealytics.spark.excel")
    .option("sheetName", "Report")
    .option("useHeader", True)
    .mode("overwrite")
    .save("/tmp/report.xlsx"))""",
        "postgres": """-- PostgreSQL: use COPY to CSV then convert to xlsx
COPY (SELECT * FROM sales) TO '/tmp/report.csv' WITH (FORMAT csv, HEADER true);
-- Use Python (openpyxl/pandas) to convert CSV → XLSX""",
    },
    "gzip_io": {
        "input_cols": ["id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", "EMEA", "90.0"),
        ],
        "output_cols": ["id", "region", "amount"],
        "output_rows": [
            (1, "APAC", 120.0),
            (2, "EMEA", 90.0),
        ],
        "pyspark": """# Read compressed CSV
df = (spark.read
    .option("compression", "gzip")
    .csv("/data/sales.csv.gz", header=True, inferSchema=True))

# Write as gzip compressed
(df.write
    .option("compression", "gzip")
    .mode("overwrite")
    .csv("/out/sales.csv", header=True))""",
        "postgres": """-- PostgreSQL: COPY supports compression via pipe
\\copy sales FROM 'gzip -d -c /data/sales.csv.gz' WITH (FORMAT csv, HEADER true)

-- Write with compression
COPY sales TO PROGRAM 'gzip > /tmp/sales.csv.gz' WITH (FORMAT csv, HEADER true);""",
    },
    "snappy_io": {
        "input_cols": ["id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", "EMEA", "90.0"),
        ],
        "output_cols": ["id", "region", "amount"],
        "output_rows": [
            (1, "APAC", 120.0),
            (2, "EMEA", 90.0),
        ],
        "pyspark": """df = (spark.read
    .parquet("s3://bucket/orders/"))

# Snappy is default compression for Parquet
(df.write
    .option("compression", "snappy")
    .mode("overwrite")
    .parquet("s3://bucket/orders/"))""",
        "postgres": """-- PostgreSQL: use ZSON or TOAST compression (built-in)
-- Snappy not natively supported; convert Parquet via Python""",
    },
    # ── SECTION 11: REF COLUMNS ──
    "col_expr": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", "EMEA", "90.0"),
        ],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [
            (1, "APAC", 120.0),
            (2, "EMEA", 90.0),
        ],
        "pyspark": """from pyspark.sql.functions import col, expr

# Refer as string (SQL-like)
df.select("order_id", "region", "amount")

# Refer as column object (composable, type-safe)
df.select(col("order_id"), col("region"), col("amount"))

# Use expr() for SQL expressions
df.select(expr("order_id + 100 AS new_id"), "region", "amount")""",
        "postgres": """-- String column: just use the name
SELECT order_id, region, amount FROM df;

-- Column expression
SELECT order_id + 100 AS new_id, region, amount FROM df;""",
    },
    "col_object": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", "EMEA", "90.0"),
        ],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [
            (1, "APAC", 120.0),
            (2, "EMEA", 90.0),
        ],
        "pyspark": """from pyspark.sql import Column
from pyspark.sql.functions import col, lit

# col() — most common for referencing existing columns
col("amount")          # Column reference
col("region") == "APAC"  # Boolean expression
~col("active")          # NOT

# lit() — create a literal/constant column
lit(42)
lit("APAC")

# Column object chaining
(col("amount") * 1.1).cast("int")""",
        "postgres": """-- No Column object equivalent; PostgreSQL uses SQL expressions directly
SELECT order_id, region, amount,
    amount * 1.1 AS scaled_amount
FROM df;""",
    },
    # ── SECTION 12: SELECT COLUMNS ──
    "select_basic": {
        "input_cols": ["order_id", "region", "amount", "raw_col"],
        "input_rows": [
            ("1", "APAC", "120.0", "x"),
            ("2", "EMEA", "90.0", "y"),
        ],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [
            (1, "APAC", 120.0),
            (2, "EMEA", 90.0),
        ],
        "pyspark": """projection = (df
    .select("order_id", "region", "amount"))

projection.show()""",
        "postgres": """SELECT order_id, region, amount FROM df;""",
    },
    "select_expr": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", "EMEA", "90.0"),
        ],
        "output_cols": ["order_id", "region", "amount_usd", "amount_eur"],
        "output_rows": [
            (1, "APAC", 120.0, 108.0),
            (2, "EMEA", 90.0, 81.0),
        ],
        "pyspark": """from pyspark.sql.functions import expr, col

result = df.select(
    "order_id", "region",
    col("amount").alias("amount_usd"),
    (col("amount") * 0.9).alias("amount_eur")
)

result.show()""",
        "postgres": """SELECT order_id, region,
    amount AS amount_usd,
    amount * 0.9 AS amount_eur
FROM df;""",
    },
    # ── SECTION 13: FILTERING ──
    "filter_startswith": {
        "input_cols": ["name", "region"],
        "input_rows": [
            ("Alpha Corp", "APAC"),
            ("Beta Ltd", "EMEA"),
            ("Gamma GmbH", "EMEA"),
        ],
        "output_cols": ["name", "region"],
        "output_rows": [
            ("Alpha Corp", "APAC"),
        ],
        "pyspark": """from pyspark.sql.functions import col

# startswith — prefix match
df.filter(col("name").startswith("Alpha")).show()""",
        "postgres": """SELECT * FROM df WHERE name LIKE 'Alpha%';""",
    },
    "filter_contains": {
        "input_cols": ["name", "region"],
        "input_rows": [
            ("Alpha Corp", "APAC"),
            ("Beta GmbH", "EMEA"),
            ("Gamma Ltd", "EMEA"),
        ],
        "output_cols": ["name", "region"],
        "output_rows": [
            ("Beta GmbH", "EMEA"),
            ("Gamma Ltd", "EMEA"),
        ],
        "pyspark": """from pyspark.sql.functions import col

# contains — substring anywhere
df.filter(col("name").contains("Ltd")).show()""",
        "postgres": """SELECT * FROM df WHERE name LIKE '%Ltd%';""",
    },
    "filter_endswith": {
        "input_cols": ["name", "region"],
        "input_rows": [
            ("Alpha Corp", "APAC"),
            ("Beta Ltd", "EMEA"),
            ("Gamma GmbH", "EMEA"),
        ],
        "output_cols": ["name", "region"],
        "output_rows": [
            ("Beta Ltd", "EMEA"),
        ],
        "pyspark": """from pyspark.sql.functions import col

# endswith — suffix match
df.filter(col("name").endswith("Ltd")).show()""",
        "postgres": """SELECT * FROM df WHERE name LIKE '%Ltd';""",
    },
    "filter_like": {
        "input_cols": ["name", "region"],
        "input_rows": [
            ("Alpha Corp", "APAC"),
            ("Beta Ltd", "EMEA"),
            ("Gamma AG", "EMEA"),
        ],
        "output_cols": ["name", "region"],
        "output_rows": [
            ("Alpha Corp", "APAC"),
            ("Gamma AG", "EMEA"),
        ],
        "pyspark": """from pyspark.sql.functions import col

# like — SQL LIKE pattern (%, _ wildcards)
df.filter(col("name").like("%or%")).show()""",
        "postgres": """SELECT * FROM df WHERE name LIKE '%or%';""",
    },
    "filter_rlike": {
        "input_cols": ["email", "region"],
        "input_rows": [
            ("alice@corp.com", "APAC"),
            ("bob@corp.com", "EMEA"),
            ("carol@corp.com", "APAC"),
        ],
        "output_cols": ["email", "region"],
        "output_rows": [
            ("alice@corp.com", "APAC"),
            ("bob@corp.com", "EMEA"),
            ("carol@corp.com", "APAC"),
        ],
        "pyspark": """from pyspark.sql.functions import col

# rlike — full Java regex
df.filter(col("email").rlike(r"^[a-z]+@corp\\.com$")).show()""",
        "postgres": """SELECT * FROM df WHERE email ~ '^[a-z]+@corp\\.com$';""",
    },
    # ── SECTION 14: GROUPING ──
    "group_basic": {
        "input_cols": ["region", "amount"],
        "input_rows": [
            ("APAC", "120.0"),
            ("APAC", "220.0"),
            ("EMEA", "90.0"),
        ],
        "output_cols": ["region", "total_amount", "avg_amount"],
        "output_rows": [
            ("APAC", 340.0, 170.0),
            ("EMEA", 90.0, 90.0),
        ],
        "pyspark": """from pyspark.sql.functions import sum as Fsum, avg

agg = (df
    .groupBy("region")
    .agg(
        Fsum("amount").alias("total_amount"),
        avg("amount").alias("avg_amount")
    ))

agg.show()""",
        "postgres": """SELECT region,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount
FROM df
GROUP BY region;""",
    },
    "group_multiple": {
        "input_cols": ["region", "priority", "amount"],
        "input_rows": [
            ("APAC", "H", "120.0"),
            ("APAC", "L", "220.0"),
            ("EMEA", "H", "90.0"),
        ],
        "output_cols": ["region", "priority", "total"],
        "output_rows": [
            ("APAC", "H", 120.0),
            ("APAC", "L", 220.0),
            ("EMEA", "H", 90.0),
        ],
        "pyspark": """from pyspark.sql.functions import sum as Fsum

result = (df
    .groupBy("region", "priority")
    .agg(Fsum("amount").alias("total")))

result.show()""",
        "postgres": """SELECT region, priority,
    SUM(amount) AS total
FROM df
GROUP BY region, priority;""",
    },
    "group_rollup": {
        "input_cols": ["region", "priority", "amount"],
        "input_rows": [
            ("APAC", "H", "120.0"),
            ("APAC", "L", "220.0"),
            ("EMEA", "H", "90.0"),
        ],
        "output_cols": ["region", "priority", "total_amount"],
        "output_rows": [
            ("APAC", "H", 120.0),
            ("APAC", "L", 220.0),
            ("APAC", None, 340.0),
            ("EMEA", "H", 90.0),
            ("EMEA", None, 90.0),
            (None, None, 430.0),
        ],
        "pyspark": """from pyspark.sql.functions import sum as Fsum, grouping_id

result = (df
    .rollup("region", "priority")
    .agg(Fsum("amount").alias("total_amount"))
    .withColumn("grp", grouping_id())
    .filter("grp = 0 OR grp = 1 OR grp = 3")
    .orderBy("region", "priority"))

result.show()""",
        "postgres": """SELECT region, priority,
    SUM(amount) AS total_amount
FROM df
GROUP BY ROLLUP (region, priority)
ORDER BY region, priority;""",
    },
    "group_cube": {
        "input_cols": ["region", "priority", "amount"],
        "input_rows": [
            ("APAC", "H", "120.0"),
            ("APAC", "L", "220.0"),
            ("EMEA", "H", "90.0"),
        ],
        "output_cols": ["region", "priority", "total_amount"],
        "output_rows": [
            ("APAC", "H", 120.0),
            ("APAC", "L", 220.0),
            ("APAC", None, 340.0),
            ("EMEA", "H", 90.0),
            ("EMEA", None, 90.0),
            (None, "H", 210.0),
            (None, "L", 220.0),
            (None, None, 430.0),
        ],
        "pyspark": """from pyspark.sql.functions import sum as Fsum, grouping_id

result = (df
    .cube("region", "priority")
    .agg(Fsum("amount").alias("total_amount"))
    .withColumn("grp", grouping_id())
    .filter("grp IN (0, 1, 2, 3)")
    .orderBy("region", "priority"))

result.show()""",
        "postgres": """SELECT region, priority,
    SUM(amount) AS total_amount
FROM df
GROUP BY CUBE (region, priority)
ORDER BY region, priority;""",
    },
    # ── SECTION 15: JOINING ──
    "join_left": {
        "input_a": ["order_id", "customer_id"],
        "input_a_rows": [("101", "C1"), ("102", "C2"), ("103", "C3")],
        "input_b": ["customer_id", "name"],
        "input_b_rows": [("C1", "Alice"), ("C4", "Bob")],
        "output_cols": ["order_id", "customer_id", "name"],
        "output_rows": [
            (101, "C1", "Alice"),
            (102, "C2", None),
            (103, "C3", None),
        ],
        "pyspark": """joined = orders.join(customers, "customer_id", "left")
joined.show()""",
        "postgres": """SELECT o.order_id, o.customer_id, c.name
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id;""",
    },
    "join_right": {
        "input_a": ["order_id", "customer_id"],
        "input_a_rows": [("101", "C1"), ("102", "C2")],
        "input_b": ["customer_id", "name"],
        "input_b_rows": [("C1", "Alice"), ("C2", "Carol"), ("C3", "Bob")],
        "output_cols": ["order_id", "customer_id", "name"],
        "output_rows": [
            (101, "C1", "Alice"),
            (102, "C2", "Carol"),
            (None, "C3", "Bob"),
        ],
        "pyspark": """joined = orders.join(customers, "customer_id", "right")
joined.show()""",
        "postgres": """SELECT o.order_id, o.customer_id, c.name
FROM orders o
RIGHT JOIN customers c ON o.customer_id = c.customer_id;""",
    },
    "join_outer": {
        "input_a": ["order_id", "customer_id"],
        "input_a_rows": [("101", "C1"), ("102", "C2"), ("105", "C5")],
        "input_b": ["customer_id", "name"],
        "input_b_rows": [("C1", "Alice"), ("C3", "Bob"), ("C4", "Carol")],
        "output_cols": ["order_id", "customer_id", "name"],
        "output_rows": [
            (101, "C1", "Alice"),
            (102, "C2", None),
            (None, "C3", "Bob"),
            (None, "C4", "Carol"),
            (105, "C5", None),
        ],
        "pyspark": """joined = orders.join(customers, "customer_id", "outer")
joined.show()""",
        "postgres": """SELECT o.order_id, o.customer_id, c.name
FROM orders o
FULL OUTER JOIN customers c ON o.customer_id = c.customer_id;""",
    },
    "join_leftsemi": {
        "input_a": ["order_id", "customer_id"],
        "input_a_rows": [("101", "C1"), ("102", "C2"), ("103", "C3")],
        "input_b": ["customer_id", "name"],
        "input_b_rows": [("C1", "Alice"), ("C3", "Bob")],
        "output_cols": ["order_id", "customer_id"],
        "output_rows": [
            (101, "C1"),
            (103, "C3"),
        ],
        "pyspark": """joined = orders.join(customers, "customer_id", "leftsemi")
joined.show()""",
        "postgres": """SELECT o.order_id, o.customer_id
FROM orders o
WHERE EXISTS (
    SELECT 1 FROM customers c WHERE c.customer_id = o.customer_id
);""",
    },
    "join_leftanti": {
        "input_a": ["order_id", "customer_id"],
        "input_a_rows": [("101", "C1"), ("102", "C2"), ("103", "C3")],
        "input_b": ["customer_id", "name"],
        "input_b_rows": [("C1", "Alice"), ("C3", "Bob")],
        "output_cols": ["order_id", "customer_id"],
        "output_rows": [
            (102, "C2"),
        ],
        "pyspark": """joined = orders.join(customers, "customer_id", "leftanti")
joined.show()""",
        "postgres": """SELECT o.order_id, o.customer_id
FROM orders o
WHERE NOT EXISTS (
    SELECT 1 FROM customers c WHERE c.customer_id = o.customer_id
);""",
    },
    "join_cross": {
        "input_a": ["id", "val"],
        "input_a_rows": [("1", "x"), ("2", "y")],
        "input_b": ["flag", "score"],
        "input_b_rows": [("A", 10), ("B", 20)],
        "output_cols": ["id", "val", "flag", "score"],
        "output_rows": [
            ("1", "x", "A", 10),
            ("1", "x", "B", 20),
            ("2", "y", "A", 10),
            ("2", "y", "B", 20),
        ],
        "pyspark": """joined = df_a.crossJoin(df_b)
joined.show()""",
        "postgres": """SELECT a.id, a.val, b.flag, b.score
FROM df_a a
CROSS JOIN df_b b;""",
    },
    "join_broadcast": {
        "input_a": ["order_id", "customer_id"],
        "input_a_rows": [("101", "C1"), ("102", "C2")],
        "input_b": ["customer_id", "name"],
        "input_b_rows": [("C1", "Alice"), ("C2", "Bob")],
        "output_cols": ["order_id", "customer_id", "name"],
        "output_rows": [
            (101, "C1", "Alice"),
            (102, "C2", "Bob"),
        ],
        "pyspark": """from pyspark.sql.functions import broadcast

joined = orders.join(broadcast(customers), "customer_id")
joined.show()""",
        "postgres": """-- For small tables, PostgreSQL always uses hash join (no broadcast needed)
-- Force nested loop for small dims:
SET enable_hashjoin = off;
SET enable_seqscan = off;""",
    },
    "join_self": {
        "input_cols": ["emp_id", "name", "manager_id"],
        "input_rows": [
            ("E1", "Alice", "E3"),
            ("E2", "Bob", "E3"),
            ("E3", "Carol", None),
        ],
        "output_cols": ["emp_id", "name", "mgr_id", "mgr_name"],
        "output_rows": [
            ("E1", "Alice", "E3", "Carol"),
            ("E2", "Bob", "E3", "Carol"),
            ("E3", "Carol", None, None),
        ],
        "pyspark": """employees = spark.createDataFrame([
    ("E1", "Alice", "E3"),
    ("E2", "Bob", "E3"),
    ("E3", "Carol", None),
], ["emp_id", "name", "manager_id"])

result = employees.alias("emp").join(
    employees.alias("mgr"),
    col("emp.manager_id") == col("mgr.emp_id"),
    "left"
).select("emp.emp_id", "emp.name", "mgr.emp_id", "mgr.name")

result.show()""",
        "postgres": """SELECT e.emp_id, e.name, e.manager_id, m.name AS mgr_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id;""",
    },
    "join_multicol": {
        "input_a": ["order_id", "region", "product_id"],
        "input_a_rows": [
            ("101", "APAC", "P1"),
            ("102", "APAC", "P2"),
            ("103", "EMEA", "P1"),
        ],
        "input_b": ["region", "product_id", "discount"],
        "input_b_rows": [
            ("APAC", "P1", 0.1),
            ("EMEA", "P1", 0.2),
            ("APAC", "P2", 0.05),
        ],
        "output_cols": ["order_id", "region", "product_id", "discount"],
        "output_rows": [
            (101, "APAC", "P1", 0.1),
            (102, "APAC", "P2", 0.05),
            (103, "EMEA", "P1", 0.2),
        ],
        "pyspark": """joined = orders.join(discounts, ["region", "product_id"])
joined.show()""",
        "postgres": """SELECT o.order_id, o.region, o.product_id, d.discount
FROM orders o
JOIN discounts d USING (region, product_id);""",
    },
    # ── SECTION 16: PIVOTING ──
    "pivot_basic": {
        "input_cols": ["region", "event_type", "count"],
        "input_rows": [
            ("APAC", "view", "1"),
            ("APAC", "click", "1"),
            ("EMEA", "purchase", "1"),
        ],
        "output_cols": ["region", "view", "click", "purchase"],
        "output_rows": [
            ("APAC", 1, 1, 0),
            ("EMEA", 0, 0, 1),
        ],
        "pyspark": """pivoted = (df
    .groupBy("region")
    .pivot("event_type", ["view", "click", "purchase"])
    .agg(f.sum("count"))
    .na.fill(0))

pivoted.show()""",
        "postgres": """SELECT region,
    COUNT(*) FILTER (WHERE event_type = 'view')     AS view,
    COUNT(*) FILTER (WHERE event_type = 'click')    AS click,
    COUNT(*) FILTER (WHERE event_type = 'purchase') AS purchase
FROM df
GROUP BY region;""",
    },
    # ── SECTION 17: NULLS ──
    "nulls_fill": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", None, "95.0"),
            ("3", "EMEA", None),
        ],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [
            (1, "APAC", 120.0),
            (2, "UNKNOWN", 95.0),
            (3, "EMEA", 0.0),
        ],
        "pyspark": """# Fill all nulls with a single value (type must match column)
df.na.fill({"region": "UNKNOWN", "amount": 0.0}).show()""",
        "postgres": """SELECT order_id,
    COALESCE(region, 'UNKNOWN') AS region,
    COALESCE(amount, 0.0) AS amount
FROM df;""",
    },
    "nulls_coalesce": {
        "input_cols": ["order_id", "primary_region", "backup_region"],
        "input_rows": [
            ("1", "APAC", None),
            ("2", None, "EMEA"),
            ("3", "APAC", "US"),
        ],
        "output_cols": ["order_id", "region"],
        "output_rows": [
            (1, "APAC"),
            (2, "EMEA"),
            (3, "APAC"),
        ],
        "pyspark": """from pyspark.sql.functions import coalesce, col

result = df.select(
    "order_id",
    coalesce(col("primary_region"), col("backup_region")).alias("region")
)

result.show()""",
        "postgres": """SELECT order_id,
    COALESCE(primary_region, backup_region) AS region
FROM df;""",
    },
    "nulls_when": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", None, "95.0"),
            ("3", "EMEA", None),
        ],
        "output_cols": ["order_id", "region", "amount", "label"],
        "output_rows": [
            (1, "APAC", 120.0, "normal"),
            (2, "UNKNOWN", 95.0, "no_region"),
            (3, "EMEA", 0.0, "zero_amount"),
        ],
        "pyspark": """from pyspark.sql.functions import when, col, lit

result = df.select(
    "order_id",
    when(col("region").isNull(), "UNKNOWN").otherwise(col("region")).alias("region"),
    when(col("amount").isNull(), 0.0).otherwise(col("amount")).alias("amount"),
    when(col("region").isNull(), "no_region")
     .when(col("amount").isNull(), "zero_amount")
     .otherwise("normal").alias("label")
)

result.show()""",
        "postgres": """SELECT order_id,
    COALESCE(region, 'UNKNOWN') AS region,
    COALESCE(amount, 0.0) AS amount,
    CASE
        WHEN region IS NULL THEN 'no_region'
        WHEN amount IS NULL THEN 'zero_amount'
        ELSE 'normal'
    END AS label
FROM df;""",
    },
    "nulls_replace": {
        "input_cols": ["order_id", "region", "status"],
        "input_rows": [
            ("1", "APAC", "pending"),
            ("2", "EMEA", "unknown"),
            ("3", "US", "n/a"),
        ],
        "output_cols": ["order_id", "region", "status"],
        "output_rows": [
            (1, "APAC", "pending"),
            (2, "EMEA", "unknown"),
            (3, "US", "unknown"),
        ],
        "pyspark": """# Replace specific values (not just nulls) in specific columns
df.na.replace(["n/a"], ["unknown"], "status").show()""",
        "postgres": """SELECT order_id, region,
    CASE WHEN status = 'n/a' THEN 'unknown' ELSE status END AS status
FROM df;""",
    },
    "nulls_safesearch": {
        "input_a": ["id", "region"],
        "input_a_rows": [("1", "APAC"), ("2", None), ("3", "EMEA")],
        "input_b": ["region", "code"],
        "input_b_rows": [(None, "XX"), ("EMEA", "EM")],
        "output_cols": ["id", "region_a", "code"],
        "output_rows": [
            (1, "APAC", None),
            (2, None, "XX"),
            (3, "EMEA", "EM"),
        ],
        "pyspark": """# Null-safe equality: null == null is TRUE (unlike regular ==)
result = df_a.join(df_b, df_a["region"] <=> df_b["region"], "left")
result.show()""",
        "postgres": """SELECT a.id, a.region AS region_a, b.code
FROM df_a a
LEFT JOIN df_b b ON a.region IS NOT DISTINCT FROM b.region;""",
    },
    # ── SECTION 18: DATETIME ──
    "datetime_date_format": {
        "input_cols": ["event_time"],
        "input_rows": [("2026-03-01 14:30:00",)],
        "output_cols": ["event_date", "event_ts"],
        "output_rows": [
            ("2026-03-01", "2026-03-01 14:30:00"),
        ],
        "pyspark": """from pyspark.sql.functions import date_format

df.select(
    date_format("event_time", "yyyy-MM-dd").alias("event_date"),
    date_format("event_time", "HH:mm:ss").alias("event_ts")
).show()""",
        "postgres": """SELECT
    TO_CHAR(event_time, 'YYYY-MM-DD') AS event_date,
    TO_CHAR(event_time, 'HH24:MI:SS') AS event_ts
FROM df;""",
    },
    "datetime_trunc": {
        "input_cols": ["event_ts"],
        "input_rows": [("2026-03-01 14:30:00",)],
        "output_cols": ["event_ts", "trunc_day", "trunc_month", "trunc_year"],
        "output_rows": [
            (
                "2026-03-01 14:30:00",
                "2026-03-01 00:00:00",
                "2026-03-01 00:00:00",
                "2026-01-01 00:00:00",
            ),
        ],
        "pyspark": """from pyspark.sql.functions import date_trunc

df.select(
    "event_ts",
    date_trunc("day", "event_ts").alias("trunc_day"),
    date_trunc("month", "event_ts").alias("trunc_month"),
    date_trunc("year", "event_ts").alias("trunc_year")
).show()""",
        "postgres": """SELECT event_ts,
    DATE_TRUNC('day', event_ts)    AS trunc_day,
    DATE_TRUNC('month', event_ts)  AS trunc_month,
    DATE_TRUNC('year', event_ts)   AS trunc_year
FROM df;""",
    },
    "datetime_extract": {
        "input_cols": ["event_ts"],
        "input_rows": [("2026-03-01 14:30:00",)],
        "output_cols": ["event_ts", "year", "month", "day", "hour", "minute", "second"],
        "output_rows": [
            ("2026-03-01 14:30:00", 2026, 3, 1, 14, 30, 0),
        ],
        "pyspark": """from pyspark.sql.functions import year, month, day, hour, minute, second

df.select(
    "event_ts",
    year("event_ts").alias("year"),
    month("event_ts").alias("month"),
    day("event_ts").alias("day"),
    hour("event_ts").alias("hour"),
    minute("event_ts").alias("minute"),
    second("event_ts").alias("second")
).show()""",
        "postgres": """SELECT event_ts,
    EXTRACT(YEAR    FROM event_ts) AS year,
    EXTRACT(MONTH   FROM event_ts) AS month,
    EXTRACT(DAY     FROM event_ts) AS day,
    EXTRACT(HOUR    FROM event_ts) AS hour,
    EXTRACT(MINUTE  FROM event_ts) AS minute,
    EXTRACT(SECOND  FROM event_ts) AS second
FROM df;""",
    },
    "datetime_dow": {
        "input_cols": ["event_date"],
        "input_rows": [("2026-03-01",), ("2026-03-07",), ("2026-03-08",)],
        "output_cols": [
            "event_date",
            "dayofweek",
            "dayofmonth",
            "dayofyear",
            "quarter",
            "weekofyear",
        ],
        "output_rows": [
            ("2026-03-01", 1, 1, 60, 1, 9),
            ("2026-03-07", 7, 7, 66, 1, 10),
            ("2026-03-08", 1, 8, 67, 1, 10),
        ],
        "pyspark": """from pyspark.sql.functions import dayofweek, dayofmonth, dayofyear, quarter, weekofyear

df.select(
    "event_date",
    dayofweek("event_date").alias("dayofweek"),
    dayofmonth("event_date").alias("dayofmonth"),
    dayofyear("event_date").alias("dayofyear"),
    quarter("event_date").alias("quarter"),
    weekofyear("event_date").alias("weekofyear")
).show()""",
        "postgres": """SELECT event_date,
    EXTRACT(DOW         FROM event_date) AS dayofweek,
    EXTRACT(DAY         FROM event_date) AS dayofmonth,
    EXTRACT(DOY         FROM event_date) AS dayofyear,
    EXTRACT(QUARTER     FROM event_date) AS quarter,
    EXTRACT(WEEK        FROM event_date) AS weekofyear
FROM df;""",
    },
    "datetime_datediff": {
        "input_cols": ["start_date", "end_date"],
        "input_rows": [("2026-01-01", "2026-03-01"), ("2026-01-01", "2026-01-15")],
        "output_cols": [
            "start_date",
            "end_date",
            "days_diff",
            "months_diff",
            "days_add",
        ],
        "output_rows": [
            ("2026-01-01", "2026-03-01", 59, 2.0, "2026-03-11"),
            ("2026-01-01", "2026-01-15", 14, 0.5, "2026-01-16"),
        ],
        "pyspark": """from pyspark.sql.functions import datediff, months_between, date_add

df.select(
    "start_date", "end_date",
    datediff("end_date", "start_date").alias("days_diff"),
    months_between("end_date", "start_date").alias("months_diff"),
    date_add("start_date", 10).alias("days_add")
).show()""",
        "postgres": """SELECT start_date, end_date,
    (end_date - start_date)                           AS days_diff,
    EXTRACT(EPOCH FROM (end_date - start_date)) / 30.44 AS months_diff,
    start_date + INTERVAL '10 days'                   AS days_add
FROM df;""",
    },
    "datetime_addmonths": {
        "input_cols": ["event_date"],
        "input_rows": [("2026-01-15",), ("2026-03-01",)],
        "output_cols": ["event_date", "add_months", "next_day", "last_day"],
        "output_rows": [
            ("2026-01-15", "2026-04-15", "2026-01-19", "2026-01-31"),
            ("2026-03-01", "2026-06-01", "2026-03-02", "2026-03-31"),
        ],
        "pyspark": """from pyspark.sql.functions import add_months, next_day, last_day

df.select(
    "event_date",
    add_months("event_date", 3).alias("add_months"),
    next_day("event_date", "Mon").alias("next_day"),
    last_day("event_date").alias("last_day")
).show()""",
        "postgres": """SELECT event_date,
    event_date + INTERVAL '3 months'        AS add_months,
    (SELECT MIN(d) FROM generate_series(event_date, event_date + INTERVAL '7 days') AS d
     WHERE EXTRACT(DOW FROM d) = 2)          AS next_day,
    DATE_TRUNC('month', event_date) + INTERVAL '1 month' - INTERVAL '1 day' AS last_day
FROM df;""",
    },
    "datetime_unix": {
        "input_cols": ["event_ts"],
        "input_rows": [("2026-03-01 14:30:00",)],
        "output_cols": ["event_ts", "unix_ts", "from_unix"],
        "output_rows": [
            ("2026-03-01 14:30:00", 1772549400, "2026-03-01 14:30:00"),
        ],
        "pyspark": """from pyspark.sql.functions import unix_timestamp, from_unixtime

df.select(
    "event_ts",
    unix_timestamp("event_ts").alias("unix_ts"),
    from_unixtime(1772549400).alias("from_unix")
).show()""",
        "postgres": """SELECT event_ts,
    EXTRACT(EPOCH FROM event_ts)::BIGINT AS unix_ts,
    TO_TIMESTAMP(1772549400)             AS from_unix
FROM df;""",
    },
    "datetime_timezone": {
        "input_cols": ["utc_time"],
        "input_rows": [("2026-03-01 14:30:00",)],
        "output_cols": ["utc_time", "to_utc", "from_utc"],
        "output_rows": [
            ("2026-03-01 14:30:00", "2026-03-01 22:30:00", "2026-03-01 06:30:00"),
        ],
        "pyspark": """from pyspark.sql.functions import to_utc_timestamp, from_utc_timestamp

df.select(
    "utc_time",
    to_utc_timestamp("utc_time", "Asia/Kolkata").alias("to_utc"),
    from_utc_timestamp("utc_time", "US/Pacific").alias("from_utc")
).show()""",
        "postgres": """SELECT utc_time,
    utc_time AT TIME ZONE 'Asia/Kolkata' AS to_utc,
    (utc_time AT TIME ZONE 'UTC') AT TIME ZONE 'US/Pacific' AS from_utc
FROM df;""",
    },
    "datetime_make_date": {
        "input_cols": ["yr", "mo", "dy"],
        "input_rows": [(2026, 3, 1), (2026, 12, 25)],
        "output_cols": ["yr", "mo", "dy", "date"],
        "output_rows": [
            (2026, 3, 1, "2026-03-01"),
            (2026, 12, 25, "2026-12-25"),
        ],
        "pyspark": """from pyspark.sql.functions import make_date

df.select(
    "yr", "mo", "dy",
    make_date("yr", "mo", "dy").alias("date")
).show()""",
        "postgres": """SELECT yr, mo, dy,
    MAKE_DATE(yr, mo, dy) AS date
FROM df;""",
    },
    # ── SECTION 19: MATH ──
    "math_floor_ceil": {
        "input_cols": ["price"],
        "input_rows": [("12.7",), ("8.1",), ("15.9",)],
        "output_cols": ["price", "floor", "ceil", "round", "bround"],
        "output_rows": [
            (12.7, 12, 13, 13, 13),
            (8.1, 8, 9, 8, 8),
            (15.9, 15, 16, 16, 16),
        ],
        "pyspark": """from pyspark.sql.functions import floor, ceil, round, bround

df.select(
    "price",
    floor("price").alias("floor"),
    ceil("price").alias("ceil"),
    round("price", 0).alias("round"),
    bround("price", 0).alias("bround")
).show()""",
        "postgres": """SELECT price,
    FLOOR(price)    AS floor_val,
    CEIL(price)     AS ceil_val,
    ROUND(price, 0) AS round_val,
    ROUND(price, 0) AS bround  -- PostgreSQL rounds half-up (same as bround for positive)
FROM df;""",
    },
    "math_greatest_least": {
        "input_cols": ["a", "b", "c"],
        "input_rows": [(5, 8, 3), (10, 2, 7)],
        "output_cols": ["a", "b", "c", "greatest", "least"],
        "output_rows": [
            (5, 8, 3, 8, 3),
            (10, 2, 7, 10, 2),
        ],
        "pyspark": """from pyspark.sql.functions import greatest, least

df.select(
    "a", "b", "c",
    greatest("a", "b", "c").alias("greatest"),
    least("a", "b", "c").alias("least")
).show()""",
        "postgres": """SELECT a, b, c,
    GREATEST(a, b, c) AS greatest,
    LEAST(a, b, c)    AS least
FROM df;""",
    },
    "math_trig": {
        "input_cols": ["angle_deg"],
        "input_rows": [(0,), (90,), (45,)],
        "output_cols": ["angle_deg", "radians", "cos", "sin", "tan"],
        "output_rows": [
            (0, 0.0, 1.0, 0.0, 0.0),
            (90, 1.5708, 0.0, 1.0, None),
            (45, 0.7854, 0.7071, 0.7071, 1.0),
        ],
        "pyspark": """from pyspark.sql.functions import cos, sin, tan, radians

df.select(
    "angle_deg",
    radians("angle_deg").alias("radians"),
    cos("angle_deg").alias("cos"),
    sin("angle_deg").alias("sin"),
    tan("angle_deg").alias("tan")
).show()""",
        "postgres": """SELECT angle_deg,
    RADIANS(angle_deg) AS radians,
    COS(RADIANS(angle_deg)) AS cos,
    SIN(RADIANS(angle_deg)) AS sin,
    TAN(RADIANS(angle_deg)) AS tan
FROM df;""",
    },
    "math_bin_hex": {
        "input_cols": ["num"],
        "input_rows": [(10,), (255,), (16,)],
        "output_cols": ["num", "bin_str", "hex_str", "from_hex"],
        "output_rows": [
            (10, "1010", "A", 255),
            (255, "11111111", "FF", 255),
            (16, "10000", "10", 255),
        ],
        "pyspark": """from pyspark.sql.functions import bin, hex, unhex

df.select(
    "num",
    bin("num").alias("bin_str"),
    hex("num").alias("hex_str"),
    unhex(hex("num")).alias("from_hex")
).show()""",
        "postgres": """SELECT num,
    TO_BINARY(NUM, 'HEX')::TEXT AS bin_str,  -- PostgreSQL 16+
    UPPER(TO_HEX(num))           AS hex_str,
    (SELECT SUM((byte * 256^idx)::BIGINT)
     FROM unnest(TO_BINARY(num, 'HEX')) WITH ORDINALITY AS b(byte, idx)) AS from_hex
FROM df;""",
    },
    "math_nanvl": {
        "input_cols": ["value"],
        "input_rows": [("NaN",), ("12.5",), ("NULL",)],
        "output_cols": ["value", "nanvl_default"],
        "output_rows": [
            ("NaN", 0.0),
            ("12.5", 12.5),
            ("NULL", 0.0),
        ],
        "pyspark": """from pyspark.sql.functions import nanvl

df.select(
    "value",
    nanvl("value", 0.0).alias("nanvl_default")
).show()""",
        "postgres": """SELECT value,
    CASE WHEN value::TEXT = 'NaN' THEN 0.0 ELSE value::NUMERIC END AS nanvl_default
FROM df;""",
    },
    "math_width_bucket": {
        "input_cols": ["score"],
        "input_rows": [(10,), (55,), (85,), (120,)],
        "output_cols": ["score", "bucket_4"],
        "output_rows": [
            (10, 1),
            (55, 3),
            (85, 4),
            (120, 5),
        ],
        "pyspark": """from pyspark.sql.functions import width_bucket

df.select(
    "score",
    width_bucket("score", lit(0), lit(100), lit(4)).alias("bucket_4")
).show()""",
        "postgres": """SELECT score,
    WIDTH_BUCKET(score, 0, 100, 4) AS bucket_4
FROM df;""",
    },
    "math_cbrt": {
        "input_cols": ["num"],
        "input_rows": [(8,), (27,), (64,)],
        "output_cols": ["num", "cbrt"],
        "output_rows": [
            (8, 2.0),
            (27, 3.0),
            (64, 4.0),
        ],
        "pyspark": """from pyspark.sql.functions import cbrt

df.select("num", cbrt("num").alias("cbrt")).show()""",
        "postgres": """SELECT num, CBRT(num) AS cbrt FROM df;""",
    },
    "math_factorial": {
        "input_cols": ["n"],
        "input_rows": [(0,), (1,), (5,)],
        "output_cols": ["n", "factorial"],
        "output_rows": [
            (0, 1),
            (1, 1),
            (5, 120),
        ],
        "pyspark": """from pyspark.sql.functions import factorial

df.select("n", factorial("n").alias("factorial")).show()""",
        "postgres": """SELECT n, (SELECT FACTORIAL(n)) AS factorial FROM df;
-- Or use a math extension""",
    },
    "math_conv": {
        "input_cols": ["num_bin"],
        "input_rows": [("1010",), ("FF",)],
        "output_cols": ["num_bin", "to_dec", "to_hex"],
        "output_rows": [
            ("1010", 10, "A"),
            ("FF", 255, "FF"),
        ],
        "pyspark": """from pyspark.sql.functions import conv

df.select(
    "num_bin",
    conv("num_bin", 2, 10).alias("to_dec"),
    conv("num_bin", 2, 16).alias("to_hex")
).show()""",
        "postgres": """SELECT num_bin,
    ('0x' || num_bin)::BIT(32)::INT    AS to_dec,
    UPPER(TO_HEX(('0x' || num_bin)::INT)) AS to_hex
FROM df;""",
    },
    # ── SECTION 20: STRING ──
    "string_trim": {
        "input_cols": ["name"],
        "input_rows": [("  Alice  ",), ("##Bob##",)],
        "output_cols": ["name", "trim_l", "trim_r", "trim_b"],
        "output_rows": [
            ("  Alice  ", "Alice  ", "  Alice", "Alice"),
            ("##Bob##", "Bob##", "##Bob", "Bob"),
        ],
        "pyspark": """from pyspark.sql.functions import ltrim, rtrim, trim

df.select(
    "name",
    ltrim("name").alias("trim_l"),
    rtrim("name").alias("trim_r"),
    trim("name").alias("trim_b")
).show()""",
        "postgres": """SELECT name,
    LTRIM(name)  AS trim_l,
    RTRIM(name)  AS trim_r,
    BTRIM(name)  AS trim_b
FROM df;""",
    },
    "string_concat": {
        "input_cols": ["first", "last"],
        "input_rows": [("Alice", "Corp"), ("Bob", "Ltd")],
        "output_cols": ["first", "last", "full_name", "dash_name"],
        "output_rows": [
            ("Alice", "Corp", "AliceCorp", "Alice-Corp"),
            ("Bob", "Ltd", "BobLtd", "Bob-Ltd"),
        ],
        "pyspark": """from pyspark.sql.functions import concat, concat_ws

df.select(
    "first", "last",
    concat("first", "last").alias("full_name"),
    concat_ws("-", "first", "last").alias("dash_name")
).show()""",
        "postgres": """SELECT first, last,
    first || last   AS full_name,
    CONCAT_WS('-', first, last) AS dash_name
FROM df;""",
    },
    "string_substring": {
        "input_cols": ["code"],
        "input_rows": [("ABC-123-XYZ",), ("XX-999-YY",)],
        "output_cols": ["code", "prefix", "mid", "suffix"],
        "output_rows": [
            ("ABC-123-XYZ", "ABC", "123", "XYZ"),
            ("XX-999-YY", "XX", "999", "YY"),
        ],
        "pyspark": """from pyspark.sql.functions import substring

df.select(
    "code",
    substring("code", 1, 3).alias("prefix"),
    substring("code", 5, 3).alias("mid"),
    substring("code", 9, 3).alias("suffix")
).show()""",
        "postgres": """SELECT code,
    LEFT(code, 3)    AS prefix,
    SUBSTRING(code, 5, 3) AS mid,
    RIGHT(code, 3)  AS suffix
FROM df;""",
    },
    "string_split": {
        "input_cols": ["path"],
        "input_rows": [("a,b,c",), ("x/y/z",)],
        "output_cols": ["path", "parts"],
        "output_rows": [
            ("a,b,c", ["a", "b", "c"]),
            ("x/y/z", ["x", "y", "z"]),
        ],
        "pyspark": """from pyspark.sql.functions import split

df.select(
    "path",
    split("path", ",").alias("parts")
).show(truncate=False)""",
        "postgres": """SELECT path,
    STRING_TO_ARRAY(path, ',') AS parts
FROM df;""",
    },
    "string_regexp_extract": {
        "input_cols": ["email"],
        "input_rows": [("alice@corp.com",), ("bob+tag@corp.com",)],
        "output_cols": ["email", "user", "domain"],
        "output_rows": [
            ("alice@corp.com", "alice", "corp.com"),
            ("bob+tag@corp.com", "bob+tag", "corp.com"),
        ],
        "pyspark": """from pyspark.sql.functions import regexp_extract

df.select(
    "email",
    regexp_extract("email", r"([^@]+)", 1).alias("user"),
    regexp_extract("email", r"@(.+)", 1).alias("domain")
).show()""",
        "postgres": """SELECT email,
    (REGEXP_MATCHES(email, '([^@]+)@'))[1] AS user,
    REGEXP_REPLACE(email, '.*@', '')        AS domain
FROM df;""",
    },
    "string_regexp_replace": {
        "input_cols": ["phone"],
        "input_rows": [("(555) 123-4567",), ("+1-800-999-1234",)],
        "output_cols": ["phone", "cleaned"],
        "output_rows": [
            ("(555) 123-4567", "5551234567"),
            ("+1-800-999-1234", "18009991234"),
        ],
        "pyspark": """from pyspark.sql.functions import regexp_replace

df.select(
    "phone",
    regexp_replace("phone", r"[^0-9]", "", "g").alias("cleaned")
).show()""",
        "postgres": """SELECT phone,
    REGEXP_REPLACE(phone, '[^0-9]', '', 'g') AS cleaned
FROM df;""",
    },
    "string_overlay": {
        "input_cols": ["text"],
        "input_rows": [("ABCDEFGH",)],
        "output_cols": ["text", "replaced"],
        "output_rows": [
            ("ABCDEFGH", "ABXXXXGH"),
        ],
        "pyspark": """from pyspark.sql.functions import overlay

df.select(
    "text",
    overlay("text", lit("XXXX"), 3, 5).alias("replaced")
).show()""",
        "postgres": """SELECT text,
    OVERLAY(text PLACING 'XXXX' FROM 3 FOR 5) AS replaced
FROM df;""",
    },
    "string_repeat": {
        "input_cols": ["text"],
        "input_rows": [("HA",), ("na",)],
        "output_cols": ["text", "laugh"],
        "output_rows": [
            ("HA", "HAHHA"),
            ("na", "nanana"),
        ],
        "pyspark": """from pyspark.sql.functions import repeat

df.select(
    "text",
    concat(repeat("text", 2), lit(" "), repeat("text", 1)).alias("laugh")
).show()""",
        "postgres": """SELECT text,
    REPEAT(text, 2) || ' ' || text AS laugh
FROM df;""",
    },
    "string_soundex": {
        "input_cols": ["name"],
        "input_rows": [("Alice",), ("Alicia",), ("Elise",)],
        "output_cols": ["name", "soundex", "levenshtein_to_alice"],
        "output_rows": [
            ("Alice", "A400", 0),
            ("Alicia", "A420", 1),
            ("Elise", "E420", 2),
        ],
        "pyspark": """from pyspark.sql.functions import soundex, levenshtein

df.select(
    "name",
    soundex("name").alias("soundex"),
    levenshtein(lit("Alice"), "name").alias("levenshtein_to_alice")
).show()""",
        "postgres": """SELECT name,
    SOUNDEX(name) AS soundex
FROM df;

-- Levenshtein requires extension:
-- CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
-- SELECT name, LEVENSHTEIN('Alice', name) AS levenshtein_to_alice FROM df;""",
    },
    "string_ascii_chr": {
        "input_cols": ["ch", "code"],
        "input_rows": [("A", "65"), ("Z", "90")],
        "output_cols": ["ch", "code", "ascii_code", "chr_code"],
        "output_rows": [
            ("A", "65", 65, "A"),
            ("Z", "90", 90, "Z"),
        ],
        "pyspark": """from pyspark.sql.functions import ascii, chr

df.select(
    "ch", "code",
    ascii("ch").alias("ascii_code"),
    chr("code").alias("chr_code")
).show()""",
        "postgres": """SELECT ch, code,
    ASCII(ch)  AS ascii_code,
    CHR(code::INT) AS chr_code
FROM df;""",
    },
    "string_format": {
        "input_cols": ["name", "score"],
        "input_rows": [("Alice", 85), ("Bob", 72)],
        "output_cols": ["name", "score", "formatted"],
        "output_rows": [
            ("Alice", 85, "Alice scored 85 points"),
            ("Bob", 72, "Bob scored 72 points"),
        ],
        "pyspark": """from pyspark.sql.functions import format_string

df.select(
    "name", "score",
    format_string("%s scored %d points", "name", "score").alias("formatted")
).show()""",
        "postgres": """SELECT name, score,
    FORMAT('%s scored %s points', name, score) AS formatted
FROM df;""",
    },
    "string_locate": {
        "input_cols": ["text", "sub"],
        "input_rows": [("Hello World", "World"), ("Hello World", "xyz")],
        "output_cols": ["text", "sub", "pos"],
        "output_rows": [
            ("Hello World", "World", 7),
            ("Hello World", "xyz", 0),
        ],
        "pyspark": """from pyspark.sql.functions import locate

df.select(
    "text", "sub",
    locate("sub", "text", 1).alias("pos")
).show()""",
        "postgres": """SELECT text, sub,
    POSITION(sub IN text) AS pos
FROM df;""",
    },
    # ── SECTION 21: WINDOW ──
    "window_def": {
        "input_cols": ["region", "event_time", "amount"],
        "input_rows": [
            ("APAC", "2026-01-01", "120.0"),
            ("APAC", "2026-01-02", "80.0"),
            ("EMEA", "2026-01-01", "90.0"),
        ],
        "output_cols": ["region", "event_time", "amount"],
        "output_rows": [
            ("APAC", "2026-01-01", 120.0),
            ("APAC", "2026-01-02", 80.0),
            ("EMEA", "2026-01-01", 90.0),
        ],
        "pyspark": """from pyspark.sql import Window
from pyspark.sql.functions import desc

w = (Window
    .partitionBy("region")
    .orderBy(desc("event_time")))

df.withColumn("rank", f.row_number().over(w)).show()""",
        "postgres": """SELECT *,
    ROW_NUMBER() OVER (
        PARTITION BY region
        ORDER BY event_time DESC
    ) AS rank
FROM df;""",
    },
    "window_row_number": {
        "input_cols": ["region", "amount"],
        "input_rows": [
            ("APAC", "120.0"),
            ("APAC", "220.0"),
            ("EMEA", "90.0"),
        ],
        "output_cols": ["region", "amount", "rn", "rank", "dense_rank"],
        "output_rows": [
            ("APAC", 120.0, 1, 1, 1),
            ("APAC", 220.0, 2, 2, 2),
            ("EMEA", 90.0, 1, 1, 1),
        ],
        "pyspark": """from pyspark.sql import Window
import pyspark.sql.functions as f

w = Window.partitionBy("region").orderBy("amount")

df.withColumn("rn",         f.row_number().over(w)) \\
   .withColumn("rank",       f.rank().over(w)) \\
   .withColumn("dense_rank", f.dense_rank().over(w)).show()""",
        "postgres": """SELECT *,
    ROW_NUMBER()  OVER w AS rn,
    RANK()        OVER w AS rank,
    DENSE_RANK()  OVER w AS dense_rank
FROM df
WINDOW w AS (PARTITION BY region ORDER BY amount);""",
    },
    "window_first_last": {
        "input_cols": ["region", "month", "amount"],
        "input_rows": [
            ("APAC", "2026-01", "120.0"),
            ("APAC", "2026-03", "80.0"),
            ("EMEA", "2026-01", "90.0"),
        ],
        "output_cols": ["region", "month", "amount", "first_amt", "last_amt"],
        "output_rows": [
            ("APAC", "2026-01", 120.0, 120.0, 80.0),
            ("APAC", "2026-03", 80.0, 120.0, 80.0),
            ("EMEA", "2026-01", 90.0, 90.0, 90.0),
        ],
        "pyspark": """from pyspark.sql import Window
import pyspark.sql.functions as f

w = Window.partitionBy("region").orderBy("month").rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)

df.withColumn("first_amt", f.first("amount").over(w)) \\
   .withColumn("last_amt",  f.last("amount").over(w)).show()""",
        "postgres": """SELECT *,
    FIRST_VALUE(amount) OVER w AS first_amt,
    LAST_VALUE(amount)  OVER w AS last_amt
FROM df
WINDOW w AS (PARTITION BY region ORDER BY month
             ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING);""",
    },
    "window_ntile": {
        "input_cols": ["region", "amount"],
        "input_rows": [
            ("APAC", "10.0"),
            ("APAC", "20.0"),
            ("APAC", "30.0"),
            ("APAC", "40.0"),
        ],
        "output_cols": ["region", "amount", "quartile"],
        "output_rows": [
            ("APAC", 10.0, 1),
            ("APAC", 20.0, 2),
            ("APAC", 30.0, 3),
            ("APAC", 40.0, 4),
        ],
        "pyspark": """from pyspark.sql import Window
import pyspark.sql.functions as f

w = Window.partitionBy("region").orderBy("amount")
df.withColumn("quartile", f.ntile(4).over(w)).show()""",
        "postgres": """SELECT *,
    NTILE(4) OVER (PARTITION BY region ORDER BY amount) AS quartile
FROM df;""",
    },
    "window_cume_dist": {
        "input_cols": ["region", "amount"],
        "input_rows": [
            ("APAC", "10.0"),
            ("APAC", "20.0"),
            ("APAC", "30.0"),
            ("APAC", "40.0"),
        ],
        "output_cols": ["region", "amount", "pct_rank", "cume_dist"],
        "output_rows": [
            ("APAC", 10.0, 0.0, 0.25),
            ("APAC", 20.0, 0.3333, 0.5),
            ("APAC", 30.0, 0.6667, 0.75),
            ("APAC", 40.0, 1.0, 1.0),
        ],
        "pyspark": """from pyspark.sql import Window
import pyspark.sql.functions as f

w = Window.partitionBy("region").orderBy("amount")
df.withColumn("pct_rank",  f.percent_rank().over(w)) \\
   .withColumn("cume_dist", f.cume_dist().over(w)).show()""",
        "postgres": """SELECT *,
    PERCENT_RANK() OVER (PARTITION BY region ORDER BY amount) AS pct_rank,
    CUME_DIST()    OVER (PARTITION BY region ORDER BY amount) AS cume_dist
FROM df;""",
    },
    "window_collect": {
        "input_cols": ["region", "product"],
        "input_rows": [
            ("APAC", "P1"),
            ("APAC", "P2"),
            ("EMEA", "P3"),
        ],
        "output_cols": ["region", "products_list", "products_set"],
        "output_rows": [
            ("APAC", ["P1", "P2"], ["P1", "P2"]),
            ("EMEA", ["P3"], ["P3"]),
        ],
        "pyspark": """from pyspark.sql import Window
import pyspark.sql.functions as f

w = Window.partitionBy("region")
df.withColumn("products_list", f.collect_list("product").over(w)) \\
   .withColumn("products_set",  f.collect_set("product").over(w)).show(truncate=False)""",
        "postgres": """SELECT region,
    ARRAY_AGG(product ORDER BY product)               AS products_list,
    ARRAY_AGG(DISTINCT product ORDER BY product)      AS products_set
FROM df
GROUP BY region;""",
    },
    # ── SECTION 22: LEAD / LAG ──
    "lag_basic": {
        "input_cols": ["event_date", "amount"],
        "input_rows": [
            ("2026-01-01", "100.0"),
            ("2026-01-02", "120.0"),
            ("2026-01-03", "90.0"),
        ],
        "output_cols": ["event_date", "amount", "prev_amount", "change"],
        "output_rows": [
            ("2026-01-01", 100.0, None, None),
            ("2026-01-02", 120.0, 100.0, 20.0),
            ("2026-01-03", 90.0, 120.0, -30.0),
        ],
        "pyspark": """from pyspark.sql import Window
from pyspark.sql.functions import lag, col

w = Window.orderBy("event_date")

df.withColumn("prev_amount", lag("amount", 1).over(w)) \\
   .withColumn("change", col("amount") - col("prev_amount")).show()""",
        "postgres": """SELECT *,
    LAG(amount, 1) OVER (ORDER BY event_date) AS prev_amount,
    amount - LAG(amount, 1) OVER (ORDER BY event_date) AS change
FROM df;""",
    },
    "lead_basic": {
        "input_cols": ["event_date", "amount"],
        "input_rows": [
            ("2026-01-01", "100.0"),
            ("2026-01-02", "120.0"),
            ("2026-01-03", "90.0"),
        ],
        "output_cols": ["event_date", "amount", "next_amount"],
        "output_rows": [
            ("2026-01-01", 100.0, 120.0),
            ("2026-01-02", 120.0, 90.0),
            ("2026-01-03", 90.0, None),
        ],
        "pyspark": """from pyspark.sql import Window
from pyspark.sql.functions import lead

w = Window.orderBy("event_date")
df.withColumn("next_amount", lead("amount", 1).over(w)).show()""",
        "postgres": """SELECT *,
    LEAD(amount, 1) OVER (ORDER BY event_date) AS next_amount
FROM df;""",
    },
    "lead_lag_defaults": {
        "input_cols": ["region", "amount"],
        "input_rows": [
            ("APAC", "100.0"),
            ("APAC", "120.0"),
            ("APAC", "80.0"),
        ],
        "output_cols": ["region", "amount", "prev", "next", "defaulted"],
        "output_rows": [
            ("APAC", 100.0, None, 120.0, 0.0),
            ("APAC", 120.0, 100.0, 80.0, 120.0),
            ("APAC", 80.0, 120.0, None, 80.0),
        ],
        "pyspark": """from pyspark.sql import Window
from pyspark.sql.functions import lag, lead

w = Window.partitionBy("region").orderBy("amount")
df.withColumn("prev",      lag("amount", 1).over(w)) \\
   .withColumn("next",      lead("amount", 1).over(w)) \\
   .withColumn("defaulted", lag("amount", 1, 0.0).over(w)).show()""",
        "postgres": """SELECT *,
    LAG(amount, 1)    OVER (PARTITION BY region ORDER BY amount) AS prev,
    LEAD(amount, 1)  OVER (PARTITION BY region ORDER BY amount) AS next,
    COALESCE(LAG(amount, 1) OVER (PARTITION BY region ORDER BY amount), 0.0) AS defaulted
FROM df;""",
    },
    "lead_lag_period_change": {
        "input_cols": ["month", "revenue"],
        "input_rows": [
            ("2026-01", "1000.0"),
            ("2026-02", "1200.0"),
            ("2026-03", "1100.0"),
        ],
        "output_cols": ["month", "revenue", "prev_rev", "pct_change"],
        "output_rows": [
            ("2026-01", 1000.0, None, None),
            ("2026-02", 1200.0, 1000.0, 0.2),
            ("2026-03", 1100.0, 1200.0, -0.0833),
        ],
        "pyspark": """from pyspark.sql import Window
from pyspark.sql.functions import lag, col

w = Window.orderBy("month")
df.withColumn("prev_rev", lag("revenue", 1).over(w)) \\
   .withColumn("pct_change",
       (col("revenue") - col("prev_rev")) / col("prev_rev")).show()""",
        "postgres": """SELECT *,
    LAG(revenue, 1) OVER (ORDER BY month) AS prev_rev,
    (revenue - LAG(revenue, 1) OVER (ORDER BY month)) /
     NULLIF(LAG(revenue, 1) OVER (ORDER BY month), 0) AS pct_change
FROM df;""",
    },
    "lead_lag_streak": {
        "input_cols": ["dt", "status"],
        "input_rows": [
            ("2026-01-01", "up"),
            ("2026-01-02", "up"),
            ("2026-01-03", "down"),
            ("2026-01-04", "up"),
            ("2026-01-05", "up"),
            ("2026-01-06", "up"),
        ],
        "output_cols": ["dt", "status", "streak"],
        "output_rows": [
            ("2026-01-01", "up", 1),
            ("2026-01-02", "up", 2),
            ("2026-01-03", "down", 1),
            ("2026-01-04", "up", 1),
            ("2026-01-05", "up", 2),
            ("2026-01-06", "up", 3),
        ],
        "pyspark": """from pyspark.sql import Window
from pyspark.sql.functions import lag, when, col, sum as Fsum

w = Window.orderBy("dt")
df = df.withColumn("prev_status", lag("status", 1).over(w))
df = df.withColumn("new_group",    when(col("status") != col("prev_status"), 1).otherwise(0))
df = df.withColumn("group_id",     Fsum("new_group").over(Window.orderBy("dt")))
df = df.withColumn("streak",
    Fsum("new_group").over(Window.partitionBy("group_id").orderBy("dt")))

df.select("dt", "status", "streak").show()""",
        "postgres": """WITH grp AS (
    SELECT *,
        SUM(CASE WHEN status != LAG(status) OVER (ORDER BY dt) THEN 1 ELSE 0 END)
            OVER (ORDER BY dt) AS grp_id
    FROM df
)
SELECT dt, status,
    ROW_NUMBER() OVER (PARTITION BY grp_id ORDER BY dt) AS streak
FROM grp;""",
    },
    # ── SECTION 23: ROWS BETWEEN ──
    "rows_unbounded": {
        "input_cols": ["event_time", "amount"],
        "input_rows": [
            ("2026-01-01", "100.0"),
            ("2026-01-02", "120.0"),
            ("2026-01-03", "80.0"),
        ],
        "output_cols": ["event_time", "amount", "running_total", "running_avg"],
        "output_rows": [
            ("2026-01-01", 100.0, 100.0, 100.0),
            ("2026-01-02", 120.0, 220.0, 110.0),
            ("2026-01-03", 80.0, 300.0, 100.0),
        ],
        "pyspark": """from pyspark.sql import Window
import pyspark.sql.functions as f

w = Window.orderBy("event_time").rowsBetween(Window.unboundedPreceding, Window.currentRow)
df.withColumn("running_total", f.sum("amount").over(w)) \\
   .withColumn("running_avg",  f.avg("amount").over(w)).show()""",
        "postgres": """SELECT *,
    SUM(amount) OVER (ORDER BY event_time
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
    AVG(amount) OVER (ORDER BY event_time
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_avg
FROM df;""",
    },
    "rows_fixed": {
        "input_cols": ["event_time", "amount"],
        "input_rows": [
            ("2026-01-01", "100.0"),
            ("2026-01-02", "120.0"),
            ("2026-01-03", "80.0"),
            ("2026-01-04", "90.0"),
        ],
        "output_cols": ["event_time", "amount", "sum_2prev", "avg_1next"],
        "output_rows": [
            ("2026-01-01", 100.0, 100.0, 110.0),
            ("2026-01-02", 120.0, 220.0, 100.0),
            ("2026-01-03", 80.0, 180.0, 90.0),
            ("2026-01-04", 90.0, 170.0, 90.0),
        ],
        "pyspark": """from pyspark.sql import Window
import pyspark.sql.functions as f

w_sum  = Window.orderBy("event_time").rowsBetween(-2, 0)
w_avg  = Window.orderBy("event_time").rowsBetween(0, 1)
df.withColumn("sum_2prev", f.sum("amount").over(w_sum)) \\
   .withColumn("avg_1next", f.avg("amount").over(w_avg)).show()""",
        "postgres": """SELECT *,
    SUM(amount) OVER (ORDER BY event_time
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS sum_2prev,
    AVG(amount) OVER (ORDER BY event_time
        ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING) AS avg_1next
FROM df;""",
    },
    "rows_range_vs_rows": {
        "input_cols": ["event_time", "amount"],
        "input_rows": [
            ("2026-01-01 00:00", "100.0"),
            ("2026-01-01 00:30", "120.0"),
            ("2026-01-01 01:00", "80.0"),
        ],
        "output_cols": ["event_time", "amount", "sum_rows", "sum_range"],
        "output_rows": [
            ("2026-01-01 00:00", 100.0, 220.0, 220.0),
            ("2026-01-01 00:30", 120.0, 200.0, 200.0),
            ("2026-01-01 01:00", 80.0, 80.0, 80.0),
        ],
        "pyspark": """from pyspark.sql import Window
import pyspark.sql.functions as f

# ROWS BETWEEN: physical row offset
w_rows  = Window.orderBy("event_time").rowsBetween(-1, 0)

# RANGE BETWEEN: logical value range (same order-by value counts together)
w_range  = Window.orderBy("event_time").rangeBetween(-3600, 0)  # 1 hour in seconds

df.withColumn("sum_rows",  f.sum("amount").over(w_rows)) \\
   .withColumn("sum_range", f.sum("amount").over(w_range)).show()""",
        "postgres": """-- PostgreSQL only supports ROWS mode (not RANGE)
SELECT *,
    SUM(amount) OVER (ORDER BY event_time
        ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS sum_rows
FROM df;""",
    },
    "rows_current": {
        "input_cols": ["event_time", "amount"],
        "input_rows": [
            ("2026-01-01", "100.0"),
            ("2026-01-02", "120.0"),
            ("2026-01-02", "90.0"),
        ],
        "output_cols": ["event_time", "amount", "current_row"],
        "output_rows": [
            ("2026-01-01", 100.0, 100.0),
            ("2026-01-02", 120.0, 210.0),
            ("2026-01-02", 90.0, 210.0),
        ],
        "pyspark": """from pyspark.sql import Window
import pyspark.sql.functions as f

w = Window.partitionBy("event_time").orderBy("amount").rowsBetween(0, 0)
df.withColumn("current_row", f.sum("amount").over(w)).show()""",
        "postgres": """SELECT *,
    SUM(amount) OVER (PARTITION BY event_time ORDER BY amount
        ROWS BETWEEN CURRENT ROW AND CURRENT ROW) AS current_row
FROM df;""",
    },
}

# ─── HELPERS ──────────────────────────────────────────────────────────────────


def rows_to_html(rows):
    trs = ""
    for r in rows:
        trs += "<tr>" + "".join(f"<td>{v}</td>" for v in r) + "</tr>"
    return trs


def td(v):
    return f"<td>{v}</td>"


# ─── PROCESS EMPTY TBODY ──────────────────────────────────────────────────────

total_filled = 0

# Pattern: <tbody></tbody> after known column headers
# We find each occurrence and fill based on surrounding context

import re

# Find all empty tbody sections
empty_pattern = re.compile(r"(<thead><tr>(.*?)</tr></thead><tbody></tbody>)", re.DOTALL)

# For sections 18-23, we need to match based on the PREVIOUS h3
# Let's process by finding h3 headings and their following tables

# Strategy: find all section/concept blocks, then for each h3, find the following
# table panels and fill them

# First pass: identify all h3 headings and what follows them
h3_pattern = re.compile(r'<h3>(.*?)</h3>\s*<div class="two-col">', re.DOTALL)
table_panel_pattern = re.compile(
    r'(<div class="panel">\s*<h3>Input Table</h3>\s*'
    r'<div class="table-wrap"><table><thead><tr>(.*?)</tr></thead><tbody></tbody></table></div>)',
    re.DOTALL,
)
output_panel_pattern = re.compile(
    r'(<div class="panel">\s*<h3>Output Table</h3>\s*'
    r'<div class="table-wrap"><table><thead><tr>(.*?)</tr></thead><tbody></tbody></table></div>)',
    re.DOTALL,
)

# Actually, let's be more surgical. I'll replace all <tbody></tbody> that are in
# table-wrap contexts where we have column headers defined.

# The challenge: we need to know the column names to generate rows.
# Let's parse the HTML and find each empty table, extract its columns, and fill.


def parse_columns(th_html):
    """Extract column names from <th> tags"""
    cols = re.findall(r"<th>(.*?)</th>", th_html)
    return [c.strip() for c in cols]


def guess_dtype(cols, h3_text):
    """Guess data type based on column name"""
    dtypes = {}
    for c in cols:
        cl = c.lower()
        if any(k in cl for k in ["id", "order"]):
            dtypes[c] = "int"
        elif any(k in cl for k in ["amount", "price", "total", "rate", "pct", "score"]):
            dtypes[c] = "float"
        elif any(k in cl for k in ["date", "ts", "time", "month"]):
            dtypes[c] = "date"
        elif any(k in cl for k in ["count", "num", "year", "day", "hour", "qty"]):
            dtypes[c] = "int"
        elif any(k in cl for k in ["bool", "flag", "active"]):
            dtypes[c] = "bool"
        else:
            dtypes[c] = "str"
    return dtypes


def generate_rows(cols, dtypes, count=3):
    """Generate sample rows based on column types"""
    rows = []
    for i in range(count):
        row = []
        for c in cols:
            dt = dtypes.get(c, "str")
            if dt == "int":
                row.append(str(100 + i * 10))
            elif dt == "float":
                row.append(f"{90 + i * 30}.0")
            elif dt == "date":
                row.append(f"2026-0{i + 1}-15")
            elif dt == "bool":
                row.append("true" if i % 2 == 0 else "false")
            else:
                row.append(f"val{i + 1}")
        rows.append(tuple(row))
    return rows


# Find and replace empty tbody patterns
# Pattern for: <tbody></tbody> (empty tbody)
# We need the full table context: <thead>...<tbody></tbody>


def replace_empty_table(m):
    full = m.group(0)
    # Extract the table
    thead_match = re.search(r"<thead><tr>(.*?)</tr></thead>", full)
    if not thead_match:
        return full
    th_html = thead_match.group(1)
    cols = parse_columns(th_html)
    if not cols:
        return full
    dtypes = guess_dtype(cols, "")
    rows = generate_rows(cols, dtypes, 3)
    trs = rows_to_html(rows)
    return full.replace("<tbody></tbody>", f"<tbody>{trs}</tbody>")


# Apply to entire file
new_content = content
new_content = re.sub(
    r"<thead><tr>.*?</tr></thead><tbody></tbody>",
    replace_empty_table,
    new_content,
    flags=re.DOTALL,
)

# Count how many we filled
empty_after = new_content.count("<tbody></tbody>")
print(f"Empty tbody after fill: {empty_after}")

# ─── ADD POSTGRESQL PANELS TO SECTIONS 1-12 ──────────────────────────────────

# Sections 1-12 have single pre.code blocks (no two-col). We need to find
# each sub-section's code block and either:
# 1. If it follows a two-col table panel, convert to two-col with PySpark + PostgreSQL
# 2. Or add PostgreSQL panel below

# Let's find the pattern: h3 + two-col (optional) + pre.code
# and add PostgreSQL panel

# The structure in sections 1-12 is:
#   <h3>Sub-heading</h3>
#   <div class="two-col">  (tables)
#   </div>
#   <pre class="code"> (PySpark only)

# We need to convert to:
#   <h3>Sub-heading</h3>
#   <div class="two-col">  (tables)
#   </div>
#   <div class="two-col">
#     <div class="panel">
#       <h3>PySpark</h3>
#       <pre class="code"> (PySpark)
#     </div>
#     <div class="panel">
#       <h3>PostgreSQL</h3>
#       <pre class="code"> (PostgreSQL)
#     </div>
#   </div>

# Key: for sections 1-12, the pre.code right after two-col tables needs a PostgreSQL twin.

# Find all the data keys that have postgres defined
has_pg = {k: v for k, v in DATA.items() if "postgres" in v}


def build_two_col_pyspark_postgres(pyspark_code, postgres_code):
    pg_escaped = (
        postgres_code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )
    py_escaped = (
        pyspark_code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )
    return (
        '<div class="two-col">'
        '<div class="panel"><h3>PySpark</h3>'
        f'<pre class="code"><code>{py_escaped}</code></pre></div>'
        '<div class="panel"><h3>PostgreSQL</h3>'
        f'<pre class="code"><code>{pg_escaped}</code></pre></div>'
        "</div>"
    )


# For sections 1-12, we need to find specific code blocks and wrap them.
# Strategy: Look for the heading text and then the following <pre class="code">
# Replace each with two-col.

# The DATA keys map to h3 heading text. Let's build a mapping from heading to data.
HEADING_TO_KEY = {}

# For sections 4-12 (CSV, JSON, etc.), we have specific h3 headings.
# Let's map them explicitly.

SPECIFIC_REPLACEMENTS = {
    # Section 4: CSV
    "CSV Reading with header, inferSchema, and delimiter": {
        "input_cols": ["id", "region", "amount"],
        "input_rows": [("1", "APAC", "120"), ("2", "EMEA", "90"), ("3", "APAC", "220")],
        "output_cols": ["id", "region", "amount"],
        "output_rows": [(1, "APAC", 120), (2, "EMEA", 90), (3, "APAC", 220)],
        "pyspark": """sales_csv = (spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("/data/sales.csv"))

sales_csv.printSchema()
sales_csv.show()""",
        "postgres": """CREATE TABLE sales (id INTEGER, region TEXT, amount NUMERIC);
COPY sales FROM '/data/sales.csv' WITH (FORMAT csv, HEADER true);
SELECT * FROM sales;""",
    },
    "CSV Writing — save to path": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", "EMEA", "90.0"),
            ("3", "APAC", "220.0"),
        ],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [(1, "APAC", 120.0), (2, "EMEA", 90.0), (3, "APAC", 220.0)],
        "pyspark": """df.write.mode("overwrite").option("header", True).csv("/tmp/sales_out")""",
        "postgres": """COPY (SELECT order_id, region, amount FROM sales)
TO '/tmp/sales_out.csv' WITH (FORMAT csv, HEADER true);""",
    },
    # Section 5: JSON
    "JSON Reading — multiLine and primitives": {
        "input_cols": ["event", "value"],
        "input_rows": [
            ('{"event":"click","value":1}',),
            ('{"event":"purchase","value":50}',),
        ],
        "output_cols": ["event", "value"],
        "output_rows": [("click", 1), ("purchase", 50)],
        "pyspark": """events = (spark.read
    .option("multiLine", False)
    .json("/data/events.json"))

events.printSchema()
events.show(truncate=False)""",
        "postgres": """SELECT e.*
FROM events,
     jsonb_array_elements(raw::jsonb) WITH ORDINALITY AS arr(e)
CROSS JOIN LATERAL jsonb_to_record(e) AS e(event TEXT, value INT);""",
    },
    "JSON Writing — output as JSON lines": {
        "input_cols": ["id", "region", "amount"],
        "input_rows": [("1", "APAC", "120.0"), ("2", "EMEA", "90.0")],
        "output_cols": ["id", "region", "amount"],
        "output_rows": [(1, "APAC", 120.0), (2, "EMEA", 90.0)],
        "pyspark": """df = spark.createDataFrame([
    (1, "APAC", 120.0),
    (2, "EMEA", 90.0),
], ["id", "region", "amount"])

df.write.mode("overwrite").json("/tmp/out_json")""",
        "postgres": """SELECT json_build_object(
    'id', id, 'region', region, 'amount', amount
) AS json_row FROM sales;""",
    },
    # Section 6: Parquet
    "Parquet Reading — read from path": {
        "input_cols": ["order_id", "customer_id", "event_date", "amount"],
        "input_rows": [
            ("101", "C1", "2026-03-01", "180.0"),
            ("102", "C2", "2026-03-01", "90.0"),
        ],
        "output_cols": ["order_id", "customer_id", "event_date", "amount"],
        "output_rows": [
            (101, "C1", "2026-03-01", 180.0),
            (102, "C2", "2026-03-01", 90.0),
        ],
        "pyspark": """orders_parquet = spark.read.parquet("/lake/raw/orders_parquet")
orders_parquet.printSchema()
orders_parquet.show()""",
        "postgres": """-- PostgreSQL 16+ supports Parquet natively
SELECT * FROM read_parquet('/lake/raw/orders_parquet/*.parquet');""",
    },
    "Parquet Writing — save curated dataset": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [("1", "APAC", "120.0"), ("2", "EMEA", "90.0")],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [(1, "APAC", 120.0), (2, "EMEA", 90.0)],
        "pyspark": """df.write.mode("overwrite").parquet("/lake/curated/orders")""",
        "postgres": """-- PostgreSQL 16+: COPY to Parquet
COPY sales TO '/lake/curated/orders/'
    WITH (FORMAT parquet, COMPRESSION 'snappy');""",
    },
    # Section 7: Avro
    "Avro Reading — read with schema": {
        "input_cols": ["event_id", "user_id", "ts", "action"],
        "input_rows": [
            ("e1", "u1", "1709280000", "click"),
            ("e2", "u2", "1709280060", "view"),
        ],
        "output_cols": ["event_id", "user_id", "ts", "action"],
        "output_rows": [
            ("e1", "u1", 1709280000, "click"),
            ("e2", "u2", 1709280060, "view"),
        ],
        "pyspark": """events_avro = (spark.read
    .format("avro")
    .load("/lake/raw/events_avro"))

events_avro.printSchema()
events_avro.show()""",
        "postgres": """-- Use avro_fdw or Python avro library
SELECT * FROM read_avro('/lake/raw/events_avro/*.avro');""",
    },
    "Avro Writing — serialize DataFrame to Avro": {
        "input_cols": ["event_id", "user_id", "action"],
        "input_rows": [("e1", "u1", "click"), ("e2", "u2", "view")],
        "output_cols": ["event_id", "user_id", "action"],
        "output_rows": [("e1", "u1", "click"), ("e2", "u2", "view")],
        "pyspark": """df = spark.createDataFrame([
    ("e1", "u1", "click"),
    ("e2", "u2", "view"),
], ["event_id", "user_id", "action"])

df.write.mode("overwrite").format("avro").save("/lake/curated/events")""",
        "postgres": """-- PostgreSQL: serialize via Python (avro library)
-- Convert rows to Avro binary and write to file""",
    },
    # Section 8: Cloud
    "AWS S3 — Read/Write with hadoop-aws": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [("1", "APAC", "120.0"), ("2", "EMEA", "90.0")],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [(1, "APAC", 120.0), (2, "EMEA", 90.0)],
        "pyspark": """aws_path = "s3a://de-bucket/sales/orders"
df = spark.read.parquet(aws_path)
df.write.mode("overwrite").parquet("s3a://de-bucket/curated/orders")""",
        "postgres": """SELECT aws_s3.table_import_from_s3(
    'sales', 'order_id,region,amount', '(format csv, header)',
    'de-bucket', 'sales/orders/', 'us-east-1'
);""",
    },
    "Azure Data Lake — Read/Write with ABFS": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [("1", "APAC", "120.0"), ("2", "EMEA", "90.0")],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [(1, "APAC", 120.0), (2, "EMEA", 90.0)],
        "pyspark": """df = spark.read.parquet(
    "abfss://data@myaccount.dfs.core.windows.net/orders/")
df.write.mode("overwrite").parquet(
    "abfss://data@myaccount.dfs.core.windows.net/curated/orders")""",
        "postgres": """COPY sales FROM
    'https://storage.blob.core.windows.net/container/orders/*.csv'
WITH (FORMAT parquet);""",
    },
    "GCP Cloud Storage — Read/Write with GCS connector": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [("1", "APAC", "120.0"), ("2", "EMEA", "90.0")],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [(1, "APAC", 120.0), (2, "EMEA", 90.0)],
        "pyspark": """df = spark.read.parquet("gs://my-bucket/orders/")
df.write.mode("overwrite").parquet("gs://my-bucket/curated/orders")""",
        "postgres": """\\! gsutil cp gs://my-bucket/orders/*.parquet /tmp/
COPY sales FROM '/tmp/orders.parquet' WITH (FORMAT parquet);""",
    },
    # Section 9: Cloud libs
    "Delta Lake — Time Travel and Streaming": {
        "input_cols": ["id", "region", "amount"],
        "input_rows": [
            ("1", "APAC", "120.0"),
            ("2", "EMEA", "90.0"),
            ("1", "APAC", "150.0"),
        ],
        "output_cols": ["id", "region", "amount", "version"],
        "output_rows": [
            (1, "APAC", 120.0, 0),
            (2, "EMEA", 90.0, 0),
            (1, "APAC", 150.0, 1),
        ],
        "pyspark": """from delta.tables import DeltaTable

# Read specific version (time travel)
df_v0 = spark.read.format("delta") \\
    .option("versionAsOf", 0) \\
    .load("/delta/orders")

# Merge / upsert
dt = DeltaTable.forPath(spark, "/delta/orders")
dt.merge(updates_df, "target.id = source.id") \\
    .whenMatchedUpdateAll() \\
    .whenNotMatchedInsertAll() \\
    .execute()""",
        "postgres": """-- PostgreSQL: version tracking via trigger or native temporal
CREATE TABLE orders (id SERIAL, region TEXT, amount NUMERIC, version INT DEFAULT 0);
SELECT * FROM orders WHERE version = 0;  -- time-travel equivalent""",
    },
    "Apache Hudi — Upsert and Incremental": {
        "input_cols": ["id", "region", "amount", "ts"],
        "input_rows": [
            ("1", "APAC", "120.0", "1709280000"),
            ("2", "EMEA", "90.0", "1709280000"),
        ],
        "output_cols": ["id", "region", "amount", "hoodie_commit"],
        "output_rows": [
            (1, "APAC", 120.0, "20240101120000"),
            (2, "EMEA", 90.0, "20240101120000"),
        ],
        "pyspark": """df.write.format("hudi") \\
    .option("hoodie.table.name", "orders") \\
    .option("hoodie.datasource.write.recordkey", "id") \\
    .option("hoodie.datasource.write.precombine.field", "ts") \\
    .mode("append") \\
    .save("hoodie/path/")""",
        "postgres": """INSERT INTO orders (id, region, amount, ts)
VALUES (1, 'APAC', 120.0, '2024-03-01')
ON CONFLICT (id) DO UPDATE SET
    amount = EXCLUDED.amount;""",
    },
    "Apache Iceberg — Tables and Time Travel": {
        "input_cols": ["id", "region", "amount"],
        "input_rows": [("1", "APAC", "120.0"), ("2", "EMEA", "90.0")],
        "output_cols": ["id", "region", "amount", "snapshot_id"],
        "output_rows": [(1, "APAC", 120.0, 1234567890), (2, "EMEA", 90.0, 1234567890)],
        "pyspark": """df = spark.read.format("iceberg").load("s3://warehouse/db/orders")

# Time-travel by snapshot
df_old = spark.read.format("iceberg") \\
    .option("snapshot-id", 1234567890) \\
    .load("s3://warehouse/db/orders")""",
        "postgres": """-- PostgreSQL (Enterprise): native time-travel
SELECT * FROM orders AS OF SYSTEM TIME '-1s';""",
    },
    # Section 10: Excel
    "Excel Reading — read Excel with spark-excel": {
        "input_cols": ["id", "region", "amount"],
        "input_rows": [("1", "APAC", "120.0"), ("2", "EMEA", "90.0")],
        "output_cols": ["id", "region", "amount"],
        "output_rows": [(1, "APAC", 120.0), (2, "EMEA", 90.0)],
        "pyspark": """excel_df = (spark.read
    .format("com.crealytics.spark.excel")
    .option("sheetName", "Sales")
    .option("useHeader", True)
    .load("/data/sales.xlsx"))

excel_df.show()""",
        "postgres": """-- PostgreSQL: use odbc_fdw or pg_excel
CREATE EXTENSION odbc_fdw;
SELECT * FROM foreign_excel_sheet;""",
    },
    "Excel Writing — write to .xlsx": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [("1", "APAC", "120.0"), ("2", "EMEA", "90.0")],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [(1, "APAC", 120.0), (2, "EMEA", 90.0)],
        "pyspark": """df.write.format("com.crealytics.spark.excel") \\
    .option("sheetName", "Report") \\
    .option("useHeader", True) \\
    .mode("overwrite") \\
    .save("/tmp/report.xlsx")""",
        "postgres": """COPY (SELECT * FROM sales) TO '/tmp/report.csv' WITH (FORMAT csv);
-- Convert CSV → XLSX using Python (openpyxl)""",
    },
    "Gzip / Snappy — compressed I/O": {
        "input_cols": ["id", "region", "amount"],
        "input_rows": [("1", "APAC", "120.0"), ("2", "EMEA", "90.0")],
        "output_cols": ["id", "region", "amount"],
        "output_rows": [(1, "APAC", 120.0), (2, "EMEA", 90.0)],
        "pyspark": """# Read with compression
df = spark.read.option("compression", "gzip") \\
    .csv("/data/sales.csv.gz", header=True, inferSchema=True)

# Write with Snappy (default for Parquet)
df.write.option("compression", "snappy") \\
    .mode("overwrite").parquet("/out/sales.parquet")""",
        "postgres": """-- Read gzip-compressed CSV
\\copy sales FROM 'gzip -d -c /data/sales.csv.gz' WITH (FORMAT csv, HEADER true)

-- Write with compression
COPY sales TO PROGRAM 'gzip > /tmp/sales.csv.gz' WITH (FORMAT csv);""",
    },
    # Section 11: Ref columns
    "Referencing columns — string vs Column object": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [("1", "APAC", "120.0"), ("2", "EMEA", "90.0")],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [(1, "APAC", 120.0), (2, "EMEA", 90.0)],
        "pyspark": """from pyspark.sql.functions import col

# String reference
df.select("order_id", "region", "amount")

# Column object (composable, type-safe)
df.select(col("order_id"), col("region"), col("amount"))

# expr for SQL expressions
df.select(expr("order_id + 100 AS new_id"))""",
        "postgres": """-- String column: just use the name
SELECT order_id, region, amount FROM df;

-- Column expression
SELECT order_id + 100 AS new_id, region, amount FROM df;""",
    },
    "Column expressions — arithmetic, cast, alias": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [("1", "APAC", "120.0"), ("2", "EMEA", "90.0")],
        "output_cols": ["order_id", "region", "amount", "scaled"],
        "output_rows": [(1, "APAC", 120.0, 132.0), (2, "EMEA", 90.0, 99.0)],
        "pyspark": """from pyspark.sql.functions import col, expr

df.select(
    "order_id", "region", "amount",
    (col("amount") * 1.1).cast("int").alias("scaled")
).show()""",
        "postgres": """SELECT order_id, region, amount,
    (amount * 1.1)::INT AS scaled
FROM df;""",
    },
    # Section 12: Select columns
    "Selecting specific columns — select()": {
        "input_cols": ["order_id", "region", "amount", "raw_col"],
        "input_rows": [("1", "APAC", "120.0", "x"), ("2", "EMEA", "90.0", "y")],
        "output_cols": ["order_id", "region", "amount"],
        "output_rows": [(1, "APAC", 120.0), (2, "EMEA", 90.0)],
        "pyspark": """projection = df.select("order_id", "region", "amount")
projection.show()""",
        "postgres": """SELECT order_id, region, amount FROM df;""",
    },
    "Adding computed columns — select + alias": {
        "input_cols": ["order_id", "region", "amount"],
        "input_rows": [("1", "APAC", "120.0"), ("2", "EMEA", "90.0")],
        "output_cols": ["order_id", "region", "amount_usd", "amount_eur"],
        "output_rows": [(1, "APAC", 120.0, 108.0), (2, "EMEA", 90.0, 81.0)],
        "pyspark": """from pyspark.sql.functions import col

result = df.select(
    "order_id", "region",
    col("amount").alias("amount_usd"),
    (col("amount") * 0.9).alias("amount_eur")
)
result.show()""",
        "postgres": """SELECT order_id, region,
    amount AS amount_usd,
    amount * 0.9 AS amount_eur
FROM df;""",
    },
}


def escape_html(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_table(cols, rows):
    trs = "".join("<tr>" + "".join(f"<td>{v}</td>" for v in r) + "</tr>" for r in rows)
    ths = "".join(f"<th>{c}</th>" for c in cols)
    return (
        '<div class="panel">'
        "<h3>Input Table</h3>"
        f'<div class="table-wrap"><table><thead><tr>{ths}</tr></thead>'
        f"<tbody>{trs}</tbody></table></div></div>"
    )


def build_table_out(cols, rows):
    trs = "".join("<tr>" + "".join(f"<td>{v}</td>" for v in r) + "</tr>" for r in rows)
    ths = "".join(f"<th>{c}</th>" for c in cols)
    return (
        '<div class="panel">'
        "<h3>Output Table</h3>"
        f'<div class="table-wrap"><table><thead><tr>{ths}</tr></thead>'
        f"<tbody>{trs}</tbody></table></div></div>"
    )


def build_code_block(code, label):
    return (
        '<div class="panel">'
        f"<h3>{label}</h3>"
        f'<pre class="code"><code>{escape_html(code)}</code></pre>'
        "</div>"
    )


# Now replace each sub-section in sections 1-12
# We look for the h3 heading text and replace the following content

replaced = 0
for heading, data in SPECIFIC_REPLACEMENTS.items():
    # Build the replacement content
    two_col_tables = (
        '<div class="two-col">'
        + build_table(data["input_cols"], data["input_rows"])
        + build_table_out(data["output_cols"], data["output_rows"])
        + "</div>"
    )
    two_col_code = (
        '<div class="two-col">'
        + build_code_block(data["pyspark"], "PySpark")
        + build_code_block(data["postgres"], "PostgreSQL")
        + "</div>"
    )
    new_section = two_col_tables + "\n" + two_col_code

    # Find the h3 heading and replace everything from it until the next h3 or section end
    pattern = re.compile(r"(<h3>" + re.escape(heading) + r"</h3>)", re.DOTALL)
    match = pattern.search(new_content)
    if match:
        start = match.start()
        # Find the end: next h3 at the same level, or </section>
        # Look for next <h3> that is not nested inside another div
        rest = new_content[start + len(match.group(0)) :]
        # Find next <h3>
        next_h3 = re.search(r"\n      <h3>", rest)
        next_section = re.search(r"\n    </section>", rest)
        if next_h3 and next_section:
            if next_h3.start() < next_section.start():
                end = start + len(match.group(0)) + next_h3.start()
            else:
                end = start + len(match.group(0)) + next_section.start()
        elif next_h3:
            end = start + len(match.group(0)) + next_h3.start()
        elif next_section:
            end = start + len(match.group(0)) + next_section.start()
        else:
            end = len(new_content)

        old_section = new_content[start:end]
        new_content = new_content[:start] + new_section + new_content[end:]
        replaced += 1
        print(f"  Replaced: {heading[:60]}")
    else:
        print(f"  NOT FOUND: {heading[:60]}")

print(f"\nTotal sub-sections replaced: {replaced}")

# ─── FILL EMPTY TBODY IN SECTIONS 1-12 ───────────────────────────────────────
# Some sections in 1-12 may still have empty tbodys for code panels with no specific data


def fill_empty_tbody_in_tables(html):
    """Find tables with empty tbody and fill with generated rows"""

    def gen_rows_for_cols(th_content):
        cols = parse_columns(th_content)
        if not cols:
            return None
        dtypes = guess_dtype(cols, "")
        return rows_to_html(generate_rows(cols, dtypes, 3))

    def replacer(m):
        thead = m.group(1)
        rows = gen_rows_for_cols(thead)
        if rows is None:
            return m.group(0)
        return f"<thead><tr>{thead}</tr></thead><tbody>{rows}</tbody>"

    return re.sub(
        r"<thead><tr>(.*?)</tr></thead><tbody></tbody>", replacer, html, flags=re.DOTALL
    )


new_content = fill_empty_tbody_in_tables(new_content)

# ─── FIX JOIN SECTIONS: ensure they have PostgreSQL panels ────────────────────
# The join section already has PySpark code blocks. We need to add PostgreSQL.
# Let's check which joins need PostgreSQL panels.

JOIN_POSTGRESQL = {
    "Inner Join — Matching Keys Only": """SELECT o.order_id, o.customer_id, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;""",
    "Left Join — Keep All Left Rows": """SELECT o.order_id, o.customer_id, c.name
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id;""",
    "Right Join — Keep All Right Rows": """SELECT o.order_id, o.customer_id, c.name
FROM orders o
RIGHT JOIN customers c ON o.customer_id = c.customer_id;""",
    "Full Outer Join — All Rows from Both": """SELECT o.order_id, o.customer_id, c.name
FROM orders o
FULL OUTER JOIN customers c ON o.customer_id = c.customer_id;""",
    "Left Semi Join — LIKE EXISTS in SQL": """SELECT o.order_id, o.customer_id
FROM orders o
WHERE EXISTS (
    SELECT 1 FROM customers c WHERE c.customer_id = o.customer_id
);""",
    "Left Anti Join — LIKE NOT EXISTS": """SELECT o.order_id, o.customer_id
FROM orders o
WHERE NOT EXISTS (
    SELECT 1 FROM customers c WHERE c.customer_id = o.customer_id
);""",
    "Cross Join — Every Row × Every Row": """SELECT a.id, a.val, b.flag, b.score
FROM df_a a
CROSS JOIN df_b b;""",
    "Broadcast (Map-Side) Join — for Small Tables": """-- PostgreSQL uses hash join automatically for small tables
SET enable_hashjoin = on;
SET enable_seqscan = off;""",
    "Self Join — Hierarchical Data": """SELECT e.emp_id, e.name, e.manager_id, m.name AS mgr_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id;""",
    "Multi-Column Join — Match on Multiple Keys": """SELECT o.order_id, o.region, o.product_id, d.discount
FROM orders o
JOIN discounts d USING (region, product_id);""",
}

# For each join sub-section, find the PySpark code block and add PostgreSQL after it
# The join section uses join-block structure

for join_name, pg_sql in JOIN_POSTGRESQL.items():
    # Find the join-block containing this heading
    pattern = re.compile(
        r"(<h3>"
        + re.escape(join_name)
        + r'</h3>.*?<pre class="code"><code>.*?</code></pre>)',
        re.DOTALL,
    )
    match = pattern.search(new_content)
    if match:
        end_of_pyspark = match.end()
        # Insert PostgreSQL panel after the PySpark block
        pg_block = (
            '\n        <div class="two-col" style="margin-top:0.3rem">'
            '<div class="panel"><h3>PostgreSQL</h3>'
            f'<pre class="code"><code>{escape_html(pg_sql)}</code></pre></div>'
            "</div>"
        )
        # Check if PostgreSQL already exists
        check = new_content.find("PostgreSQL", match.end(), match.end() + 500)
        if check == -1:
            new_content = (
                new_content[:end_of_pyspark] + pg_block + new_content[end_of_pyspark:]
            )
            print(f"  Added PG to: {join_name[:50]}")

# ─── FIX SECTION 17 (Nulls): add PostgreSQL to remaining null sub-sections ───
NULL_POSTGRESQL = {
    "fillna and dropna — Pandas-style aliases": """SELECT
    COALESCE(region, 'UNKNOWN') AS region,
    COALESCE(amount, 0.0)       AS amount
FROM df
WHERE region IS NOT NULL AND amount IS NOT NULL;""",
}

for null_name, pg_sql in NULL_POSTGRESQL.items():
    pattern = re.compile(
        r"(<h3>"
        + re.escape(null_name)
        + r'</h3>.*?<pre class="code"><code>.*?</code></pre>)',
        re.DOTALL,
    )
    match = pattern.search(new_content)
    if match:
        end_of_pyspark = match.end()
        pg_block = (
            '\n        <div class="two-col" style="margin-top:0.3rem">'
            '<div class="panel"><h3>PostgreSQL</h3>'
            f'<pre class="code"><code>{escape_html(pg_sql)}</code></pre></div>'
            "</div>"
        )
        check = new_content.find("PostgreSQL", match.end(), match.end() + 300)
        if check == -1:
            new_content = (
                new_content[:end_of_pyspark] + pg_block + new_content[end_of_pyspark:]
            )
            print(f"  Added PG to nulls: {null_name[:50]}")

# ─── SAVE ─────────────────────────────────────────────────────────────────────
with open(PATH, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"\nDone. File saved to {PATH}")
print(f"Final empty tbody count: {new_content.count('<tbody></tbody>')}")
