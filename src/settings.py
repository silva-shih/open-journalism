from pathlib import Path

THIS_DIR = Path(__file__).parent
ROOT_DIR = THIS_DIR.parent
DATA_DIR = ROOT_DIR / "data"
EXTRACT_DIR = DATA_DIR / "extracted"
TRANSFORM_DIR = DATA_DIR / "transformed"
