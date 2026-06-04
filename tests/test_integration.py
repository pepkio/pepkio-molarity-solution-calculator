"""Integration tests against live Pepkio Tools API."""

from __future__ import annotations

import os

import pytest

from pepkio_molarity_solution_calculator.client import PepkioClient
from pepkio_molarity_solution_calculator.exceptions import PepkioAPIError

# Local first, then production (param order).
ENVIRONMENTS = [
    ("local", "https://tools.localtest.me"),
    ("production", "https://tools.pepkio.com"),
]


def _api_key_for(base_url: str) -> str | None:
    if "localtest.me" in base_url:
        return os.getenv("LOCAL_PEPKIO_API_KEY")
    return os.getenv("PEPKIO_API_KEY")


@pytest.fixture(params=ENVIRONMENTS, ids=["local", "production"])
def live_client(request):
    env_name, base_url = request.param
    api_key = _api_key_for(base_url)
    if not api_key:
        pytest.skip(f"No API key for {env_name} (set LOCAL_PEPKIO_API_KEY or PEPKIO_API_KEY)")
    with PepkioClient(api_key=api_key, base_url=base_url) as client:
        try:
            client.get_manifest(refresh=True)
        except PepkioAPIError as exc:
            if exc.status_code == 404 and exc.code == "TOOL_NOT_FOUND":
                pytest.skip(f"Tool not deployed on {env_name} ({base_url})")
            raise
        yield client


def test_get_manifest(live_client: PepkioClient):
    manifest = live_client.get_manifest(refresh=True)
    assert manifest["tool_id"] == "molarity-solution-calculator"
    names = live_client.list_examples()
    assert "powder_cuso4" in names
    assert "dilution_pbs_10x" in names
    assert "serial_1M_to_1uM" in names


def test_run_powder_cuso4(live_client: PepkioClient):
    inp = live_client.get_example_input("powder_cuso4")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.run_id
    assert result.permalink
    assert result.result is not None
    assert result.result.get("mode") == "powder"
    inner = result.result.get("result")
    assert isinstance(inner, dict)
    mass_g = inner.get("mass_g")
    assert isinstance(mass_g, (int, float))
    assert 0.07 < mass_g < 0.15
    assert result.result.get("error") is None


def test_run_dilution_pbs_10x(live_client: PepkioClient):
    inp = live_client.get_example_input("dilution_pbs_10x")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("mode") == "dilution"
    stock_volume = result.result.get("result", {}).get("stock_volume_L")
    assert isinstance(stock_volume, (int, float))
    assert abs(stock_volume - 0.1) < 0.01


def test_run_serial_1M_to_1uM(live_client: PepkioClient):
    inp = live_client.get_example_input("serial_1M_to_1uM")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("mode") == "serial"
    assert result.result.get("result", {}).get("step_count") == 4
