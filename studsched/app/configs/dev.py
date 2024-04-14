"""DEV Environment"""
# mypy: ignore-errors
from .base import Settings


class SettingsDev(Settings):
    DEBUG = True
    LOAD_EXAMPLE_DATA = True
    DUMP_SQL_FILE = "db/example_data/dump.sql"
