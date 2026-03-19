import re

with open("spark/pyspark-code-guide.html", "r", encoding="utf-8") as f:
    content = f.read()


def sub_section(h3, input_tbl, output_tbl, pyspark_code, pg_code):
    cols_in = len(input_tbl[0])
    cols_out = len(output_tbl[0])
    th_in = "".join(f"<th>{h}</th>" for h in input_tbl[0])
    th_out = "".join(f"<th>{h}</th>" for h in output_tbl[0])
    rows_in = "".join(
        "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in input_tbl[1:]
    )
    rows_out = "".join(
        "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in output_tbl[1:]
    )
    return f"""      <h3>{h3}</h3>
      <div class="two-col">
        <div class="panel">
          <h3>Input Table</h3>
          <div class="table-wrap"><table><thead><tr>{th_in}</tr></thead><tbody>{rows_in}</tbody></table></div>
        </div>
        <div class="panel">
          <h3>Output Table</h3>
          <div class="table-wrap"><table><thead><tr>{th_out}</tr></thead><tbody>{rows_out}</tbody></table></div>
        </div>
      </div>
      <div class="two-col">
        <div class="panel">
          <h3>PySpark</h3>
          <pre class="code"><code>{pyspark_code}</code></pre>
        </div>
        <div class="panel">
          <h3>PostgreSQL</h3>
          <pre class="code"><code>{pg_code}</code></pre>
        </div>
      </div>"""


