import json, os, tempfile, pytest
from src.config.loader import load_config, AppConfig

pytestmark = pytest.mark.unit

def test_load_config_from_temp_file(monkeypatch):
    fd, p = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    with open(p, "w", encoding="utf-8") as f:
        json.dump({"db_url":"sqlite://","env":"test"}, f)
    monkeypatch.setenv("SWAB_CONFIG_PATH", p)
    cfg = load_config()
    assert isinstance(cfg, AppConfig)
    assert cfg.env == "test" and cfg.db_url == "sqlite://"
    os.remove(p)
