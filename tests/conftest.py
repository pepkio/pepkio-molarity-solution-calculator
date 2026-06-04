"""Pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load monorepo .env for local integration runs (never log keys).
_monorepo_env = Path(__file__).resolve().parents[3] / ".env"
if _monorepo_env.is_file():
    load_dotenv(_monorepo_env, override=True)

_package_env = Path(__file__).resolve().parents[1] / ".env"
if _package_env.is_file():
    load_dotenv(_package_env, override=True)


@pytest.fixture
def mock_manifest() -> dict:
    return {
        "tool_id": "molarity-solution-calculator",
        "title": "Molarity Solution Calculator",
        "execution_mode": "sync",
        "examples": [
            {
                "name": "powder_cuso4",
                "input": {
                    "mode": "powder",
                    "mw_anhydrous_g_per_mol": 159.61,
                    "hydrate_notation": "·5H₂O",
                    "purity_percent": 99,
                    "target_concentration": 10,
                    "target_concentration_unit": "mM",
                    "final_volume": 50,
                    "final_volume_unit": "mL",
                },
                "output": {"result": {"mass_g": 0.081}},
            },
            {
                "name": "dilution_pbs_10x",
                "input": {
                    "mode": "dilution",
                    "stock_concentration": 10,
                    "stock_unit": "M",
                    "target_concentration": 1,
                    "target_unit": "M",
                    "final_volume": 1,
                    "final_volume_unit": "L",
                },
                "output": {"result": {"stock_volume_L": 0.1}},
            },
            {
                "name": "serial_1M_to_1uM",
                "input": {
                    "mode": "serial",
                    "stock_concentration": 1,
                    "stock_unit": "M",
                    "target_concentration": 1,
                    "target_unit": "uM",
                    "num_steps": 4,
                    "final_volume_ul": 100,
                },
                "output": {"result": {"step_count": 4}},
            },
        ],
    }


@pytest.fixture
def mock_run_response() -> dict:
    return {
        "run_id": "run_test123",
        "status": "completed",
        "result": {
            "mode": "powder",
            "result": {"mass_g": 0.081},
            "warnings": [],
            "protocol_steps": [],
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_test123",
        "permalink": "https://tools.pepkio.com/r/run_test123",
    }
