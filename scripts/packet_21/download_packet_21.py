import os
import sys
from pathlib import Path
import polars as pl
from dotenv import load_dotenv
from rich.console import Console


console = Console()

os.environ["POLARS_UNKNOWN_EXTENSION_TYPE_BEHAVIOR"] = "load_as_storage"

BASE_DIR = Path(__file__).resolve().parents[2]
out_dir = BASE_DIR / "data" / "packet_21" / "dataset.parquet"

# Columns to convert to Categorical dtype 
CATEGORICAL_COLS = [
    "residence_area",
    "edrpou"
]

UInt_COLS = [
    "age_years",
    "report_month"
]

dotenv_path = BASE_DIR / "scripts" / "env" / ".env"
load_dotenv(dotenv_path=dotenv_path)

db_url = os.getenv("DB_URL")
if not db_url:
    raise ValueError("Missing DB_URL in .env")

query = """
SELECT
       v.residence_area,
       e.edrpou,
       e.patient_id::text AS patient_id,
       e.age_years,
       e.event_id::text AS event_id,
       e.report_month
  FROM analytics.rds_pmg_events_analytics AS e
       LEFT JOIN analytics.dwh_legal_entities_edrpou_view AS v ON v.edrpou = e.edrpou
 WHERE e.report_year = 2026
   AND e.is_correct
   AND e.packet_number = '21'
   AND e.class = 'AMB'
   AND e.principal_diagnosis = 'B20'
"""

console.print(
    "🚀 ... Start reading data with Polars",
    style="bright_blue"
)

df = None
try:
    df = pl.read_database_uri(
        query=query,
        uri=db_url,
        engine="adbc"
    )
    console.print(
        f"✅ Loaded: {df.shape[0]} rows.",
        style="bold green"
    )
except Exception as e:
    console.print(
        f"❌ ... Query error: '{e}",
        style="bold bright_red"
    )

    
try:
    df = df.with_columns(
        pl.col(CATEGORICAL_COLS).cast(pl.Categorical),
        pl.col(UInt_COLS).cast(pl.UInt8),
    )
    console.print(
        f"🏷️ Cast to Categorical: {', '.join(CATEGORICAL_COLS)} | UInt8: {', '.join(UInt_COLS)}",
        style="bold green",
    )
except Exception as e:
    console.print(
        f"❌ ... Cast error: '{e}'",
        style="bold bright_red",
    )
# ------------------------------ Run execution ------------------------------
if __name__ == "__main__":
    if df is not None and not df.is_empty():
        out_dir.parent.mkdir(parents=True, exist_ok=True)
        df.write_parquet(out_dir)
        console.print(f"💾 Saved: {out_dir} ({df.shape[0]} rows)", style="bold green")
        console.print(f"📦 In memory: {df.estimated_size('mb'):.1f} MB", style="bright_blue")
        print(df)
