"""Tests for the element_of_day plugin."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from plugins.element_of_day import ElementOfDayPlugin
from src.plugins.base import PluginResult

MANIFEST = json.loads("""
{
    "id": "element_of_day",
    "name": "Element of the Day",
    "version": "0.1.0",
    "settings_schema": {
        "type": "object",
        "properties": {
            "enabled": {
                "type": "boolean",
                "title": "Enabled",
                "default": false
            },
            "refresh_seconds": {
                "type": "integer",
                "title": "Refresh Interval (seconds)",
                "description": "How often to refresh (once per day is sufficient).",
                "default": 3600,
                "minimum": 3600
            }
        },
        "required": []
    }
}
""")

SAMPLE_RESPONSE = json.loads("""
{
    "element_name": "Hydrogen",
    "symbol": "H",
    "atomic_number": 1,
    "atomic_weight": "1.008",
    "category": "nonmetal"
}
""")


@pytest.fixture
def plugin():
    return ElementOfDayPlugin(MANIFEST)


@pytest.fixture
def configured_plugin():
    p = ElementOfDayPlugin(MANIFEST)
    p.config = json.loads("""
{}
""")
    return p


class TestElementOfDayPlugin:

    def test_plugin_id(self, plugin):
        assert plugin.plugin_id == "element_of_day"

    def test_manifest_valid(self):
        manifest_path = Path(__file__).parent.parent / "manifest.json"
        with open(manifest_path) as f:
            m = json.load(f)
        for field in ("id", "name", "version"):
            assert field in m

    @patch("plugins.element_of_day.requests.get")
    def test_fetch_data_success(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is True
        assert result.error is None
        assert result.data is not None
        assert "element_name" in result.data, "missing variable: element_name"
        assert "symbol" in result.data, "missing variable: symbol"
        assert "atomic_number" in result.data, "missing variable: atomic_number"
        assert "atomic_weight" in result.data, "missing variable: atomic_weight"
        assert "category" in result.data, "missing variable: category"

    @pytest.mark.skip(reason="plugin does not use requests.get")
    def test_fetch_data_network_error(self, configured_plugin):
        pass

    @pytest.mark.skip(reason="plugin does not use requests.get")
    def test_fetch_data_bad_json(self, configured_plugin):
        pass

