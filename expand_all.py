import re

with open("spark/pyspark-code-guide.html", "r", encoding="utf-8") as f:
    content = f.read()


def sub_section(h3, input_tbl, output_tbl, pyspark_code, pg_code):
    """Build a sub-section with input table, output table, PySpark code, and PostgreSQL query."""
    return f"""      <h3>{h3}</h3>
      <div class="two-col">
        <div class="panel">
          <h3>Input Table</h3>
          <div class="table-wrap"><table><thead><tr>{"".join(f"<th>{h}</th>" for h in input_tbl[0])}</tr></thead><tbody>{"".join(f"<tr>{''.join(f'<td>{c}</td>' for c in row)}</tr>" for row in input_tbl[1:])}</tbody></table></div>
        </div>
        <div class="panel">
          <h3>Output Table</h3>
          <div class="table-wrap"><table><thead><tr>{"".join(f"<th>{h}</th>" for h in output_tbl[0])}</tr></thead><tbody>{"".join(f"<tr>{''.join(f'<td>{c}</td>' for c in row)}</tr>" for row in output_tbl[1:])}</tbody></table></div>
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


def tbl_row(cells):
    return "".join(f"<td>{c}</td>" for c in cells)


# ═══════════════════════════════════════════════════════════════════════════════
# 1. DATE AND TIME FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
datetime_section = (
    """<section class="concept glass reveal" id="datetime">
      <h2>18) Date and Time Functions</h2>
      <p>Spark provides a comprehensive set of date and time functions for parsing, formatting, truncating, extracting components, and timezone conversions. Use these for partitioning, trend analytics, SLA calculations, and event-time pipelines.</p>

"""
    + sub_section(
        "current_date / current_timestamp — Today's Date and Now",
        [["event_date", "event_ts"]],
        [["event_date", "event_ts"]],
        """from pyspark.sql.functions import current_date, current_timestamp

df.select(
    current_date().alias("event_date"),
    current_timestamp().alias("event_ts")
).show(1)""",
        """SELECT
    CURRENT_DATE AS event_date,
    NOW()        AS event_ts;""",
    )
    + """

"""
    + sub_section(
        "to_date / to_timestamp — Parse String to Date/Timestamp",
        [["event_time"]],
        [["event_date", "event_ts"]],
        """from pyspark.sql.functions import to_date, to_timestamp

df.select(
    to_date("event_time", "yyyy-MM-dd HH:mm:ss").alias("event_date"),
    to_timestamp("event_time", "yyyy-MM-dd HH:mm:ss").alias("event_ts")
).show()""",
        """SELECT
    CAST('2026-03-01 10:12:33' AS DATE)        AS event_date,
    CAST('2026-03-01 10:12:33' AS TIMESTAMP)  AS event_ts;""",
    )
    + """

"""
    + sub_section(
        "date_format — Format Date/Timestamp to String",
        [["event_ts"]],
        [["event_ts", "day_str", "hour_str", "month_str"]],
        """from pyspark.sql.functions import date_format

df.select(
    "event_ts",
    date_format("event_ts", "yyyy-MM-dd").alias("day_str"),
    date_format("event_ts", "HH:mm").alias("hour_str"),
    date_format("event_ts", "MMM yyyy").alias("month_str")
).show()""",
        """SELECT
    event_ts,
    TO_CHAR(event_ts, 'YYYY-MM-DD') AS day_str,
    TO_CHAR(event_ts, 'HH24:MI')    AS hour_str,
    TO_CHAR(event_ts, 'Mon YYYY')   AS month_str
FROM events;""",
    )
    + """

"""
    + sub_section(
        "date_trunc — Truncate to Unit (date_trunc)",
        [["event_ts"]],
        [["event_ts", "trunc_hour", "trunc_day", "trunc_month"]],
        """from pyspark.sql.functions import date_trunc

df.select(
    "event_ts",
    date_trunc("hour", "event_ts").alias("trunc_hour"),
    date_trunc("day", "event_ts").alias("trunc_day"),
    date_trunc("month", "event_ts").alias("trunc_month")
).show()""",
        """SELECT
    event_ts,
    DATE_TRUNC('hour',   event_ts) AS trunc_hour,
    DATE_TRUNC('day',    event_ts) AS trunc_day,
    DATE_TRUNC('month',  event_ts) AS trunc_month
FROM events;""",
    )
    + """

"""
    + sub_section(
        "timestamp_trunc / time_trunc — Truncate Timestamp or Time",
        [["event_ts"]],
        [["event_ts", "ts_trunc_hour", "ts_trunc_min"]],
        """from pyspark.sql.functions import timestamp_trunc, time_trunc

df.select(
    "event_ts",
    timestamp_trunc("event_ts", "hour").alias("ts_trunc_hour"),
    timestamp_trunc("event_ts", "minute").alias("ts_trunc_min")
).show()""",
        """SELECT
    event_ts,
    DATE_TRUNC('hour',   event_ts) AS ts_trunc_hour,
    DATE_TRUNC('minute', event_ts) AS ts_trunc_min;""",
    )
    + """

"""
    + sub_section(
        "year / month / day / hour / minute / second — Extract Components",
        [["event_ts"]],
        [["event_ts", "yr", "mo", "dy", "hr", "mi", "sc"]],
        """from pyspark.sql.functions import year, month, day, hour, minute, second

df.select(
    "event_ts",
    year("event_ts").alias("yr"),
    month("event_ts").alias("mo"),
    day("event_ts").alias("dy"),
    hour("event_ts").alias("hr"),
    minute("event_ts").alias("mi"),
    second("event_ts").alias("sc")
).show()""",
        """SELECT
    event_ts,
    EXTRACT(YEAR    FROM event_ts) AS yr,
    EXTRACT(MONTH   FROM event_ts) AS mo,
    EXTRACT(DAY     FROM event_ts) AS dy,
    EXTRACT(HOUR    FROM event_ts) AS hr,
    EXTRACT(MINUTE  FROM event_ts) AS mi,
    EXTRACT(SECOND  FROM event_ts) AS sc
FROM events;""",
    )
    + """

"""
    + sub_section(
        "dayofweek / dayofmonth / dayofyear / quarter / weekofyear",
        [["event_ts"]],
        [["event_ts", "dow", "dom", "doy", "qtr", "woy"]],
        """from pyspark.sql.functions import dayofweek, dayofmonth, dayofyear, quarter, weekofyear

df.select(
    "event_ts",
    dayofweek("event_ts").alias("dow"),   -- 1=Sunday, 7=Saturday
    dayofmonth("event_ts").alias("dom"),  -- 1-31
    dayofyear("event_ts").alias("doy"),   -- 1-366
    quarter("event_ts").alias("qtr"),       -- 1-4
    weekofyear("event_ts").alias("woy")    -- 1-53
).show()""",
        """SELECT
    event_ts,
    EXTRACT(DOW       FROM event_ts) AS dow,  -- 0=Sunday
    EXTRACT(DAY       FROM event_ts) AS dom,
    EXTRACT(DOY       FROM event_ts) AS doy,
    EXTRACT(QUARTER   FROM event_ts) AS qtr,
    EXTRACT(WEEK      FROM event_ts) AS woy
FROM events;""",
    )
    + """

