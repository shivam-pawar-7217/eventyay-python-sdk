import json
from pathlib import Path
from typer.testing import CliRunner

from eventyay.cli import app

runner = CliRunner()

def test_version_command():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "Eventyay CLI v0.1.0" in result.stdout

def test_login_command(monkeypatch, tmp_path):
    # The constants are evaluated at import time, so we must mock them directly
    # on the module to ensure the test isolates config writing to tmp_path.
    target_config_dir = tmp_path / ".config" / "eventyay"
    target_config_file = target_config_dir / "config.json"
    
    monkeypatch.setattr("eventyay.cli.CONFIG_DIR", target_config_dir)
    monkeypatch.setattr("eventyay.cli.CONFIG_FILE", target_config_file)

    # Run the login command, simulating user input
    result = runner.invoke(app, ["login"], input="test-dummy-api-key\n")
    
    assert result.exit_code == 0
    assert "Successfully saved API key to config" in result.stdout
    
    # Verify the config file was created and contains the correct data
    assert target_config_file.exists()
    
    with open(target_config_file, "r") as f:
        data = json.load(f)
        assert data.get("api_key") == "test-dummy-api-key"
