# Application COnfiguration
from pathlib import Path

# Root project folder 
BASE_DIR = Path(__file__).resolve().parent

# Reports folder
REPORT_DIR = BASE_DIR / "reports"

# Exports folder
EXPORT_DIR = BASE_DIR / "exports"

# Log folder
LOG_DIR = BASE_DIR / "logs"

REPORT_DIR.mkdir(exist_ok=True)
EXPORT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)