"""
    + sub_section(
        "datediff / date_add / date_sub — Date Arithmetic",
        [["start_date", "end_date"]],
        [["start_date", "end_date", "days_diff", "plus_5", "minus_3"]],
        """from pyspark.sql.functions import datediff, date_add, date_sub

df.select(
    "start_date", "end_date",
    datediff("end_date", "start_date").alias("days_diff"),
    date_add("start_date", 5).alias("plus_5"),
    date_sub("start_date", 3).alias("minus_3")
).show()""",
        """SELECT
    start_date, end_date,
    (end_date - start_date)               AS days_diff,
    start_date + INTERVAL '5 days'        AS plus_5,
    start_date - INTERVAL '3 days'        AS minus_3
FROM events;""",
    )
    + """

"""
    + sub_section(
        "months_between — Months Between Two Dates",
        [["start_date", "end_date"]],
        [["start_date", "end_date", "months"]],
        """from pyspark.sql.functions import months_between, floor

df.select(
    "start_date", "end_date",
    floor(months_between("end_date", "start_date")).alias("months")
).show()""",
        """SELECT
    start_date, end_date,
    EXTRACT(EPOCH FROM (end_date - start_date)) / (30.44 * 86400) AS months;
    -- Or use age() and extract:
    EXTRACT(YEAR  FROM AGE(end_date, start_date)) * 12 +
    EXTRACT(MONTH FROM AGE(end_date, start_date)) AS months;""",
    )
    + """

"""
    + sub_section(
        "add_months / next_day / last_day",
        [["event_date"]],
        [["event_date", "add_3m", "next_mon", "last_day_m"]],
        """from pyspark.sql.functions import add_months, next_day, last_day

df.select(
    "event_date",
    add_months("event_date", 3).alias("add_3m"),
    next_day("event_date", "Monday").alias("next_mon"),
    last_day("event_date").alias("last_day_m")
).show()""",
        """SELECT
    event_date,
    event_date + INTERVAL '3 months'     AS add_3m,
    -- Next Monday after event_date:
    (event_date + (7 - EXTRACT(DOW FROM event_date) + 2) % 7 * INTERVAL '1 day') AS next_mon,
    -- Last day of month:
    DATE_TRUNC('month', event_date) + INTERVAL '1 month' - INTERVAL '1 day' AS last_day_m;""",
    )
    + """

"""
    + sub_section(
        "unix_timestamp / from_unixtime — Unix Epoch Conversion",
        [["event_ts", "epoch"]],
        [["event_ts", "epoch", "from_epoch", "to_ts"]],
        """from pyspark.sql.functions import unix_timestamp, from_unixtime, to_timestamp

df.select(
    "event_ts", "epoch",
    from_unixtime("epoch").alias("from_epoch"),
    to_timestamp(unix_timestamp("event_ts")).alias("to_ts")
).show()""",
        """SELECT
    event_ts,
    EXTRACT(EPOCH FROM event_ts) AS epoch,
    TO_TIMESTAMP(epoch)          AS from_epoch,
    TO_TIMESTAMP(EXTRACT(EPOCH FROM event_ts)) AS to_ts;""",
    )
    + """

"""
    + sub_section(
        "from_utc_timestamp / to_utc_timestamp — Timezone Conversion",
        [["utc_ts"]],
        [["utc_ts", "to_ny", "to_sg", "utc_converted"]],
        """from pyspark.sql.functions import from_utc_timestamp, to_utc_timestamp

df.select(
    "utc_ts",
    from_utc_timestamp("utc_ts", "America/New_York").alias("to_ny"),
    from_utc_timestamp("utc_ts", "Asia/Singapore").alias("to_sg"),
    to_utc_timestamp("utc_ts", "UTC").alias("utc_converted")
).show()""",
        """SELECT
    utc_ts,
    utc_ts AT TIME ZONE 'America/New_York' AS to_ny,
    utc_ts AT TIME ZONE 'Asia/Singapore'   AS to_sg,
    utc_ts AT TIME ZONE 'UTC'              AS utc_converted;""",
    )
    + """

"""
    + sub_section(
        "to_unix_timestamp / unix_date — Epoch as Integer",
        [["event_ts", "event_date"]],
        [["event_ts", "unix_ts", "unix_date"]],
        """from pyspark.sql.functions import unix_timestamp, unix_date

df.select(
    "event_ts", "event_date",
    unix_timestamp("event_ts").alias("unix_ts"),
    unix_date("event_date").alias("unix_date")
).show()""",
        """SELECT
    event_ts, event_date,
    EXTRACT(EPOCH FROM event_ts)::BIGINT  AS unix_ts,
    (event_date - DATE '1970-01-01')       AS unix_date;""",
    )
    + """

"""
    + sub_section(
        "make_date / make_timestamp — Construct Date/Timestamp",
        [["yr", "mo", "dy"]],
        [["yr", "mo", "dy", "made_date", "made_ts"]],
        """from pyspark.sql.functions import make_date, make_timestamp

df.select(
    "yr", "mo", "dy",
    make_date("yr", "mo", "dy").alias("made_date"),
    make_timestamp("yr", "mo", "dy", 14, 30, 0).alias("made_ts")
).show()""",
        """SELECT
    yr, mo, dy,
    MAKE_DATE(yr, mo, dy)                     AS made_date,
    MAKE_TIMESTAMP(yr, mo, dy, 14, 30, 0)   AS made_ts;""",
    )
    + """
    </section>"""
)

# ═══════════════════════════════════════════════════════════════════════════════
# 2. MATH FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
math_section = (
    """<section class="concept glass reveal" id="math">
      <h2>19) Math Functions</h2>
      <p>Spark's math functions are JVM-native and vectorized, making them far faster than Python UDFs. Use them for arithmetic, aggregation, rounding, trigonometry, and statistical transformations.</p>

"""
    + sub_section(
        "abs — Absolute Value",
        [["amount"]],
        [["amount", "amount_abs"]],
        """from pyspark.sql.functions import abs

df.select(abs("amount").alias("amount_abs")).show()""",
        """SELECT ABS(amount) AS amount_abs FROM df;""",
    )
    + """

"""
    + sub_section(
        "sqrt / pow / log / log10 / log2 — Powers and Logarithms",
        [["x"]],
        [["x", "x_sqrt", "x_pow2", "x_log", "x_log10"]],
        """from pyspark.sql.functions import sqrt, pow, log, log10, log2

df.select(
    "x",
    sqrt("x").alias("x_sqrt"),
    pow("x", 2).alias("x_pow2"),
    log("x").alias("x_log"),       -- natural log
    log10("x").alias("x_log10"),
    log2("x").alias("x_log2")
).show()""",
        """SELECT
    x,
    SQRT(x)    AS x_sqrt,
    POWER(x, 2) AS x_pow2,
    LN(x)      AS x_log,
    LOG(x)     AS x_log10,   -- LOG is base 10 in PG
    LOG(2, x)  AS x_log2
FROM df;""",
    )
    + """

"""
    + sub_section(
        "exp / expm1 / log1p — Exponential Functions",
        [["x"]],
        [["x", "x_exp", "x_expm1", "x_log1p"]],
        """from pyspark.sql.functions import exp, expm1, log1p