# ─── MATH ───────────────────────────────────────────────────────────────────
math_section = (
    '<section class="concept glass reveal" id="math">\n      <h2>19) Math Functions</h2>\n      <p>Spark\'s math functions are JVM-native and vectorized, making them far faster than Python UDFs. Use them for arithmetic, aggregation, rounding, trigonometry, and statistical transformations.</p>\n\n'
    + sub_section(
        "abs — Absolute Value",
        [["amount"]],
        [["amount", "amount_abs"]],
        'from pyspark.sql.functions import abs\n\ndf.select(abs("amount").alias("amount_abs")).show()',
        "SELECT ABS(amount) AS amount_abs FROM df;",
    )
    + "\n\n"
    + sub_section(
        "sqrt / pow / log / log10 / log2 — Powers and Logarithms",
        [["x"]],
        [["x", "x_sqrt", "x_pow2", "x_log", "x_log10"]],
        'from pyspark.sql.functions import sqrt, pow, log, log10, log2\n\ndf.select(\n    "x",\n    sqrt("x").alias("x_sqrt"),\n    pow("x", 2).alias("x_pow2"),\n    log("x").alias("x_log"),\n    log10("x").alias("x_log10"),\n    log2("x").alias("x_log2")\n).show()',
        "SELECT\n    x,\n    SQRT(x)    AS x_sqrt,\n    POWER(x, 2) AS x_pow2,\n    LN(x)      AS x_log,\n    LOG(x)     AS x_log10,\n    LOG(2, x)  AS x_log2\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "exp / expm1 / log1p — Exponential Functions",
        [["x"]],
        [["x", "x_exp", "x_expm1", "x_log1p"]],
        'from pyspark.sql.functions import exp, expm1, log1p\n\ndf.select(\n    "x",\n    exp("x").alias("x_exp"),\n    expm1("x").alias("x_expm1"),\n    log1p("x").alias("x_log1p")\n).show()',
        "SELECT\n    x,\n    EXP(x)    AS x_exp,\n    EXP(x) - 1 AS x_expm1,\n    LN(1 + x) AS x_log1p\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "floor / ceil / round / bround — Rounding",
        [["value"]],
        [["value", "v_floor", "v_ceil", "v_round2", "v_bround2"]],
        'from pyspark.sql.functions import floor, ceil, round, bround\n\ndf.select(\n    "value",\n    floor("value").alias("v_floor"),\n    ceil("value").alias("v_ceil"),\n    round("value", 2).alias("v_round2"),\n    bround("value", 2).alias("v_bround2")\n).show()',
        "SELECT\n    value,\n    FLOOR(value)  AS v_floor,\n    CEIL(value)   AS v_ceil,\n    ROUND(value, 2) AS v_round2,\n    ROUND(value, 2) AS v_bround2\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "trunc — Truncate to Unit",
        [["value"]],
        [["value", "trunc_d", "trunc_m", "trunc_y"]],
        'from pyspark.sql.functions import trunc\n\ndf.select(\n    "value",\n    trunc("value", "day").alias("trunc_d"),\n    trunc("value", "month").alias("trunc_m"),\n    trunc("value", "year").alias("trunc_y")\n).show()',
        "SELECT\n    value,\n    DATE_TRUNC('day',   value) AS trunc_d,\n    DATE_TRUNC('month',  value) AS trunc_m,\n    DATE_TRUNC('year',   value) AS trunc_y\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "greatest / least — Max/Min Across Columns",
        [["a", "b", "c"]],
        [["a", "b", "c", "greatest", "least"]],
        'from pyspark.sql.functions import greatest, least\n\ndf.select(\n    "a", "b", "c",\n    greatest("a", "b", "c").alias("greatest"),\n    least("a", "b", "c").alias("least")\n).show()',
        "SELECT a, b, c,\n    GREATEST(a, b, c) AS greatest,\n    LEAST(a, b, c)   AS least\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "signum / sign — Sign of Number",
        [["amount"]],
        [["amount", "sgn"]],
        'from pyspark.sql.functions import signum\n\ndf.select(signum("amount").alias("sgn")).show()',
        "SELECT SIGN(amount) AS sgn FROM df;",
    )
    + "\n\n"
    + sub_section(
        "mod / % — Modulo",
        [["a", "b"]],
        [["a", "b", "mod_result"]],
        'from pyspark.sql.functions import col, mod\n\ndf.select(mod("a", "b").alias("mod_result")).show()',
        "SELECT a % b AS mod_result FROM df;",
    )
    + "\n\n"
    + sub_section(
        "cos / sin / tan / acos / asin / atan / atan2 — Trigonometry",
        [["angle_rad"]],
        [["angle_rad", "cos_v", "sin_v", "tan_v"]],
        'from pyspark.sql.functions import cos, sin, tan, acos, asin, atan\n\ndf.select(\n    "angle_rad",\n    cos("angle_rad").alias("cos_v"),\n    sin("angle_rad").alias("sin_v"),\n    tan("angle_rad").alias("tan_v")\n).show()',
        "SELECT\n    angle_rad,\n    COS(angle_rad)  AS cos_v,\n    SIN(angle_rad)  AS sin_v,\n    TAN(angle_rad)  AS tan_v\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "degrees / radians — Angle Conversion",
        [["angle_rad"]],
        [["angle_rad", "to_degrees", "pi_radians"]],
        'from pyspark.sql.functions import degrees, radians\n\ndf.select(\n    "angle_rad",\n    degrees("angle_rad").alias("to_degrees"),\n    radians(180.0).alias("pi_radians")\n).show()',
        "SELECT\n    angle_rad,\n    DEGREES(angle_rad)  AS to_degrees,\n    RADIANS(180.0)     AS pi_radians\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "cbrt — Cube Root",
        [["value"]],
        [["value", "cube_root"]],
        'from pyspark.sql.functions import cbrt\n\ndf.select(cbrt("value").alias("cube_root")).show()',
        "SELECT POWER(value, 1.0/3.0) AS cube_root FROM df;",
    )
    + "\n\n"
    + sub_section(
        "factorial — Factorial",
        [["n"]],
        [["n", "factorial_n"]],
        'from pyspark.sql.functions import factorial\n\ndf.select(factorial("n").alias("factorial_n")).show()',
        "SELECT\n    n,\n    CASE n\n        WHEN 0 THEN 1 WHEN 1 THEN 1 WHEN 2 THEN 2 WHEN 3 THEN 6\n        WHEN 4 THEN 24 WHEN 5 THEN 120 WHEN 6 THEN 720\n    END AS factorial_n\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "bin / hex — Binary/Hexadecimal",
        [["n"]],
        [["n", "n_bin", "n_hex"]],
        'from pyspark.sql.functions import bin, hex\n\ndf.select(\n    "n",\n    bin("n").alias("n_bin"),\n    hex("n").alias("n_hex")\n).show()',
        "SELECT\n    n,\n    TO_HEX(n) AS n_hex\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "conv — Base Conversion",
        [["value"]],
        [["value", "base2", "base16", "back_to_10"]],
        'from pyspark.sql.functions import conv\n\ndf.select(\n    "value",\n    conv("value", 10, 2).alias("base2"),\n    conv("value", 10, 16).alias("base16"),\n    conv(conv("value", 10, 16), 16, 10).alias("back_to_10")\n).show()',
        "SELECT\n    value,\n    value::BINARY AS base2,\n    TO_HEX(value) AS base16\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "nanvl / isnan — NaN Handling",
        [["value"]],
        [["value", "nan_fixed", "is_nan"]],
        'from pyspark.sql.functions import nanvl, isnan\n\ndf.select(\n    "value",\n    nanvl("value", 0.0).alias("nan_fixed"),\n    isnan("value").alias("is_nan")\n).show()',
        "SELECT\n    value,\n    CASE WHEN value IS NULL THEN 0.0 ELSE value END AS nan_fixed,\n    value IS NULL AS is_nan\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "width_bucket — Histogram Bucketing",
        [["amount"]],
        [["amount", "bucket_5", "bucket_10"]],
        'from pyspark.sql.functions import width_bucket\n\ndf.select(\n    width_bucket("amount", 0, 1000, 5).alias("bucket_5"),\n    width_bucket("amount", 0, 1000, 10).alias("bucket_10")\n).show()',
        "SELECT\n    WIDTH_BUCKET(amount, 0, 1000, 5)  AS bucket_5,\n    WIDTH_BUCKET(amount, 0, 1000, 10) AS bucket_10\nFROM df;",
    )
    + "\n    </section>"
)

