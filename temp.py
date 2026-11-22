from pathlib import Path
import polars as pl


def print_unique_values(file_path: Path, column_name: str, limit: int | None = None) -> None:
    """Читає Parquet-файл та виводить у консоль унікальні значення вказаної колонки."""
    if not file_path.exists():
        raise FileNotFoundError(f"Файл не знайдено: {file_path}")

    # Lazy-читання: Polars завантажить лише потрібну колонку з метаданих/сторінків файлу
    lazy_series = (
        pl.scan_parquet(file_path)
        .select(pl.col(column_name).drop_nulls().unique().sort())
        .collect()
        .get_column(column_name)
    )

    total_unique = lazy_series.len()
    values = lazy_series.head(limit) if limit is not None else lazy_series

    print(f"Колонка '{column_name}': всього унікальних значень (без NULL) — {total_unique}")
    for val in values:
        print(val)


if __name__ == "__main__":
    parquet_file = Path("data", "packet_21", "dataset.parquet")
    target_column = "principal_diagnosis"  # Замініть на назву вашої колонки
    print_unique_values(parquet_file, target_column)
