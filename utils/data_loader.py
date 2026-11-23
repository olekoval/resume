from pathlib import Path
import polars as pl

ROOT_MARKER = "pyproject.toml"

def _dataset_path(name_dir):
    current = Path(__file__).resolve()
    for parent in  current.parents:
        if (parent / ROOT_MARKER).exists():
            return parent / "data" / name_dir / "dataset.parquet"
    return None


def dataset_loader(directory):
    path = _dataset_path(directory)
    if path is  None:
        raise FileNotFoundError(
                f"Could not find project root with marker '{ROOT_MARKER}'"
                f" or path for '{directory}'."
                )                
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")

    return pl.scan_parquet(path)