# ─── STRING ─────────────────────────────────────────────────────────────────
string_section = (
    '<section class="concept glass reveal" id="string">\n      <h2>20) String Functions</h2>\n      <p>String functions are essential for data cleaning, normalization, and pattern extraction. Spark provides both SQL-standard functions and powerful regex capabilities.</p>\n\n'
    + sub_section(
        "upper / lower / initcap — Case Conversion",
        [["name"]],
        [["name", "upper_v", "lower_v", "initcap_v"]],
        'from pyspark.sql.functions import upper, lower, initcap\n\ndf.select(\n    "name",\n    upper("name").alias("upper_v"),\n    lower("name").alias("lower_v"),\n    initcap("name").alias("initcap_v")\n).show()',
        "SELECT\n    name,\n    UPPER(name)    AS upper_v,\n    LOWER(name)    AS lower_v,\n    INITCAP(name)  AS initcap_v\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "trim / ltrim / rtrim — Whitespace Removal",
        [["raw_str"]],
        [["raw_str", "trim_v", "ltrim_v", "rtrim_v"]],
        'from pyspark.sql.functions import trim, ltrim, rtrim\n\ndf.select(\n    "raw_str",\n    trim("raw_str").alias("trim_v"),\n    ltrim("raw_str").alias("ltrim_v"),\n    rtrim("raw_str").alias("rtrim_v")\n).show()',
        "SELECT\n    raw_str,\n    TRIM(raw_str)   AS trim_v,\n    LTRIM(raw_str) AS ltrim_v,\n    RTRIM(raw_str) AS rtrim_v\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "lpad / rpad — Pad String to Width",
        [["code"]],
        [["code", "lpad_8", "rpad_8"]],
        'from pyspark.sql.functions import lpad, rpad\n\ndf.select(\n    "code",\n    lpad("code", 8, "0").alias("lpad_8"),\n    rpad("code", 8, "-").alias("rpad_8")\n).show()',
        "SELECT\n    code,\n    LPAD(code, 8, '0') AS lpad_8,\n    RPAD(code, 8, '-') AS rpad_8\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "concat_ws — Concatenate with Separator",
        [["first_name", "last_name"]],
        [["first_name", "last_name", "full_name"]],
        'from pyspark.sql.functions import concat_ws\n\ndf.select(\n    "first_name", "last_name",\n    concat_ws(" ", "first_name", "last_name").alias("full_name")\n).show()',
        "SELECT\n    first_name, last_name,\n    first_name || ' ' || last_name AS full_name\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "substring / substr — Extract Part of String",
        [["email"]],
        [["email", "local_part", "domain"]],
        'from pyspark.sql.functions import substring, instr\n\ndf.select(\n    "email",\n    substring("email", 1, instr("email", "@") - 1).alias("local_part"),\n    substring("email", instr("email", "@") + 1, 100).alias("domain")\n).show()',
        "SELECT\n    email,\n    SPLIT_PART(email, '@', 1) AS local_part,\n    SPLIT_PART(email, '@', 2) AS domain\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "split — Split String into Array",
        [["path"]],
        [["path", "part_0", "part_2"]],
        'from pyspark.sql.functions import split\n\ndf.select(\n    "path",\n    split("path", "/")[0].alias("part_0"),\n    split("path", "/")[2].alias("part_2")\n).show()',
        "SELECT\n    path,\n    SPLIT_PART(path, '/', 1) AS part_0,\n    SPLIT_PART(path, '/', 3) AS part_2\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "contains / instr — Substring Search",
        [["text"]],
        [["text", "has_spark", "spark_pos"]],
        'from pyspark.sql.functions import contains, instr\n\ndf.select(\n    "text",\n    contains("text", "Spark").alias("has_spark"),\n    instr("text", "Spark").alias("spark_pos")\n).show()',
        "SELECT\n    text,\n    text LIKE '%Spark%'                AS has_spark,\n    POSITION('Spark' IN text)          AS spark_pos\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "startswith / endswith — Prefix/Suffix Match",
        [["product"]],
        [["product", "is_widget", "is_pro"]],
        'from pyspark.sql.functions import col\n\ndf.select(\n    "product",\n    col("product").startswith("Widget").alias("is_widget"),\n    col("product").endswith("Pro").alias("is_pro")\n).show()',
        "SELECT\n    product,\n    product LIKE 'Widget%' AS is_widget,\n    product LIKE '%Pro'    AS is_pro\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "length / char_length — String Length",
        [["word"]],
        [["word", "len_v"]],
        'from pyspark.sql.functions import length\n\ndf.select(length("word").alias("len_v")).show()',
        "SELECT LENGTH(word) AS len_v FROM df;",
    )
    + "\n\n"
    + sub_section(
        "reverse — Reverse String",
        [["code"]],
        [["code", "reversed"]],
        'from pyspark.sql.functions import reverse\n\ndf.select(reverse("code").alias("reversed")).show()',
        "SELECT REVERSE(code) AS reversed FROM df;",
    )
    + "\n\n"
    + sub_section(
        "repeat — Repeat String N Times",
        [["char_v", "n"]],
        [["char_v", "n", "repeated"]],
        'from pyspark.sql.functions import repeat\n\ndf.select(repeat("char_v", 3).alias("repeated")).show()',
        "SELECT REPEAT(char_v, 3) AS repeated FROM df;",
    )
    + "\n\n"
    + sub_section(
        "translate — Character-by-Character Replacement",
        [["raw"]],
        [["raw", "translated"]],
        'from pyspark.sql.functions import translate\n\ndf.select(translate("raw", "aei", "xyz").alias("translated")).show()',
        "SELECT TRANSLATE(raw, 'aei', 'xyz') AS translated FROM df;",
    )
    + "\n\n"
    + sub_section(
        "overlay — Replace Portion of String",
        [["text"]],
        [["text", "overlay_v"]],
        'from pyspark.sql.functions import overlay\n\ndf.select(overlay("text", "XXX", 5, 3).alias("overlay_v")).show()',
        "SELECT OVERLAY(text PLACING 'XXX' FROM 5 FOR 3) AS overlay_v FROM df;",
    )
    + "\n\n"
    + sub_section(
        "regexp_extract — Extract with Regex Groups",
        [["log_line"]],
        [["log_line", "level", "component", "msg"]],
        'from pyspark.sql.functions import regexp_extract\n\ndf.select(\n    regexp_extract("log_line", r"\\[(\\w+)\\] ", 1).alias("level"),\n    regexp_extract("log_line", r"\\{(\\w+)\\}", 1).alias("component"),\n    regexp_extract("log_line", r": (.+)$", 1).alias("msg")\n).show()',
        "SELECT\n    (REGEXP_MATCHES(log_line, '\\[(\\w+)\\] '))[1] AS level,\n    (REGEXP_MATCHES(log_line, '\\{(\\w+)\\}') )[1] AS component,\n    (REGEXP_MATCHES(log_line, ': (.+)$'))[1]        AS msg\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "regexp_replace — Replace with Regex",
        [["text"]],
        [["text", "cleaned", "digits_only"]],
        'from pyspark.sql.functions import regexp_replace\n\ndf.select(\n    "text",\n    regexp_replace("text", r"[^a-zA-Z0-9 ]", "").alias("cleaned"),\n    regexp_replace("text", r"\\D", "").alias("digits_only")\n).show()',
        "SELECT\n    text,\n    REGEXP_REPLACE(text, '[^a-zA-Z0-9 ]', '') AS cleaned,\n    REGEXP_REPLACE(text, '\\D', '')             AS digits_only\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "rlike — Full Regex Match",
        [["email"]],
        [["email", "is_corp", "is_dev"]],
        'from pyspark.sql.functions import col\n\ndf.select(\n    "email",\n    col("email").rlike(r"^[a-z]+@company\\.com$").alias("is_corp"),\n    col("email").rlike(r"^[a-z]+@(dev|test)\\.io$").alias("is_dev")\n).show()',
        "SELECT\n    email,\n    email ~ '^[a-z]+@company\\.com$'    AS is_corp,\n    email ~ '^[a-z]+@(dev|test)\\.io$' AS is_dev\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "locate / position — Find Substring Position",
        [["text", "sub"]],
        [["text", "sub", "pos_v"]],
        'from pyspark.sql.functions import locate\n\ndf.select(locate("sub", "text", 1).alias("pos_v")).show()',
        "SELECT POSITION(sub IN text) AS pos_v FROM df;",
    )
    + "\n\n"
    + sub_section(
        "soundex / levenshtein — Fuzzy Matching",
        [["name1", "name2"]],
        [["name1", "name2", "sdx1", "sdx2"]],
        'from pyspark.sql.functions import soundex, levenshtein\n\ndf.select(\n    "name1", "name2",\n    soundex("name1").alias("sdx1"),\n    soundex("name2").alias("sdx2"),\n    levenshtein("name1", "name2").alias("lev_dist")\n).show()',
        "SELECT\n    name1, name2,\n    SOUNDEX(name1) AS sdx1,\n    SOUNDEX(name2) AS sdx2\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "ascii / chr — Character Code Conversion",
        [["char_v", "code"]],
        [["char_v", "code", "ascii_v", "chr_v"]],
        'from pyspark.sql.functions import ascii, chr\n\ndf.select(\n    "char_v", "code",\n    ascii("char_v").alias("ascii_v"),\n    chr("code").alias("chr_v")\n).show()',
        "SELECT\n    char_v, code,\n    ASCII(char_v) AS ascii_v,\n    CHR(code)     AS chr_v\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "format_string / printf — String Formatting",
        [["name", "score"]],
        [["name", "score", "formatted"]],
        'from pyspark.sql.functions import format_string\n\ndf.select(format_string("%s scored %d", "name", "score").alias("formatted")).show()',
        "SELECT FORMAT('%s scored %d', name, score) AS formatted FROM df;",
    )
    + "\n    </section>"
)