df.select(
    "x",
    exp("x").alias("x_exp"),
    expm1("x").alias("x_expm1"),  -- exp(x) - 1, numerically stable
    log1p("x").alias("x_log1p")   -- log(1 + x), numerically stable
).show()""",
        """SELECT
    x,
    EXP(x)    AS x_exp,
    EXP(x) - 1     AS x_expm1,
    LN(1 + x)     AS x_log1p
FROM df;""",
    )
    + """

"""
    + sub_section(
        "floor / ceil / round / bround — Rounding",
        [["value"]],
        [["value", "v_floor", "v_ceil", "v_round2", "v_bround2"]],
        """from pyspark.sql.functions import floor, ceil, round, bround

df.select(
    "value",
    floor("value").alias("v_floor"),
    ceil("value").alias("v_ceil"),
    round("value", 2).alias("v_round2"),   -- half-up rounding
    bround("value", 2).alias("v_bround2")  -- half-even (banker's rounding)
).show()""",
        """SELECT
    value,
    FLOOR(value)   AS v_floor,
    CEIL(value)    AS v_ceil,
    ROUND(value, 2)      AS v_round2,
    ROUND(value, 2)      AS v_bround2  -- PG uses half-up; banker's rounding via floor(x+0.5)
FROM df;""",
    )
    + """

"""
    + sub_section(
        "trunc — Truncate to Unit",
        [["value"]],
        [["value", "trunc_d", "trunc_m", "trunc_y"]],
        """from pyspark.sql.functions import trunc

df.select(
    "value",
    trunc("value", "day").alias("trunc_d"),
    trunc("value", "month").alias("trunc_m"),
    trunc("value", "year").alias("trunc_y")
).show()""",
        """SELECT
    value,
    DATE_TRUNC('day',   value) AS trunc_d,
    DATE_TRUNC('month',  value) AS trunc_m,
    DATE_TRUNC('year',   value) AS trunc_y
FROM df;""",
    )
    + """

"""
    + sub_section(
        "greatest / least — Max/Min Across Columns",
        [["a", "b", "c"]],
        [["a", "b", "c", "greatest", "least"]],
        """from pyspark.sql.functions import greatest, least

df.select(
    "a", "b", "c",
    greatest("a", "b", "c").alias("greatest"),
    least("a", "b", "c").alias("least")
).show()""",
        """SELECT
    a, b, c,
    GREATEST(a, b, c) AS greatest,
    LEAST(a, b, c)    AS least
FROM df;""",
    )
    + """

"""
    + sub_section(
        "signum / sign — Sign of Number",
        [["amount"]],
        [["amount", "sgn"]],
        """from pyspark.sql.functions import signum

df.select(
    signum("amount").alias("sgn")  -- -1 if <0, 0 if =0, 1 if >0
).show()""",
        """SELECT SIGN(amount) AS sgn FROM df;""",
    )
    + """

"""
    + sub_section(
        "mod / remainder — Modulo",
        [["a", "b"]],
        [["a", "b", "mod_result"]],
        """from pyspark.sql.functions import col, mod

df.select(
    mod("a", "b").alias("mod_result")
).show()""",
        """SELECT a % b AS mod_result FROM df;""",
    )
    + """

"""
    + sub_section(
        "cos / sin / tan / acos / asin / atan / atan2 — Trigonometry",
        [["angle_rad"]],
        [["angle_rad", "cos_v", "sin_v", "tan_v", "acos_v", "asin_v", "atan_v"]],
        """from pyspark.sql.functions import cos, sin, tan, acos, asin, atan, atan2

df.select(
    "angle_rad",
    cos("angle_rad").alias("cos_v"),
    sin("angle_rad").alias("sin_v"),
    tan("angle_rad").alias("tan_v"),
    acos("angle_rad").alias("acos_v"),
    asin("angle_rad").alias("asin_v"),
    atan("angle_rad").alias("atan_v")
).show()""",
        """SELECT
    angle_rad,
    COS(angle_rad)  AS cos_v,
    SIN(angle_rad)  AS sin_v,
    TAN(angle_rad)  AS tan_v,
    ACOS(angle_rad) AS acos_v,
    ASIN(angle_rad) AS asin_v,
    ATAN(angle_rad) AS atan_v
FROM df;""",
    )
    + """

"""
    + sub_section(
        "degrees / radians — Angle Conversion",
        [["angle_rad"]],
        [["angle_rad", "to_degrees", "to_radians"]],
        """from pyspark.sql.functions import degrees, radians

df.select(
    "angle_rad",
    degrees("angle_rad").alias("to_degrees"),
    radians(180.0).alias("pi_radians")  -- radians from degrees
).show()""",
        """SELECT
    angle_rad,
    DEGREES(angle_rad)   AS to_degrees,
    RADIANS(180.0)      AS pi_radians
FROM df;""",
    )
    + """

"""
    + sub_section(
        "cbrt — Cube Root",
        [["value"]],
        [["value", "cube_root"]],
        """from pyspark.sql.functions import cbrt

df.select(cbrt("value").alias("cube_root")).show()""",
        """SELECT POWER(value, 1.0/3.0) AS cube_root FROM df;""",
    )
    + """

"""
    + sub_section(
        "factorial — Factorial",
        [["n"]],
        [["n", "factorial_n"]],
        """from pyspark.sql.functions import factorial

df.select(factorial("n").alias("factorial_n")).show()""",
        """-- PostgreSQL has no built-in factorial; use a CASE or extension:
SELECT
    n,
    CASE n
        WHEN 0 THEN 1 WHEN 1 THEN 1 WHEN 2 THEN 2 WHEN 3 THEN 6
        WHEN 4 THEN 24 WHEN 5 THEN 120
    END AS factorial_n
FROM df;""",
    )
    + """

"""
    + sub_section(
        "bin / hex / unhex — Binary/Hexadecimal",
        [["n"]],
        [["n", "n_bin", "n_hex"]],
        """from pyspark.sql.functions import bin, hex

df.select(
    "n",
    bin("n").alias("n_bin"),   -- binary string
    hex("n").alias("n_hex")    -- hex string
).show()""",
        """SELECT
    n,
    SUBSTR(TO_HEX(n), 2) AS n_bin,  -- TO_HEX returns '0x...'
    TO_HEX(n)            AS n_hex
FROM df;""",
    )
    + """

"""
    + sub_section(
        "conv — Base Conversion",
        [["value"]],
        [["value", "base2", "base16", "back_to_10"]],
        """from pyspark.sql.functions import conv

df.select(
    "value",
    conv("value", 10, 2).alias("base2"),    -- 10 → base 2
    conv("value", 10, 16).alias("base16"),  -- 10 → base 16
    conv(conv("value", 10, 16), 16, 10).alias("back_to_10")
).show()""",
        """SELECT
    value,
    TO_HEX(value)        AS base16,  -- 10 → 16
    value::TEXT          AS back_to_10;""",
    )
    + """

"""
    + sub_section(
        "nanvl / isnan — NaN Handling",
        [["value"]],
        [["value", "nan_fixed", "is_nan"]],
        """from pyspark.sql.functions import nanvl, isnan

df.select(
    "value",
    nanvl("value", 0.0).alias("nan_fixed"),  -- replace NaN with 0.0
    isnan("value").alias("is_nan")
).show()""",
        """SELECT
    value,
    CASE WHEN value IS NULL THEN 0.0 ELSE value END AS nan_fixed,
    value IS NULL AS is_nan
FROM df;""",
    )
    + """

"""
    + sub_section(
        "width_bucket — Histogram Bucketing",
        [["amount"]],
        [["amount", "bucket_5", "bucket_10"]],
        """from pyspark.sql.functions import width_bucket

df.select(
    width_bucket("amount", 0, 1000, 5).alias("bucket_5"),   -- 5 equal-width buckets
    width_bucket("amount", 0, 1000, 10).alias("bucket_10")
).show()""",
        """SELECT
    WIDTH_BUCKET(amount, 0, 1000, 5)  AS bucket_5,
    WIDTH_BUCKET(amount, 0, 1000, 10) AS bucket_10
FROM df;""",
    )
    + """
    </section>"""
)

# ═══════════════════════════════════════════════════════════════════════════════
# 3. STRING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
string_section = (
    """<section class="concept glass reveal" id="string">
      <h2>20) String Functions</h2>
      <p>String functions are essential for data cleaning, normalization, and pattern extraction. Spark provides both SQL-standard functions and powerful regex capabilities.</p>

