"""
download_dataset.py

Downloads the latest Steam Games dataset from Kaggle and copies the
raw source file into the project's Bronze layer.
"""

from pathlib import Path
import shutil

import kagglehub


DATASET = "artermiloff/steam-games-dataset"
SOURCE_FILE = "games_march2025_cleaned.csv"


def main():
    print("Downloading latest Steam dataset...")

    dataset_path = Path(kagglehub.dataset_download(DATASET))

    source_file = dataset_path / SOURCE_FILE

    if not source_file.exists():
        raise FileNotFoundError(f"Could not find {SOURCE_FILE}")

    bronze_dir = Path("data/bronze")
    bronze_dir.mkdir(parents=True, exist_ok=True)

    destination = bronze_dir / SOURCE_FILE

    shutil.copy2(source_file, destination)

    print("Dataset successfully copied to Bronze layer.")
    print(f"Location: {destination.resolve()}")


if __name__ == "__main__":
    main()