"""Tests for the CLI tool."""

import json
from unittest.mock import Mock

from typer.testing import CliRunner

from eventyay.cli import app

runner = CliRunner()


class TestVersionCommand:
    def test_shows_version(self):
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "Eventyay CLI v0.1.0" in result.stdout


class TestLoginCommand:
    def test_saves_api_key(self, monkeypatch, tmp_path):
        target_config_dir = tmp_path / ".config" / "eventyay"
        target_config_file = target_config_dir / "config.json"

        monkeypatch.setattr("eventyay.cli.CONFIG_DIR", target_config_dir)
        monkeypatch.setattr("eventyay.cli.CONFIG_FILE", target_config_file)

        result = runner.invoke(app, ["login"], input="test-dummy-api-key\n")

        assert result.exit_code == 0
        assert "Successfully saved API key to config" in result.stdout

        assert target_config_file.exists()
        with open(target_config_file, "r") as f:
            data = json.load(f)
            assert data.get("api_key") == "test-dummy-api-key"


class TestLogoutCommand:
    def test_removes_api_key(self, monkeypatch, tmp_path):
        target_config_dir = tmp_path / ".config" / "eventyay"
        target_config_file = target_config_dir / "config.json"
        target_config_dir.mkdir(parents=True)
        with open(target_config_file, "w") as f:
            json.dump({"api_key": "old-key"}, f)

        monkeypatch.setattr("eventyay.cli.CONFIG_DIR", target_config_dir)
        monkeypatch.setattr("eventyay.cli.CONFIG_FILE", target_config_file)

        result = runner.invoke(app, ["logout"])

        assert result.exit_code == 0
        assert "API key removed" in result.stdout

        with open(target_config_file, "r") as f:
            data = json.load(f)
            assert "api_key" not in data

    def test_logout_no_config(self, monkeypatch, tmp_path):
        target_config_file = tmp_path / "nonexistent" / "config.json"
        monkeypatch.setattr("eventyay.cli.CONFIG_FILE", target_config_file)

        result = runner.invoke(app, ["logout"])

        assert result.exit_code == 0
        assert "No config file found" in result.stdout


class TestConfigCommand:
    def test_shows_config(self, monkeypatch, tmp_path):
        target_config_dir = tmp_path / ".config" / "eventyay"
        target_config_file = target_config_dir / "config.json"
        target_config_dir.mkdir(parents=True)
        with open(target_config_file, "w") as f:
            json.dump({"api_key": "mykey12345"}, f)

        monkeypatch.setattr("eventyay.cli.CONFIG_DIR", target_config_dir)
        monkeypatch.setattr("eventyay.cli.CONFIG_FILE", target_config_file)
        monkeypatch.delenv("EVENTYAY_API_KEY", raising=False)

        result = runner.invoke(app, ["config"])

        assert result.exit_code == 0
        assert "myke****" in result.stdout


class TestEventsListCommand:
    def test_lists_events(self, monkeypatch):
        from eventyay.models import Event, EventList

        mock_events = EventList(
            data=[
                Event(
                    id=1,
                    name="Test Event",
                    identifier="test",
                    starts_at="2026-01-01",
                    privacy="public",
                )
            ]
        )
        mock_client = Mock()
        mock_client.get_events.return_value = mock_events
        monkeypatch.setattr("eventyay.cli._client", mock_client)

        result = runner.invoke(app, ["events", "list"])

        assert result.exit_code == 0
        assert "Test Event" in result.stdout

    def test_json_output(self, monkeypatch):
        from eventyay.models import Event, EventList

        mock_events = EventList(data=[Event(id=1, name="JSON Event", identifier="json-test")])
        mock_client = Mock()
        mock_client.get_events.return_value = mock_events
        monkeypatch.setattr("eventyay.cli._client", mock_client)

        result = runner.invoke(app, ["events", "list", "--output", "json"])

        assert result.exit_code == 0
        assert "JSON Event" in result.stdout


class TestEventsShowCommand:
    def test_shows_event(self, monkeypatch):
        from eventyay.models import Event

        mock_event = Event(
            id=1,
            name="Detail Event",
            identifier="detail-test",
            starts_at="2026-01-01",
            ends_at="2026-01-02",
            privacy="public",
        )
        mock_client = Mock()
        mock_client.get_event.return_value = mock_event
        monkeypatch.setattr("eventyay.cli._client", mock_client)

        result = runner.invoke(app, ["events", "show", "1"])

        assert result.exit_code == 0
        assert "Detail Event" in result.stdout
