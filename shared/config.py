from configparser import ConfigParser
from pathlib import Path

def load_db_config(filename: str = "database.ini",
                   section: str = "postgresql") -> dict:
    
    parser = ConfigParser()
    config_path = Path(__file__).parent.parent / filename
    parser.read(config_path)
    if not parser.has_section(section):
        raise RuntimeError(f"[postgresql] section not found in {config_path}")
    return dict(parser.items(section))


