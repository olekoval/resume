import os
import sys
from pathlib import Path
import polars as pl
from dotenv import load_dotenv

from rich.console import Console
console = Console()

# Прибираємо сповіщення від Arrow/ADBC -
os.environ["POLARS_UNKNOWN_EXTENSION_TYPE_BEHAVIOR"] = "load_as_storage"

BASE_DIR = Path(__file__).resolve().parents[2]
out_dir = BASE_DIR / "data" / "packet_21" / "packet_21.parquet"

dotenv_path = BASE_DIR/ "scripts" / "env" / ".env"
load_dotenv(dotenv_path=dotenv_path)

db_url = os.getenv("DB_URL")
if not db_url:
    raise ValueError("DB_URL не задано в .env")
    
# ⚡⚡⚡ якщо використовується поле з типом даних uuid, то обов'язково його конвертувати ::text ⚡⚡⚡
query= """
WITH dicts AS (
    SELECT 
        v.code, 
        v.description, 
        d.kwd_name
    FROM core.dim_rpt_dictionary_values AS v
    INNER JOIN core.dim_rpt_dictionaries AS d ON v.dictionary_id = d.id
    WHERE v.is_current = 'Y' 
      AND d.is_current = 'Y'
      AND d.kwd_name = 'eHealth/ICD10_AM/condition_codes'
)  
          
SELECT
       v.residence_area,
       e.edrpou,
       e.patient_id::text AS patient_id,
       e.age_years,
       e.event_id::text AS event_id,
       e.episode_id ::text AS episode_id,
       e.class,
       CONCAT (e.principal_diagnosis, ' - ', pd.description) AS principal_diagnosis
  FROM analytics.rds_pmg_events_analytics AS e
           LEFT JOIN dicts AS pd ON e.principal_diagnosis = pd.code 
           LEFT JOIN analytics.dwh_legal_entities_edrpou_view AS v ON v.edrpou = e.edrpou
 WHERE e.report_year = 2026
   AND e.is_correct
   AND e.packet_number = '21'
   AND e.principal_diagnosis != 'Z21'

"""

console.print(
    "🚀 ... Запуск процесу зчитування даних через Polars",
    style="bright_blue"
)
try:
    df  = pl.read_database_uri(
        query=query,
        uri=db_url,
        engine="adbc"
    )
    console.print(
        f"✅ 'завантажено: {df.shape[0]} рядків.",
        style="bold green"
    )
except Exception as e:
    console.print(
        f"❌ ... Помилка у запиті '{e}",
        style="bold bright_red"
    )

# ------------------------------ Запуск на виконання ------------------------------
if __name__ == "__main__":
    if df is not None and not df.is_empty():
        df.write_parquet(out_dir)
        console.print(f"💾 Збережено: {out_dir} ({df.shape[0]} рядків)", style="bold green")
    print(df)