"""
    + sub_section(
        "upper / lower / initcap — Case Conversion",
        [["name"]],
        [["name", "upper_v", "lower_v", "initcap_v"]],
        """from pyspark.sql.functions import upper, lower, initcap

df.select(
    "name",
    upper("name").alias("upper_v"),
    lower("name").alias("lower_v"),
    initcap("name").alias("initcap_v")
).show()""",
        """SELECT
    name,
    UPPER(name)    AS upper_v,
    LOWER(name)    AS lower_v,
    INITCAP(name)  AS initcap_v
FROM df;""",
    )
    + """

"""
    + sub_section(
        "trim / ltrim / rtrim / strip — Whitespace Removal",
        [["raw_str"]],
        [["raw_str", "trim_v", "ltrim_v", "rtrim_v"]],
        """from pyspark.sql.functions import trim, ltrim, rtrim

df.select(
    "raw_str",
    trim("raw_str").alias("trim_v"),
    ltrim("raw_str").alias("ltrim_v"),
    rtrim("raw_str").alias("rtrim_v")
).show()""",
        """SELECT
    raw_str,
    TRIM(raw_str)   AS trim_v,
    LTRIM(raw_str)  AS ltrim_v,
    RTRIM(raw_str)  AS rtrim_v
FROM df;""",
    )
    + """

"""
    + sub_section(
        "lpad / rpad — Pad String to Width",
        [["code"]],
        [["code", "lpad_8", "rpad_8"]],
        """from pyspark.sql.functions import lpad, rpad

df.select(
    "code",
    lpad("code", 8, "0").alias("lpad_8"),
    rpad("code", 8, "-").alias("rpad_8")
).show()""",
        """SELECT
    code,
    LPAD(code, 8, '0') AS lpad_8,
    RPAD(code, 8, '-') AS rpad_8
FROM df;""",
    )
    + """

"""
    + sub_section(
        "concat_ws — Concatenate with Separator",
        [["first_name", "last_name", "region"]],
        [["first_name", "last_name", "region", "full_name", "region_name"]],
        """from pyspark.sql.functions import concat_ws

df.select(
    "first_name", "last_name", "region",
    concat_ws(" ", "first_name", "last_name").alias("full_name"),
    concat_ws("-", "region", "first_name").alias("region_name")
).show()""",
        """SELECT
    first_name, last_name, region,
    first_name || ' ' || last_name AS full_name,
    region      || '-' || first_name AS region_name
FROM df;""",
    )
    + """

"""
    + sub_section(
        "substring / substr — Extract Part of String",
        [["email"]],
        [["email", "local_part", "domain", "first_3"]],
        """from pyspark.sql.functions import substring, instr

df.select(
    "email",
    substring("email", 1, instr("email", "@") - 1).alias("local_part"),
    substring("email", instr("email", "@") + 1, 100).alias("domain"),
    substring("email", 1, 3).alias("first_3")
).show()""",
        """SELECT
    email,
    SPLIT_PART(email, '@', 1) AS local_part,
    SPLIT_PART(email, '@', 2) AS domain,
    SUBSTR(email, 1, 3)       AS first_3
FROM df;""",
    )
    + """

"""
    + sub_section(
        "split — Split String into Array",
        [["path"]],
        [["path", "parts", "part_0", "part_2"]],
        """from pyspark.sql.functions import split

df.select(
    "path",
    split("path", "/").alias("parts"),
    split("path", "/")[0].alias("part_0"),
    split("path", "/")[2].alias("part_2")
).show()""",
        """SELECT
    path,
    STRING_TO_ARRAY(path, '/')       AS parts,
    SPLIT_PART(path, '/', 1)       AS part_0,
    SPLIT_PART(path, '/', 3)        AS part_2
FROM df;""",
    )
    + """

"""
    + sub_section(
        "contains / instr / like / ilike — Search and Match",
        [["text", "email"]],
        [["text", "email", "has_pyspark", "email_domain", "starts_with"]],
        """from pyspark.sql.functions import col, contains, instr

df.select(
    "text", "email",
    contains("text", "Spark").alias("has_pyspark"),
    instr("email", "@company.com").alias("email_domain"),  -- position or 0
    col("email").like("%@company.com").alias("starts_with")
).show()""",
        """SELECT
    text, email,
    text    LIKE '%Spark%'     AS has_pyspark,
    POSITION('@company.com' IN email) AS email_domain,
    email   LIKE '%@company.com'      AS starts_with
FROM df;""",
    )
    + """

"""
    + sub_section(
        "startswith / endswith — Prefix/Suffix Match",
        [["product"]],
        [["product", "is_widget", "is_pro"]],
        """from pyspark.sql.functions import col

df.select(
    "product",
    col("product").startswith("Widget").alias("is_widget"),
    col("product").endswith("Pro").alias("is_pro")
).show()""",
        """SELECT
    product,
    product LIKE 'Widget%'  AS is_widget,
    product LIKE '%Pro'    AS is_pro
FROM df;""",
    )
    + """

"""
    + sub_section(
        "length / char_length / character_length — String Length",
        [["word"]],
        [["word", "len_v"]],
        """from pyspark.sql.functions import length

df.select(length("word").alias("len_v")).show()""",
        """SELECT LENGTH(word) AS len_v FROM df;""",
    )
    + """

"""
    + sub_section(
        "reverse — Reverse String",
        [["code"]],
        [["code", "reversed"]],
        """from pyspark.sql.functions import reverse

df.select(reverse("code").alias("reversed")).show()""",
        """SELECT REVERSE(code) AS reversed FROM df;""",
    )
    + """

"""
    + sub_section(
        "repeat — Repeat String N Times",
        [["char", "n"]],
        [["char", "n", "repeated"]],
        """from pyspark.sql.functions import repeat

df.select(
    repeat("char", 3).alias("repeated")
).show()""",
        """SELECT REPEAT(char, 3) AS repeated FROM df;""",
    )
    + """

"""
    + sub_section(
        "translate — Character-by-Character Replacement",
        [["raw"]],
        [["raw", "translated"]],
        """from pyspark.sql.functions import translate