# ─── WINDOW ─────────────────────────────────────────────────────────────────
window_section = (
    '<section class="concept glass reveal" id="window">\n      <h2>21) Window Functions</h2>\n      <p>Window functions compute row-level analytics without collapsing rows. They operate on a frame of rows relative to the current row. Use <code>partitionBy()</code> to define groups and <code>orderBy()</code> to define row ordering within each partition.</p>\n\n'
    + sub_section(
        "Window Definition — partitionBy + orderBy",
        [["region", "amount"]],
        [["region", "amount", "running_sum"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import sum as Fsum\n\nw = Window.partitionBy("region").orderBy("amount")\n\ndf.withColumn("running_sum", Fsum("amount").over(w)).show()',
        "SELECT region, amount,\n    SUM(amount) OVER (PARTITION BY region ORDER BY amount) AS running_sum\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "row_number — Sequential Row Number (No Gaps)",
        [["region", "amount"]],
        [["region", "amount", "row_num"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import row_number\n\nw = Window.partitionBy("region").orderBy("amount")\n\ndf.withColumn("row_num", row_number().over(w)).show()',
        "SELECT region, amount,\n    ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount) AS row_num\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "rank — Rank with Gaps (1, 2, 2, 4)",
        [["region", "amount"]],
        [["region", "amount", "rank_v"]],
        'from pyspark.sql.functions import rank\n\nw = Window.partitionBy("region").orderBy("amount")\n\ndf.withColumn("rank_v", rank().over(w)).show()',
        "SELECT region, amount,\n    RANK() OVER (PARTITION BY region ORDER BY amount) AS rank_v\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "dense_rank — Rank Without Gaps (1, 2, 2, 3)",
        [["region", "amount"]],
        [["region", "amount", "dense_rank_v"]],
        'from pyspark.sql.functions import dense_rank\n\nw = Window.partitionBy("region").orderBy("amount")\n\ndf.withColumn("dense_rank_v", dense_rank().over(w)).show()',
        "SELECT region, amount,\n    DENSE_RANK() OVER (PARTITION BY region ORDER BY amount) AS dense_rank_v\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "percent_rank — Percentile Rank (0.0 to 1.0)",
        [["region", "amount"]],
        [["region", "amount", "pct_rank"]],
        'from pyspark.sql.functions import percent_rank\n\nw = Window.partitionBy("region").orderBy("amount")\n\ndf.withColumn("pct_rank", percent_rank().over(w)).show()',
        "SELECT region, amount,\n    PERCENT_RANK() OVER (PARTITION BY region ORDER BY amount) AS pct_rank\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "ntile — Divide Rows into N Buckets",
        [["region", "amount"]],
        [["region", "amount", "quartile", "tercile"]],
        'from pyspark.sql.functions import ntile\n\nw = Window.partitionBy("region").orderBy("amount")\n\ndf.select(\n    "region", "amount",\n    ntile(4).over(w).alias("quartile"),\n    ntile(3).over(w).alias("tercile")\n).show()',
        "SELECT region, amount,\n    NTILE(4) OVER (PARTITION BY region ORDER BY amount) AS quartile,\n    NTILE(3) OVER (PARTITION BY region ORDER BY amount) AS tercile\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "first_value / last_value — First/Last in Window Frame",
        [["region", "amount"]],
        [["region", "amount", "first_v", "last_v"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import first, last\n\nw = Window.partitionBy("region").orderBy("amount")\n\ndf.select(\n    "region", "amount",\n    first("amount").over(w).alias("first_v"),\n    last("amount").over(w).alias("last_v")\n).show()',
        "SELECT region, amount,\n    FIRST_VALUE(amount) OVER w AS first_v,\n    LAST_VALUE(amount)  OVER w AS last_v\nFROM df WINDOW w AS (PARTITION BY region ORDER BY amount);",
    )
    + "\n\n"
    + sub_section(
        "nth_value — Nth Value in Window Frame",
        [["region", "amount"]],
        [["region", "amount", "3rd_value"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import nth_value\n\nw = Window.partitionBy("region").orderBy("amount")\n\ndf.select(\n    nth_value("amount", 3).over(w).alias("3rd_value")\n).show()',
        "SELECT region, amount,\n    NTH_VALUE(amount, 3) OVER w AS 3rd_value\nFROM df WINDOW w AS (PARTITION BY region ORDER BY amount);",
    )
    + "\n\n"
    + sub_section(
        "lag / lead — Previous/Next Row Value",
        [["event_time", "amount"]],
        [["event_time", "amount", "prev_amt", "next_amt"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import lag, lead\n\nw = Window.partitionBy("region").orderBy("event_time")\n\ndf.select(\n    "event_time", "amount",\n    lag("amount", 1).over(w).alias("prev_amt"),\n    lead("amount", 1).over(w).alias("next_amt")\n).show()',
        "SELECT event_time, amount,\n    LAG(amount, 1)   OVER w AS prev_amt,\n    LEAD(amount, 1)  OVER w AS next_amt\nFROM df WINDOW w AS (PARTITION BY region ORDER BY event_time);",
    )
    + "\n\n"
    + sub_section(
        "sum / avg / count / min / max — Aggregate Over Window",
        [["region", "amount"]],
        [
            [
                "region",
                "amount",
                "running_sum",
                "running_avg",
                "running_count",
                "running_min",
                "running_max",
            ]
        ],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import sum as Fsum, avg, count, min as Fmin, max as Fmax\n\nw = Window.partitionBy("region").orderBy("amount")\n\ndf.select(\n    "region", "amount",\n    Fsum("amount").over(w).alias("running_sum"),\n    avg("amount").over(w).alias("running_avg"),\n    count("amount").over(w).alias("running_count"),\n    Fmin("amount").over(w).alias("running_min"),\n    Fmax("amount").over(w).alias("running_max")\n).show()',
        "SELECT region, amount,\n    SUM(amount)  OVER w AS running_sum,\n    AVG(amount)  OVER w AS running_avg,\n    COUNT(amount) OVER w AS running_count,\n    MIN(amount) OVER w AS running_min,\n    MAX(amount) OVER w AS running_max\nFROM df WINDOW w AS (PARTITION BY region ORDER BY amount);",
    )
    + "\n\n"
    + sub_section(
        "cume_dist — Cumulative Distribution",
        [["region", "amount"]],
        [["region", "amount", "cume_dist_v"]],
        'from pyspark.sql.functions import cume_dist\n\nw = Window.partitionBy("region").orderBy("amount")\n\ndf.withColumn("cume_dist_v", cume_dist().over(w)).show()',
        "SELECT region, amount,\n    CUME_DIST() OVER (PARTITION BY region ORDER BY amount) AS cume_dist_v\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "collect_list / collect_set — Collect Values as List/Set",
        [["region", "product"]],
        [["region", "product", "all_products", "unique_products"]],
        'from pyspark.sql.functions import collect_list, collect_set\n\nw = Window.partitionBy("region")\n\ndf.select(\n    "region",\n    collect_list("product").over(w).alias("all_products"),\n    collect_set("product").over(w).alias("unique_products")\n).distinct().show()',
        "SELECT region,\n    ARRAY_AGG(product)            OVER w AS all_products,\n    ARRAY_AGG(DISTINCT product)   OVER w AS unique_products\nFROM df WINDOW w AS (PARTITION BY region);",
    )
    + "\n    </section>"
)

# ─── LEAD AND LAG ────────────────────────────────────────────────────────────
leadlag_section = (
    '<section class="concept glass reveal" id="lead-lag">\n      <h2>22) Lead and Lag</h2>\n      <p><code>lag(col, n, default)</code> returns the value from n rows before the current row. <code>lead(col, n, default)</code> returns the value from n rows after the current row. Both are essential for time-series comparisons and period-over-period analysis.</p>\n\n'
    + sub_section(
        "lag — Previous Row Value",
        [["event_time", "amount"]],
        [["event_time", "amount", "prev_amount", "prev_2"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import lag\n\nw = Window.partitionBy("region").orderBy("event_time")\n\ndf.select(\n    "event_time", "amount",\n    lag("amount", 1).over(w).alias("prev_amount"),\n    lag("amount", 2).over(w).alias("prev_2")\n).show()',
        "SELECT event_time, amount,\n    LAG(amount, 1) OVER w AS prev_amount,\n    LAG(amount, 2) OVER w AS prev_2\nFROM df WINDOW w AS (PARTITION BY region ORDER BY event_time);",
    )
    + "\n\n"
    + sub_section(
        "lead — Next Row Value",
        [["event_time", "amount"]],
        [["event_time", "amount", "next_amount", "next_2"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import lead\n\nw = Window.partitionBy("region").orderBy("event_time")\n\ndf.select(\n    "event_time", "amount",\n    lead("amount", 1).over(w).alias("next_amount"),\n    lead("amount", 2).over(w).alias("next_2")\n).show()',
        "SELECT event_time, amount,\n    LEAD(amount, 1) OVER w AS next_amount,\n    LEAD(amount, 2) OVER w AS next_2\nFROM df WINDOW w AS (PARTITION BY region ORDER BY event_time);",
    )
    + "\n\n"
    + sub_section(
        "lag / lead with Default Value",
        [["event_time", "amount"]],
        [["event_time", "amount", "prev_0", "next_default"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import lag, lead, coalesce, lit\n\nw = Window.partitionBy("region").orderBy("event_time")\n\ndf.select(\n    "event_time", "amount",\n    coalesce(lag("amount", 1).over(w), lit(0.0)).alias("prev_0"),\n    coalesce(lead("amount", 1).over(w), lit(-1.0)).alias("next_default")\n).show()',
        "SELECT event_time, amount,\n    COALESCE(LAG(amount, 1) OVER w, 0.0)  AS prev_0,\n    COALESCE(LEAD(amount, 1) OVER w, -1.0) AS next_default\nFROM df WINDOW w AS (PARTITION BY region ORDER BY event_time);",
    )
    + "\n\n"
    + sub_section(
        "Period-over-Period Change with lag",
        [["event_time", "amount"]],
        [["event_time", "amount", "prev_amount", "amount_change", "pct_change"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import lag, round as Fround\n\nw = Window.partitionBy("region").orderBy("event_time")\n\nresult = df.withColumn("prev_amount", lag("amount", 1).over(w))\\\n    .withColumn("amount_change", result["amount"] - result["prev_amount"])\\\n    .withColumn("pct_change", Fround(\n        (result["amount"] - result["prev_amount"]) / result["prev_amount"] * 100, 2))\n\nresult.select("event_time", "amount", "prev_amount", "amount_change", "pct_change").show()',
        "SELECT event_time, amount,\n    LAG(amount, 1) OVER w AS prev_amount,\n    amount - LAG(amount, 1) OVER w AS amount_change,\n    ROUND((amount - LAG(amount, 1) OVER w) / NULLIF(LAG(amount, 1) OVER w, 0) * 100, 2) AS pct_change\nFROM df WINDOW w AS (PARTITION BY region ORDER BY event_time);",
    )
    + "\n\n"
    + sub_section(
        "Streak / Gap Detection with lag",
        [["event_time", "status"]],
        [["event_time", "status", "prev_status", "status_changed"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import lag, when, col, lit\n\nw = Window.partitionBy("region").orderBy("event_time")\n\ndf.select(\n    "event_time", "status",\n    lag("status", 1).over(w).alias("prev_status"),\n    when(lag("status", 1).over(w) != "status", lit(True)).otherwise(lit(False)).alias("status_changed")\n).show()',
        "SELECT event_time, status,\n    LAG(status, 1) OVER w AS prev_status,\n    LAG(status, 1) OVER w IS DISTINCT FROM status AS status_changed\nFROM df WINDOW w AS (PARTITION BY region ORDER BY event_time);",
    )
    + "\n    </section>"
)

# ─── ROWS BETWEEN ────────────────────────────────────────────────────────────
rows_section = (
    '<section class="concept glass reveal" id="rows-between">\n      <h2>23) Rows Between — Window Frame Boundaries</h2>\n      <p><code>rowsBetween(start, end)</code> defines the frame of rows relative to the current row for aggregate window functions. The frame slides with each row. By default, aggregate functions use <code>RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW</code>.</p>\n\n'
    + sub_section(
        "Window.unboundedPreceding — All Rows Before Current (Running Total)",
        [["event_time", "amount"]],
        [["event_time", "amount", "cumulative_sum", "cumulative_count"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import sum as Fsum, count\n\nw_all = Window.partitionBy("region").orderBy("event_time").rowsBetween(Window.unboundedPreceding, Window.currentRow)\n\ndf.select(\n    "event_time", "amount",\n    Fsum("amount").over(w_all).alias("cumulative_sum"),\n    count("amount").over(w_all).alias("cumulative_count")\n).show()',
        "SELECT event_time, amount,\n    SUM(amount)  OVER w AS cumulative_sum,\n    COUNT(amount) OVER w AS cumulative_count\nFROM df\nWINDOW w AS (\n    PARTITION BY region\n    ORDER BY event_time\n    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n);",
    )
    + "\n\n"
    + sub_section(
        "Window.unboundedFollowing — All Rows After Current",
        [["event_time", "amount"]],
        [["event_time", "amount", "reverse_sum"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import sum as Fsum\n\nw_rev = Window.partitionBy("region").orderBy("event_time").rowsBetween(Window.currentRow, Window.unboundedFollowing)\n\ndf.select(\n    "event_time", "amount",\n    Fsum("amount").over(w_rev).alias("reverse_sum")\n).show()',
        "SELECT event_time, amount,\n    SUM(amount) OVER w AS reverse_sum\nFROM df\nWINDOW w AS (\n    PARTITION BY region\n    ORDER BY event_time\n    ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING\n);",
    )
    + "\n\n"
    + sub_section(
        "rowsBetween(N, M) — Fixed Frame Size",
        [["event_time", "amount"]],
        [["event_time", "amount", "sum_3_back", "sum_prev_next", "avg_2_ahead"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import sum as Fsum, avg\n\nw_3back = Window.orderBy("event_time").rowsBetween(-3, 0)\nw_around = Window.orderBy("event_time").rowsBetween(-1, 1)\nw_2ahead = Window.orderBy("event_time").rowsBetween(0, 2)\n\ndf.select(\n    "event_time", "amount",\n    Fsum("amount").over(w_3back).alias("sum_3_back"),\n    Fsum("amount").over(w_around).alias("sum_prev_next"),\n    avg("amount").over(w_2ahead).alias("avg_2_ahead")\n).show()',
        "SELECT event_time, amount,\n    SUM(amount) OVER (ORDER BY event_time ROWS BETWEEN 3 PRECEDING AND CURRENT ROW)  AS sum_3_back,\n    SUM(amount) OVER (ORDER BY event_time ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS sum_prev_next,\n    AVG(amount) OVER (ORDER BY event_time ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING) AS avg_2_ahead\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "rowsBetween(0, 0) — Current Row Only",
        [["event_time", "amount"]],
        [["event_time", "amount", "same_as_amount"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import sum as Fsum\n\nw_curr = Window.orderBy("event_time").rowsBetween(0, 0)\n\ndf.select(\n    "event_time", "amount",\n    Fsum("amount").over(w_curr).alias("same_as_amount")\n).show()',
        "SELECT event_time, amount,\n    SUM(amount) OVER (\n        ORDER BY event_time\n        ROWS BETWEEN CURRENT ROW AND CURRENT ROW\n    ) AS same_as_amount\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "rangeBetween vs rowsBetween — RANGE Uses Value, ROWS Uses Position",
        [["ts", "amount"]],
        [["ts", "amount", "sum_rows_2", "sum_range_2"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import sum as Fsum\n\n# ROWS: includes 2 rows before regardless of value\nw_rows = Window.partitionBy("region").orderBy("ts").rowsBetween(-2, 0)\n# RANGE: includes rows where key <= current key + 2 (in same partition)\nw_range = Window.partitionBy("region").orderBy("ts").rangeBetween(-2, 0)\n\ndf.select(\n    "ts", "amount",\n    Fsum("amount").over(w_rows).alias("sum_rows_2"),\n    Fsum("amount").over(w_range).alias("sum_range_2")\n).show()',
        "-- PostgreSQL uses ROWS mode by default.\n-- RANGE with offset (in terms of ORDER BY value):\nSELECT ts, amount,\n    SUM(amount) OVER (\n        PARTITION BY region\n        ORDER BY ts\n        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW\n    ) AS sum_rows_2,\n    SUM(amount) OVER (\n        PARTITION BY region\n        ORDER BY ts\n        RANGE BETWEEN 2 PRECEDING AND CURRENT ROW\n    ) AS sum_range_2\nFROM df;",
    )
    + "\n\n"
    + sub_section(
        "First/Last in Sliding Frame with rowsBetween",
        [["event_time", "amount"]],
        [["event_time", "amount", "first_in_frame", "last_in_frame"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import first, last\n\nw_frame = Window.partitionBy("region").orderBy("event_time").rowsBetween(-2, 0)\n\ndf.select(\n    "event_time", "amount",\n    first("amount").over(w_frame).alias("first_in_frame"),\n    last("amount").over(w_frame).alias("last_in_frame")\n).show()',
        "SELECT event_time, amount,\n    FIRST_VALUE(amount) OVER w AS first_in_frame,\n    LAST_VALUE(amount)  OVER w AS last_in_frame\nFROM df\nWINDOW w AS (\n    PARTITION BY region\n    ORDER BY event_time\n    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW\n);",
    )
    + "\n\n"
    + sub_section(
        "Running Total + Moving Average + Moving Count",
        [["event_time", "amount"]],
        [["event_time", "amount", "running_total", "moving_avg_3", "moving_count_5"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import sum as Fsum, avg, count\n\nw_total = Window.partitionBy("region").orderBy("event_time").rowsBetween(Window.unboundedPreceding, Window.currentRow)\nw_avg3  = Window.partitionBy("region").orderBy("event_time").rowsBetween(-2, 0)\nw_cnt5  = Window.partitionBy("region").orderBy("event_time").rowsBetween(-4, 0)\n\ndf.select(\n    "event_time", "amount",\n    Fsum("amount").over(w_total).alias("running_total"),\n    avg("amount").over(w_avg3).alias("moving_avg_3"),\n    count("amount").over(w_cnt5).alias("moving_count_5")\n).show()',
        "SELECT event_time, amount,\n    SUM(amount)   OVER w_total AS running_total,\n    AVG(amount)   OVER w_avg3  AS moving_avg_3,\n    COUNT(amount) OVER w_cnt5  AS moving_count_5\nFROM df\nWINDOW\n    w_total AS (PARTITION BY region ORDER BY event_time ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW),\n    w_avg3  AS (PARTITION BY region ORDER BY event_time ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),\n    w_cnt5  AS (PARTITION BY region ORDER BY event_time ROWS BETWEEN 4 PRECEDING AND CURRENT ROW);",
    )
    + "\n\n"
    + sub_section(
        "Lag/Lead Offsets in Sliding Window Frame",
        [["event_time", "amount"]],
        [["event_time", "amount", "lag_1", "lag_2", "lead_1"]],
        'from pyspark.sql import Window\nfrom pyspark.sql.functions import lag, lead\n\nw = Window.partitionBy("region").orderBy("event_time")\n\ndf.select(\n    "event_time", "amount",\n    lag("amount", 1).over(w).alias("lag_1"),\n    lag("amount", 2).over(w).alias("lag_2"),\n    lead("amount", 1).over(w).alias("lead_1")\n).show()',
        "SELECT event_time, amount,\n    LAG(amount, 1)  OVER w AS lag_1,\n    LAG(amount, 2)  OVER w AS lag_2,\n    LEAD(amount, 1) OVER w AS lead_1\nFROM df\nWINDOW w AS (PARTITION BY region ORDER BY event_time);",
    )
    + "\n    </section>"
)

# ─── INSERT ALL SECTIONS ─────────────────────────────────────────────────────
# Find the end of the datetime section and insert all others after it
dt_start = content.find('id="datetime"')
dt_end = content.find("</section>", dt_start) + len("</section>")

# Insert math, string, window, lead-lag, rows-between after datetime
insert_pos = dt_end
new_content = (
    content[:insert_pos]
    + "\n\n"
    + math_section
    + "\n\n"
    + string_section
    + "\n\n"
    + window_section
    + "\n\n"
    + leadlag_section
    + "\n\n"
    + rows_section
    + "\n    </div>\n  </main>"
    + content[insert_pos + len("\n    </div>\n  </main>") :]
)

with open("spark/pyspark-code-guide.html", "w", encoding="utf-8") as f:
    f.write(new_content)

lines = new_content.count("\n")
print("Done! ~" + str(lines) + " lines")

import re

tags = ["div", "section", "pre", "table", "svg"]
for tag in tags:
    opens = len(re.findall(rf"<{tag}[\s>]", new_content))
    closes = len(re.findall(rf"</{tag}>", new_content))
    ok = "OK" if opens == closes else "MISMATCH"
    print(f"  {tag}: {opens}/{closes} {ok}")