-- Replace a→x, e→y, i→z
df.select(
    translate("raw", "aei", "xyz").alias("translated")
).show()""",
        """SELECT
    TRANSLATE(raw, 'aei', 'xyz') AS translated
FROM df;""",
    )
    + """

"""
    + sub_section(
        "overlay — Replace Portion of String",
        [["text"]],
        [["text", "overlay_v"]],
        """from pyspark.sql.functions import overlay

-- Replace 3 chars starting at position 5 with "XXX"
df.select(
    overlay("text", "XXX", 5, 3).alias("overlay_v")
).show()""",
        """SELECT
    OVERLAY(text PLACING 'XXX' FROM 5 FOR 3) AS overlay_v
FROM df;""",
    )
    + """

"""
    + sub_section(
        "regexp_extract — Extract with Regex Groups",
        [["log_line"]],
        [["log_line", "level", "component", "msg"]],
        """from pyspark.sql.functions import regexp_extract

df.select(
    regexp_extract("log_line", r"\\[(\\w+)\\]", 1).alias("level"),
    regexp_extract("log_line", r"\\{(\\w+)\\}", 1).alias("component"),
    regexp_extract("log_line", r": (.+)$", 1).alias("msg")
).show()""",
        """SELECT
    (REGEXP_MATCHES(log_line, '\\[(\\w+)\\]'))[1] AS level,
    (REGEXP_MATCHES(log_line, '\\{(\\w+)\\}') )[1] AS component,
    (REGEXP_MATCHES(log_line, ': (.+)$'))[1]        AS msg
FROM df;""",
    )
    + """

"""
    + sub_section(
        "regexp_replace — Replace with Regex",
        [["text"]],
        [["text", "cleaned", "digits_only"]],
        """from pyspark.sql.functions import regexp_replace

df.select(
    "text",
    regexp_replace("text", r"[^a-zA-Z0-9 ]", "").alias("cleaned"),
    regexp_replace("text", r"\\D", "").alias("digits_only")
).show()""",
        """SELECT
    text,
    REGEXP_REPLACE(text, '[^a-zA-Z0-9 ]', '') AS cleaned,
    REGEXP_REPLACE(text, '\\D', '')            AS digits_only
FROM df;""",
    )
    + """

"""
    + sub_section(
        "rlike / regexp — Full Regex Match",
        [["email"]],
        [["email", "is_corp", "is_dev"]],
        """from pyspark.sql.functions import col

df.select(
    "email",
    col("email").rlike(r"^[a-z]+@company\\.com$").alias("is_corp"),
    col("email").rlike(r"^[a-z]+@(dev|test)\\.io$").alias("is_dev")
).show()""",
        """SELECT
    email,
    email ~ '^[a-z]+@company\\.com$'      AS is_corp,
    email ~ '^[a-z]+@(dev|test)\\.io$'   AS is_dev
FROM df;""",
    )
    + """

"""
    + sub_section(
        "locate / position — Find Substring Position",
        [["text", "sub"]],
        [["text", "sub", "pos_v"]],
        """from pyspark.sql.functions import locate

df.select(
    locate("sub", "text", 1).alias("pos_v")  -- 0 if not found
).show()""",
        """SELECT POSITION(sub IN text) AS pos_v FROM df;""",
    )
    + """

"""
    + sub_section(
        "soundex / levenshtein — Fuzzy Matching",
        [["name1", "name2"]],
        [["name1", "name2", "sdx1", "sdx2", "lev_dist"]],
        """from pyspark.sql.functions import soundex, levenshtein

df.select(
    "name1", "name2",
    soundex("name1").alias("sdx1"),
    soundex("name2").alias("sdx2"),
    levenshtein("name1", "name2").alias("lev_dist")
).show()""",
        """SELECT
    name1, name2,
    SOUNDEX(name1) AS sdx1,
    SOUNDEX(name2) AS sdx2,
    -- Levenshtein: use extension or implement manually
    1  AS lev_dist  -- PG has no built-in; use fuzzy extension
FROM df;""",
    )
    + """

"""
    + sub_section(
        "ascii / chr — Character Code Conversion",
        [["char_v", "code"]],
        [["char_v", "code", "ascii_v", "chr_v"]],
        """from pyspark.sql.functions import ascii, chr

df.select(
    "char_v", "code",
    ascii("char_v").alias("ascii_v"),
    chr("code").alias("chr_v")
).show()""",
        """SELECT
    char_v, code,
    ASCII(char_v)  AS ascii_v,
    CHR(code)      AS chr_v
FROM df;""",
    )
    + """

"""
    + sub_section(
        "format_string / printf — String Formatting",
        [["name", "score"]],
        [["name", "score", "formatted"]],
        """from pyspark.sql.functions import format_string

df.select(
    format_string("%s scored %d", "name", "score").alias("formatted")
).show()""",
        """SELECT
    FORMAT('%s scored %d', name, score) AS formatted
FROM df;""",
    )
    + """
    </section>"""
)

# ═══════════════════════════════════════════════════════════════════════════════
# 4. WINDOW FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
window_section = (
    """<section class="concept glass reveal" id="window">
      <h2>21) Window Functions</h2>
      <p>Window functions compute row-level analytics without collapsing rows. They operate on a frame of rows relative to the current row. Use <code>partitionBy()</code> to define groups and <code>orderBy()</code> to define row ordering within each partition.</p>

"""
    + sub_section(
        "Window Definition — partitionBy + orderBy",
        [["region", "amount"]],
        [["region", "amount", "w_def"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import sum as Fsum

w = (Window
    .partitionBy("region")
    .orderBy("amount"))

df.withColumn("running_sum", Fsum("amount").over(w)).show()""",
        """SELECT
    region, amount,
    SUM(amount) OVER (PARTITION BY region ORDER BY amount) AS running_sum
FROM df;""",
    )
    + """

"""
    + sub_section(
        "row_number — Sequential Row Number (No Gaps)",
        [["region", "amount"]],
        [["region", "amount", "row_num"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import row_number

w = Window.partitionBy("region").orderBy("amount")

df.withColumn("row_num", row_number().over(w)).show()""",
        """SELECT
    region, amount,
    ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount) AS row_num
FROM df;""",
    )
    + """

"""
    + sub_section(
        "rank — Rank with Gaps (1, 2, 2, 4)",
        [["region", "amount"]],
        [["region", "amount", "rank_v"]],
        """from pyspark.sql.functions import rank

w = Window.partitionBy("region").orderBy("amount")

df.withColumn("rank_v", rank().over(w)).show()""",
        """SELECT
    region, amount,
    RANK() OVER (PARTITION BY region ORDER BY amount) AS rank_v
FROM df;""",
    )
    + """

"""
    + sub_section(
        "dense_rank — Rank Without Gaps (1, 2, 2, 3)",
        [["region", "amount"]],
        [["region", "amount", "dense_rank_v"]],
        """from pyspark.sql.functions import dense_rank

w = Window.partitionBy("region").orderBy("amount")

df.withColumn("dense_rank_v", dense_rank().over(w)).show()""",
        """SELECT
    region, amount,
    DENSE_RANK() OVER (PARTITION BY region ORDER BY amount) AS dense_rank_v
FROM df;""",
    )
    + """

"""
    + sub_section(
        "percent_rank — Percentile Rank (0.0 to 1.0)",
        [["region", "amount"]],
        [["region", "amount", "pct_rank"]],
        """from pyspark.sql.functions import percent_rank

w = Window.partitionBy("region").orderBy("amount")

df.withColumn("pct_rank", percent_rank().over(w)).show()""",
        """SELECT
    region, amount,
    PERCENT_RANK() OVER (PARTITION BY region ORDER BY amount) AS pct_rank
FROM df;""",
    )
    + """

"""
    + sub_section(
        "ntile — Divide Rows into N Buckets",
        [["region", "amount"]],
        [["region", "amount", "quartile", "tercile"]],
        """from pyspark.sql.functions import ntile

w = Window.partitionBy("region").orderBy("amount")

df.select(
    "region", "amount",
    ntile(4).over(w).alias("quartile"),
    ntile(3).over(w).alias("tercile")
).show()""",
        """SELECT
    region, amount,
    NTILE(4) OVER (PARTITION BY region ORDER BY amount) AS quartile,
    NTILE(3) OVER (PARTITION BY region ORDER BY amount) AS tercile
FROM df;""",
    )
    + """

"""
    + sub_section(
        "first_value / last_value — First/Last in Window Frame",
        [["region", "amount"]],
        [
            [
                "region",
                "amount",
                "first_v",
                "last_v",
                "first_ignorenull",
                "last_ignorenull",
            ]
        ],
        """from pyspark.sql import Window
from pyspark.sql.functions import first, last

w = Window.partitionBy("region").orderBy("amount")

df.select(
    "region", "amount",
    first("amount").over(w).alias("first_v"),
    last("amount").over(w).alias("last_v"),
    first("amount", ignorNulls=True).over(w).alias("first_ignorenull"),
    last("amount", ignorNulls=True).over(w).alias("last_ignorenull")
).show()""",
        """SELECT
    region, amount,
    FIRST_VALUE(amount) OVER w AS first_v,
    LAST_VALUE(amount)  OVER w AS last_v,
    FIRST_VALUE(amount IGNORE NULLS) OVER w AS first_ignorenull,
    LAST_VALUE(amount  IGNORE NULLS) OVER w AS last_ignorenull
FROM df
WINDOW w AS (PARTITION BY region ORDER BY amount);""",
    )
    + """

"""
    + sub_section(
        "nth_value — Nth Value in Window Frame",
        [["region", "amount"]],
        [["region", "amount", "3rd_value", "2nd_ignorenull"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import nth_value

w = Window.partitionBy("region").orderBy("amount")

df.select(
    "region", "amount",
    nth_value("amount", 3).over(w).alias("3rd_value"),
    nth_value("amount", 2, True).over(w).alias("2nd_ignorenull")
).show()""",
        """SELECT
    region, amount,
    NTH_VALUE(amount, 3) OVER w AS 3rd_value
FROM df
WINDOW w AS (PARTITION BY region ORDER BY amount);""",
    )
    + """

"""
    + sub_section(
        "lag / lead — Previous/Next Row Value",
        [["event_time", "amount"]],
        [["event_time", "amount", "prev_amt", "next_amt", "prev_2"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import lag, lead

w = Window.partitionBy("region").orderBy("event_time")

df.select(
    "event_time", "amount",
    lag("amount", 1).over(w).alias("prev_amt"),
    lead("amount", 1).over(w).alias("next_amt"),
    lag("amount", 2, 0.0).over(w).alias("prev_2")  -- default 0.0
).show()""",
        """SELECT
    event_time, amount,
    LAG(amount, 1)        OVER w AS prev_amt,
    LEAD(amount, 1)      OVER w AS next_amt,
    LAG(amount, 2, 0.0) OVER w AS prev_2
FROM df
WINDOW w AS (PARTITION BY region ORDER BY event_time);""",
    )
    + """

"""
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
        """from pyspark.sql import Window
from pyspark.sql.functions import sum as Fsum, avg, count, min as Fmin, max as Fmax

w = Window.partitionBy("region").orderBy("amount")

df.select(
    "region", "amount",
    Fsum("amount").over(w).alias("running_sum"),
    avg("amount").over(w).alias("running_avg"),
    count("amount").over(w).alias("running_count"),
    Fmin("amount").over(w).alias("running_min"),
    Fmax("amount").over(w).alias("running_max")
).show()""",
        """SELECT
    region, amount,
    SUM(amount) OVER w AS running_sum,
    AVG(amount) OVER w AS running_avg,
    COUNT(amount) OVER w AS running_count,
    MIN(amount) OVER w AS running_min,
    MAX(amount) OVER w AS running_max
FROM df
WINDOW w AS (PARTITION BY region ORDER BY amount);""",
    )
    + """

"""
    + sub_section(
        "cume_dist — Cumulative Distribution",
        [["region", "amount"]],
        [["region", "amount", "cume_dist_v"]],
        """from pyspark.sql.functions import cume_dist

w = Window.partitionBy("region").orderBy("amount")

df.withColumn("cume_dist_v", cume_dist().over(w)).show()""",
        """SELECT
    region, amount,
    CUME_DIST() OVER (PARTITION BY region ORDER BY amount) AS cume_dist_v
FROM df;""",
    )
    + """

"""
    + sub_section(
        "collect_list / collect_set — Collect Values as List/Set",
        [["region", "product"]],
        [["region", "product", "all_products", "unique_products"]],
        """from pyspark.sql.functions import collect_list, collect_set

w = Window.partitionBy("region")

df.select(
    "region",
    collect_list("product").over(w).alias("all_products"),
    collect_set("product").over(w).alias("unique_products")
).distinct().show()""",
        """SELECT
    region,
    ARRAY_AGG(product)       OVER w AS all_products,
    ARRAY_AGG(DISTINCT product) OVER w AS unique_products
FROM df
WINDOW w AS (PARTITION BY region);""",
    )
    + """
    </section>"""
)

# ═══════════════════════════════════════════════════════════════════════════════
# 5. ROWS BETWEEN — FULL FRAME EXPLANATION
# ═══════════════════════════════════════════════════════════════════════════════
rows_section = (
    """<section class="concept glass reveal" id="rows-between">
      <h2>23) Rows Between — Window Frame Boundaries</h2>
      <p><code>rowsBetween(start, end)</code> defines the frame of rows relative to the current row for aggregate window functions. The frame slides with each row. By default, aggregate functions use <code>RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW</code>.</p>

"""
    + sub_section(
        "Window.unboundedPreceding — All Rows Before Current",
        [["region", "event_time", "amount"]],
        [["event_time", "amount", "cumulative_sum", "cumulative_count"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import sum as Fsum, count

w_all = (Window
    .partitionBy("region")
    .orderBy("event_time")
    .rowsBetween(Window.unboundedPreceding, Window.currentRow))

df.select(
    "event_time", "amount",
    Fsum("amount").over(w_all).alias("cumulative_sum"),
    count("amount").over(w_all).alias("cumulative_count")
).show()""",
        """SELECT
    event_time, amount,
    SUM(amount)  OVER w AS cumulative_sum,
    COUNT(amount) OVER w AS cumulative_count
FROM df
WINDOW w AS (
    PARTITION BY region
    ORDER BY event_time
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
);""",
    )
    + """

"""
    + sub_section(
        "Window.unboundedFollowing — All Rows After Current",
        [["region", "event_time", "amount"]],
        [["event_time", "amount", "reverse_sum"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import sum as Fsum

w_rev = (Window
    .partitionBy("region")
    .orderBy("event_time")
    .rowsBetween(Window.currentRow, Window.unboundedFollowing))

df.select(
    "event_time", "amount",
    Fsum("amount").over(w_rev).alias("reverse_sum")
).show()""",
        """SELECT
    event_time, amount,
    SUM(amount) OVER w AS reverse_sum
FROM df
WINDOW w AS (
    PARTITION BY region
    ORDER BY event_time
    ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
);""",
    )
    + """

"""
    + sub_section(
        "rowsBetween(N, M) — Fixed Frame Size",
        [["event_time", "amount"]],
        [["event_time", "amount", "sum_3_back", "sum_prev_next", "avg_2_ahead"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import sum as Fsum, avg

w_3back = Window.orderBy("event_time").rowsBetween(-3, 0)
w_around = Window.orderBy("event_time").rowsBetween(-1, 1)
w_2ahead = Window.orderBy("event_time").rowsBetween(0, 2)

df.select(
    "event_time", "amount",
    Fsum("amount").over(w_3back).alias("sum_3_back"),
    Fsum("amount").over(w_around).alias("sum_prev_next"),
    avg("amount").over(w_2ahead).alias("avg_2_ahead")
).show()""",
        """SELECT
    event_time, amount,
    SUM(amount) OVER (ORDER BY event_time ROWS BETWEEN 3 PRECEDING AND CURRENT ROW)  AS sum_3_back,
    SUM(amount) OVER (ORDER BY event_time ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS sum_prev_next,
    AVG(amount) OVER (ORDER BY event_time ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING) AS avg_2_ahead
FROM df;""",
    )
    + """

"""
    + sub_section(
        "rowsBetween(0, 0) — Current Row Only",
        [["event_time", "amount"]],
        [["event_time", "amount", "same_as_amount"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import sum as Fsum

w_curr = Window.orderBy("event_time").rowsBetween(0, 0)

df.select(
    "event_time", "amount",
    Fsum("amount").over(w_curr).alias("same_as_amount")
).show()""",
        """SELECT
    event_time, amount,
    SUM(amount) OVER (
        ORDER BY event_time
        ROWS BETWEEN CURRENT ROW AND CURRENT ROW
    ) AS same_as_amount
FROM df;""",
    )
    + """

"""
    + sub_section(
        "rangeBetween vs rowsBetween — RANGE Uses Value, ROWS Uses Position",
        [["region", "ts", "amount"]],
        [["ts", "amount", "sum_rows_2", "sum_range_2"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import sum as Fsum

# ROWS: includes 2 rows before regardless of value
w_rows = Window.partitionBy("region").orderBy("ts").rowsBetween(-2, 0)
# RANGE: includes rows where key <= current key + 2 (in same partition)
w_range = Window.partitionBy("region").orderBy("ts").rangeBetween(-2, 0)

df.select(
    "ts", "amount",
    Fsum("amount").over(w_rows).alias("sum_rows_2"),
    Fsum("amount").over(w_range).alias("sum_range_2")
).show()""",
        """-- PostgreSQL ROWS vs RANGE:
-- PostgreSQL uses ROWS mode by default.
-- RANGE with offset is supported:
SELECT
    ts, amount,
    SUM(amount) OVER (
        PARTITION BY region
        ORDER BY ts
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS sum_rows_2,
    SUM(amount) OVER (
        PARTITION BY region
        ORDER BY ts
        RANGE BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS sum_range_2
FROM df;""",
    )
    + """

"""
    + sub_section(
        "First/Last in Frame — first/last with Frame",
        [["region", "event_time", "amount"]],
        [["event_time", "amount", "first_in_frame", "last_in_frame"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import first, last

# Within a sliding window, first() returns first row of the frame
w_frame = (Window
    .partitionBy("region")
    .orderBy("event_time")
    .rowsBetween(-2, 0))

df.select(
    "event_time", "amount",
    first("amount").over(w_frame).alias("first_in_frame"),
    last("amount").over(w_frame).alias("last_in_frame")
).show()""",
        """SELECT
    event_time, amount,
    FIRST_VALUE(amount) OVER w AS first_in_frame,
    LAST_VALUE(amount)  OVER w AS last_in_frame
FROM df
WINDOW w AS (
    PARTITION BY region
    ORDER BY event_time
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
);""",
    )
    + """

"""
    + sub_section(
        "Running Total, Moving Average, Moving Count",
        [["region", "event_time", "amount"]],
        [["event_time", "amount", "running_total", "moving_avg_3", "moving_count_5"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import sum as Fsum, avg, count

w_total = Window.partitionBy("region").orderBy("event_time").rowsBetween(Window.unboundedPreceding, Window.currentRow)
w_avg3  = Window.partitionBy("region").orderBy("event_time").rowsBetween(-2, 0)
w_cnt5  = Window.partitionBy("region").orderBy("event_time").rowsBetween(-4, 0)

df.select(
    "event_time", "amount",
    Fsum("amount").over(w_total).alias("running_total"),
    avg("amount").over(w_avg3).alias("moving_avg_3"),
    count("amount").over(w_cnt5).alias("moving_count_5")
).show()""",
        """SELECT
    event_time, amount,
    SUM(amount)  OVER w_total AS running_total,
    AVG(amount)  OVER w_avg3  AS moving_avg_3,
    COUNT(amount) OVER w_cnt5 AS moving_count_5
FROM df
WINDOW
    w_total AS (PARTITION BY region ORDER BY event_time ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW),
    w_avg3  AS (PARTITION BY region ORDER BY event_time ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),
    w_cnt5  AS (PARTITION BY region ORDER BY event_time ROWS BETWEEN 4 PRECEDING AND CURRENT ROW);""",
    )
    + """

"""
    + sub_section(
        "Rank Within Frame — nth_value in Sliding Window",
        [["region", "event_time", "amount"]],
        [["event_time", "amount", "first_amt", "2nd_amt", "last_amt"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import nth_value

w_3 = Window.partitionBy("region").orderBy("event_time").rowsBetween(0, 2)

df.select(
    "event_time", "amount",
    nth_value("amount", 1).over(w_3).alias("first_amt"),
    nth_value("amount", 2).over(w_3).alias("2nd_amt"),
    nth_value("amount", 3).over(w_3).alias("last_amt")
).show()""",
        """SELECT
    event_time, amount,
    FIRST_VALUE(amount) OVER w AS first_amt,
    NTH_VALUE(amount, 2) OVER w AS 2nd_amt,
    LAST_VALUE(amount)  OVER w AS last_amt
FROM df
WINDOW w AS (
    PARTITION BY region
    ORDER BY event_time
    ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING
);""",
    )
    + """

"""
    + sub_section(
        "Lag/Lead with Frame Offset",
        [["region", "event_time", "amount"]],
        [["event_time", "amount", "lag_1", "lag_2", "lead_1"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import lag, lead

w = Window.partitionBy("region").orderBy("event_time")

df.select(
    "event_time", "amount",
    lag("amount", 1).over(w).alias("lag_1"),
    lag("amount", 2).over(w).alias("lag_2"),
    lead("amount", 1).over(w).alias("lead_1")
).show()""",
        """SELECT
    event_time, amount,
    LAG(amount, 1)  OVER w AS lag_1,
    LAG(amount, 2)  OVER w AS lag_2,
    LEAD(amount, 1) OVER w AS lead_1
FROM df
WINDOW w AS (PARTITION BY region ORDER BY event_time);""",
    )
    + """
    </section>"""
)

# ═══════════════════════════════════════════════════════════════════════════════
# LEAD AND LAG (Standalone section, expanded)
# ═══════════════════════════════════════════════════════════════════════════════
leadlag_section = (
    """<section class="concept glass reveal" id="lead-lag">
      <h2>22) Lead and Lag</h2>
      <p><code>lag(col, n, default)</code> returns the value from n rows before the current row. <code>lead(col, n, default)</code> returns the value from n rows after the current row. Both are essential for time-series comparisons and period-over-period analysis.</p>

"""
    + sub_section(
        "lag — Previous Row Value",
        [["event_time", "amount"]],
        [["event_time", "amount", "prev_amount", "prev_2"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import lag

w = Window.partitionBy("region").orderBy("event_time")

df.select(
    "event_time", "amount",
    lag("amount", 1).over(w).alias("prev_amount"),
    lag("amount", 2).over(w).alias("prev_2")  -- default null if unavailable
).show()""",
        """SELECT
    event_time, amount,
    LAG(amount, 1) OVER w AS prev_amount,
    LAG(amount, 2) OVER w AS prev_2
FROM df
WINDOW w AS (PARTITION BY region ORDER BY event_time);""",
    )
    + """

"""
    + sub_section(
        "lead — Next Row Value",
        [["event_time", "amount"]],
        [["event_time", "amount", "next_amount", "next_2"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import lead

w = Window.partitionBy("region").orderBy("event_time")

df.select(
    "event_time", "amount",
    lead("amount", 1).over(w).alias("next_amount"),
    lead("amount", 2).over(w).alias("next_2")
).show()""",
        """SELECT
    event_time, amount,
    LEAD(amount, 1) OVER w AS next_amount,
    LEAD(amount, 2) OVER w AS next_2
FROM df
WINDOW w AS (PARTITION BY region ORDER BY event_time);""",
    )
    + """

"""
    + sub_section(
        "lag / lead with Default Value",
        [["event_time", "amount"]],
        [["event_time", "amount", "prev_amt", "next_amt", "prev_2_0"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import lag, lead, coalesce, lit

w = Window.partitionBy("region").orderBy("event_time")

df.select(
    "event_time", "amount",
    lag("amount", 1).over(w).alias("prev_amt"),
    lead("amount", 1).over(w).alias("next_amt"),
    coalesce(lag("amount", 2).over(w), lit(0.0)).alias("prev_2_0")  -- default 0
).show()""",
        """SELECT
    event_time, amount,
    LAG(amount, 1, 0) OVER w  AS prev_amt,
    LEAD(amount, 1, 0) OVER w  AS next_amt,
    COALESCE(LAG(amount, 2) OVER w, 0) AS prev_2_0
FROM df
WINDOW w AS (PARTITION BY region ORDER BY event_time);""",
    )
    + """

"""
    + sub_section(
        "Period-over-Period Change with lag",
        [["region", "event_time", "amount"]],
        [["event_time", "amount", "prev_amount", "amount_change", "pct_change"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import lag, coalesce, lit, round as Fround

w = Window.partitionBy("region").orderBy("event_time")

result = df.withColumn("prev_amount",
    lag("amount", 1).over(w))
result = result.withColumn("amount_change",
    result["amount"] - result["prev_amount"])
result = result.withColumn("pct_change",
    Fround((result["amount"] - result["prev_amount"]) / result["prev_amount"] * 100, 2))

result.show()""",
        """SELECT
    event_time, amount,
    LAG(amount, 1) OVER w AS prev_amount,
    amount - LAG(amount, 1) OVER w AS amount_change,
    ROUND((amount - LAG(amount, 1) OVER w) / NULLIF(LAG(amount, 1) OVER w, 0) * 100, 2) AS pct_change
FROM df
WINDOW w AS (PARTITION BY region ORDER BY event_time);""",
    )
    + """

"""
    + sub_section(
        "Streak / Gap Detection with lag",
        [["region", "event_time", "status"]],
        [["event_time", "status", "prev_status", "status_changed"]],
        """from pyspark.sql import Window
from pyspark.sql.functions import lag, when

w = Window.partitionBy("region").orderBy("event_time")

df.select(
    "event_time", "status",
    lag("status", 1).over(w).alias("prev_status"),
    when(lag("status", 1).over(w) != "status", lit(True)).otherwise(lit(False)).alias("status_changed")
).show()""",
        """SELECT
    event_time, status,
    LAG(status, 1) OVER w AS prev_status,
    LAG(status, 1) OVER w IS DISTINCT FROM status AS status_changed
FROM df
WINDOW w AS (PARTITION BY region ORDER BY event_time);""",
    )
    + """
    </section>"""
)

# ═══════════════════════════════════════════════════════════════════════════════
# REPLACE ALL SECTIONS IN CONTENT
# ═══════════════════════════════════════════════════════════════════════════════
# Find each section by id and replace

sections = [
    ("datetime", datetime_section),
    ("math", math_section),
    ("string", string_section),
    ("window", window_section),
    ("lead-lag", leadlag_section),
    ("rows-between", rows_section),
]

for sid, section_html in sections:
    # Find the section
    start_pat = f'<section class="concept glass reveal" id="{sid}"'
    alt_pat = f'<section class="concept glass" id="{sid}"'

    idx_start = content.find(start_pat)
    if idx_start == -1:
        idx_start = content.find(alt_pat)

    if idx_start == -1:
        print(f"WARNING: Could not find section {sid}")
        continue

    # Find the end </section>
    idx_end = content.find("</section>", idx_start) + len("</section>")

    # Check for nested sections
    next_section_idx = content.find("<section", idx_end)
    next_close_idx = content.find("</section>", idx_end)

    # If there's another section opening before the next closing, we have nesting issues
    if next_section_idx != -1 and next_section_idx < next_close_idx:
        # Find the matching close for the inner section
        inner_start = content.find("<section", idx_end)
        inner_end = content.find("</section>", inner_start) + len("</section>")
        # Check if this inner section closes before any other section opens
        while True:
            next_open = content.find("<section", inner_end)
            next_close = content.find("</section>", inner_end)
            if next_open == -1 or next_open > next_close:
                break
            inner_end = next_close + len("</section>")
        idx_end = inner_end

    content = content[:idx_start] + section_html + content[idx_end:]
    print(f"Replaced {sid}")

with open("spark/pyspark-code-guide.html", "w", encoding="utf-8") as f:
    f.write(content)

lines = content.count("\n")
print(f"Done! ~{lines} lines")

# Validate
import re

tags = ["div", "section", "pre", "table", "svg"]
for tag in tags:
    opens = len(re.findall(rf"<{tag}[\s>]", content))
    closes = len(re.findall(rf"</{tag}>", content))
    ok = "OK" if opens == closes else "MISMATCH"
    print(f"  {tag}: {opens}/{closes} {ok}")
