# Pepkio Molarity Solution Calculator

Python client for the Pepkio Molarity Solution Calculator API: powder mass, single-step dilution volumes, and serial dilution tables with hydrate and purity correction plus bench-ready protocols.

# Overview

Preparing solutions at a defined molarity is a routine step in molecular biology, biochemistry, cell culture, and analytical chemistry. Researchers weigh solid reagents to make stock solutions, dilute concentrated stocks to working concentrations, and build serial dilution series for standard curves or dose–response experiments. Each calculation involves unit conversions (millimolar to micromolar, grams to moles), volume arithmetic, and—when the reagent is a hydrated salt or not 100% pure—corrections that simple calculators often omit.

Manual spreadsheets and generic molarity calculators typically solve one equation at a time. They may ignore water of crystallization in hydrated salts (for example CuSO₄·5H₂O), supplier purity on the bottle label, or the difference between anhydrous and hydrated molecular weight. The result is often under-weighed powder and solutions that are less concentrated than intended. Unit mistakes (confusing mL with µL, or mM with µM) are another common source of error at the bench.

The [Pepkio Molarity Solution Calculator](https://www.pepkio.com/tools/molarity-solution-calculator) web application computes powder mass to weigh, stock and diluent volumes for a single dilution, or a multi-step serial dilution table—with hydrate parsing, purity adjustment, plain-language protocol steps, and shareable saved recipes. This repository provides the **Python client** (`pepkio-molarity-solution-calculator`) that calls the same calculation engine through the Pepkio Tools REST API, so you can generate solution prep instructions from scripts, Jupyter notebooks, or automated pipelines.

If you prefer a graphical interface, use the hosted web tool (see [Web Application](#web-application) below). If you need reproducible, programmatic access, install the package from [PyPI](https://pypi.org/project/pepkio-molarity-solution-calculator/) and follow the Quick Start below.

# Features

## Solution calculations (API-backed)

- **Three modes:** `powder` (mass to weigh from solid), `dilution` (C₁V₁ = C₂V₂ single step), `serial` (multi-step concentration table)
- **Powder mode:** anhydrous molecular weight, hydrate notation (e.g. ·5H₂O), and supplier purity percent; returns corrected mass in grams and effective hydrated MW
- **Dilution mode:** stock and target concentration with unit support (`M`, `mM`, `uM`, `nM`); stock volume, diluent volume, dilution factor, and final volume
- **Serial mode:** step count, final volume per tube in µL, concentration and transfer/diluent volumes at each step
- **Protocol steps:** plain-language bench instructions returned with every run
- **Warnings:** flags impractical pipette volumes in serial mode (for pipette-aware rounding and plate maps, use the [Serial Dilution Planner](https://www.pepkio.com/tools/serial-dilution-planner))
- **Shareable runs:** each API run returns a `permalink` that restores the exact parameters

## Python package

- Fetch the tool manifest and list named examples (`get_manifest`, `list_examples`, `get_example_input`)
- Run calculations synchronously (`run`) with custom JSON or manifest examples
- Poll runs for async tools (`get_run`, `wait_for_run`)
- CLI for manifest inspection and one-off runs (`pepkio-molarity-solution-calculator`)
- Configurable API base URL and API keys via environment variables

# Common Use Cases

### Weighing a hydrated salt for a stock solution (`powder_cuso4`)

Prepare 10 mM CuSO₄ in 50 mL from bottle-labeled CuSO₄·5H₂O at 99% purity. Enter anhydrous MW (159.61 g/mol), hydrate notation, purity, target concentration, and final volume. The calculator returns grams to weigh with hydrate and purity correction—avoiding the common error of using anhydrous MW while weighing the pentahydrate.

### Diluting a concentrated buffer (`dilution_pbs_10x`)

Dilute 10× PBS stock to 1× in 1 L. Enter stock concentration, target concentration, and final volume; receive stock volume and diluent volume plus step-by-step mixing instructions.

### Quick serial dilution estimate (`serial_1M_to_1uM`)

Plan a four-step serial dilution from 1 M stock to 1 µM with 100 µL per tube. Useful for estimating transfer volumes before moving to pipette-aware planning in the Serial Dilution Planner when volumes fall below practical pipetting limits.

### Cell culture media and reagent stocks

Calculate how much powder to dissolve for a defined molarity in a given flask volume, or how much 100 mM stock to add when making a 10 mM working solution in a specified final volume.

### Teaching solution preparation

Students practice linking molecular weight, molarity, and mass while seeing how hydrate water and purity affect the amount weighed.

# Why This Tool Exists

Spreadsheets and many online molarity calculators solve **mass = M × V × MW** or **C₁V₁ = C₂V₂** without adjusting for:

- **Hydrated salts:** the molecular weight on a datasheet may be anhydrous, but the bottle contains a hydrate form with extra water molecules per formula unit.
- **Reagent purity:** supplier labels often state 95–99% active content; ignoring purity leads to under-weighing.
- **Workflow integration:** powder prep, dilution, and serial tables are usually separate calculators or tabs, so researchers re-enter the same stock concentration multiple times.

Generic tools (for example basic molarity pages from reagent suppliers or general-purpose dilution calculators) rarely output step-by-step bench instructions, saved recipes, or shareable links. They also do not warn when serial transfer volumes are below typical pipette minimums.

The Pepkio Molarity Solution Calculator combines powder, dilution, and serial modes in one workspace with live results, hydrate parsing, purity adjustment, protocol text, and shareable permalinks. When serial volumes are impractical to pipette, the web interface directs you to the Serial Dilution Planner for pipette rounding and plate maps. The Python package in this repository calls the same API for scripted or automated workflows.

# Installation

Install from PyPI:

```bash
pip install pepkio-molarity-solution-calculator
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add pepkio-molarity-solution-calculator
```

PyPI package: [https://pypi.org/project/pepkio-molarity-solution-calculator/](https://pypi.org/project/pepkio-molarity-solution-calculator/)

## API key

Programmatic runs require a Pepkio API key with **tools:run** scope. Create one at [https://www.pepkio.com/account/api-keys](https://www.pepkio.com/account/api-keys).

```bash
export PEPKIO_API_KEY="your-key"
```

| Variable | Description |
|----------|-------------|
| `PEPKIO_API_KEY` | Production (or default) API key |
| `LOCAL_PEPKIO_API_KEY` | Local dev key when base URL points to `tools.localtest.me` |
| `PEPKIO_API_BASE_URL` | Override API host (default: `https://tools.pepkio.com`) |
| `PEPKIO_SSL_VERIFY` | Set to `0` or `false` to disable TLS verify (local dev disables verify for `localtest.me` by default) |

Local development against a staging stack:

```bash
export PEPKIO_API_BASE_URL=https://tools.localtest.me
export PEPKIO_API_KEY="$LOCAL_PEPKIO_API_KEY"
```

Web UI (local): [https://www.localtest.me/tools/molarity-solution-calculator](https://www.localtest.me/tools/molarity-solution-calculator)

# Quick Start

Manifest inspection does **not** require an API key. Running the tool does.

### Python: powder example

```python
from pepkio_molarity_solution_calculator import PepkioClient

with PepkioClient() as client:
    inp = client.get_example_input("powder_cuso4")
    result = client.run(inp)
    print(result.status, result.permalink)
    out = result.result
    print("Mass to weigh:", out["result"]["mass_display"])
    print("Effective MW:", out["effective_mw_g_per_mol"], "g/mol")
    for step in out["protocol_steps"]:
        print(step)
```

### Python: single dilution

```python
from pepkio_molarity_solution_calculator import PepkioClient

inp = {
    "mode": "dilution",
    "stock_concentration": 10,
    "stock_unit": "M",
    "target_concentration": 1,
    "target_unit": "M",
    "final_volume": 1,
    "final_volume_unit": "L",
}

with PepkioClient() as client:
    result = client.run(inp)
    r = result.result["result"]
    print(r["stock_volume_display"], "stock +", r["diluent_volume_display"], "diluent")
    print("Dilution factor:", r["dilution_factor"])
```

### Python: serial dilution table

```python
from pepkio_molarity_solution_calculator import PepkioClient

with PepkioClient() as client:
    inp = client.get_example_input("serial_1M_to_1uM")
    result = client.run(inp)
    for step in result.result["result"]["steps"]:
        print(step["step"], step["concentration_display"], step["transfer_ul"], "µL transfer")
```

### CLI

```bash
# Manifest (no API key)
pepkio-molarity-solution-calculator manifest
pepkio-molarity-solution-calculator manifest --examples

# Run a named example (API key required)
pepkio-molarity-solution-calculator run --example powder_cuso4

# Run custom JSON input
pepkio-molarity-solution-calculator run --input-json '{"mode":"dilution","stock_concentration":10,"stock_unit":"M","target_concentration":1,"target_unit":"M","final_volume":1,"final_volume_unit":"L"}'
```

Options: `--api-key`, `--base-url`, `--label`, `--idempotency-key`.

# Example Output

A completed run for the `powder_cuso4` manifest example (10 mM CuSO₄·5H₂O in 50 mL, 99% purity) returns a structure similar to:

```json
{
  "run_id": "3dbb9b7a-dd01-4659-9631-3e59ad283aed",
  "status": "completed",
  "permalink": "https://tools.pepkio.com/r/3dbb9b7a-dd01-4659-9631-3e59ad283aed",
  "result": {
    "mode": "powder",
    "effective_mw_g_per_mol": 249.685,
    "warnings": [],
    "protocol_steps": [
      "Weigh 0.1261 g into a suitable container",
      "Dissolve in 40 mL solvent (e.g. ddH₂O)",
      "Adjust pH if required",
      "Top up to 50 mL final volume"
    ],
    "result": {
      "mass_g": 0.1261,
      "mass_display": "0.1261 g",
      "target_molarity_M": 0.01,
      "purity_adjusted": true
    }
  }
}
```

A `dilution_pbs_10x` run (10× → 1× in 1 L) includes stock and diluent volumes:

```json
{
  "result": {
    "mode": "dilution",
    "protocol_steps": [
      "Pipette 0.1000 L of stock solution",
      "Add 0.9000 L diluent (water or buffer)",
      "Mix and verify final volume is 1.000 L"
    ],
    "result": {
      "stock_volume_L": 0.1,
      "stock_volume_display": "0.1000 L",
      "diluent_volume_L": 0.9,
      "dilution_factor": 10
    }
  }
}
```

The `permalink` field links to a saved run that colleagues can open in the browser to review the same parameters and protocol.

# Scientific Background

## Molarity

**Molarity (M)** is moles of solute per liter of solution:

**M = n / V**

where n is amount in moles and V is volume in liters. To prepare a solution from solid:

**mass (g) = M × V (L) × MW (g/mol)**

Researchers search for molarity calculator, solution preparation calculator, and how to make a mM stock from powder—these all reduce to this relationship with consistent units.

## C₁V₁ = C₂V₂ (single dilution)

For one mixing step, amount of solute is conserved:

**C₁V₁ = C₂V₂**

where C is concentration and V is volume. Given any three of initial concentration, final concentration, stock volume, and final volume, you can solve for the fourth. This applies to diluting a stock into a larger final volume (for example 100 mM → 10 mM) or preparing a fixed final volume from a concentrated stock.

**Dilution factor** for a single step: DF = C_stock / C_final = V_final / V_stock.

## Hydrated salts and effective molecular weight

Many laboratory chemicals are sold as hydrates (e.g. CuSO₄·5H₂O, Na₂HPO₄·7H₂O). The anhydrous molecular weight from a datasheet does not match the mass per mole of the solid in the bottle. The calculator parses hydrate notation and computes an **effective molecular weight** that includes crystal water, so the weighed mass matches the target molarity in the final solution volume.

## Purity correction

Reagent bottles often specify purity below 100% (for example ≥99%). The required mass is increased proportionally so the **active** amount of compound in the final solution meets the target concentration:

**mass_corrected = mass_ideal × (100 / purity_percent)**

## Serial dilution

In a constant-ratio **serial dilution**, each step dilutes the previous tube into fresh solvent. If each step has dilution factor DF and you perform n steps from initial concentration C₀:

**Cₙ = C₀ / DFⁿ**

The Molarity Solution Calculator’s `serial` mode produces a step table with concentration, transfer volume, and diluent volume per step. For pipette-aware rounding, economy mode, and microplate maps, use the dedicated [Serial Dilution Planner](https://www.pepkio.com/tools/serial-dilution-planner).

## Unit conventions

Supported molar units include `M`, `mM`, `uM`, and `nM`. Volume units for powder and dilution modes include `mL` and `L`; serial mode uses `final_volume_ul` in microliters per step. Always confirm whether a concentration refers to the solute alone or a complex formulation (for example percent w/v vs molarity).

# Frequently Asked Questions

### What is molarity?

Molarity (M) is the number of moles of solute per liter of solution. A 1 M solution contains one mole of solute per liter. Millimolar (mM), micromolar (µM), and nanomolar (nM) are common in biochemistry and cell biology.

### How do I calculate how much powder to weigh for a mM solution?

Use **mass (g) = M × V (L) × MW (g/mol)**. Convert target concentration to molar (for example 10 mM = 0.01 M), multiply by final volume in liters and by the correct molecular weight—including hydrate water if you are weighing a hydrated salt. Adjust for purity if the bottle is not 100%. The `powder` mode in the Pepkio Molarity Solution Calculator performs these steps automatically.

### What is C1V1 = C2V2?

It is the conservation-of-mass equation for a single dilution: initial concentration × volume used = final concentration × final volume. Use it to find how much stock to pipette into a known diluent volume, or what concentration results from a chosen transfer. The `dilution` mode applies this relation and reports stock volume, diluent volume, and dilution factor.

### How do I dilute a 10x buffer to 1x?

Enter stock concentration 10, target concentration 1 (same unit, e.g. × or M depending on how your stock is labeled), and desired final volume. For 1 L of 1× from 10× stock, you need 0.1 L stock and 0.9 L diluent—a 10-fold dilution. See the `dilution_pbs_10x` manifest example.

### Why does my weighed mass differ from a simple MW calculator?

If the compound is a hydrate or the bottle purity is below 100%, the ideal mass from anhydrous MW alone is too low. Hydrate water increases the formula weight of the solid; impurity decreases the active fraction. Both corrections increase the mass you should weigh.

### How do I enter hydrate notation?

In powder mode, supply `mw_anhydrous_g_per_mol` and `hydrate_notation` such as `·5H₂O`. The tool computes `effective_mw_g_per_mol` and uses it for the mass calculation.

### What is serial dilution?

Serial dilution prepares a geometric series of concentrations by repeatedly diluting the previous solution into fresh solvent. Each step uses the same dilution factor. It is used for standard curves, dose–response setups, and template dilutions before qPCR.

### How do I calculate dilution factor?

For one step, dilution factor DF = C_before / C_after (equivalently V_final / V_stock for a single dilution). For n identical serial steps from C₀, final concentration Cₙ = C₀ / DFⁿ.

### How do I prepare a standard curve?

Start from a concentrated stock at known concentration. Choose the number of standards and desired highest and lowest concentrations. A serial dilution with constant dilution factor gives evenly log-spaced points—standard for ELISA and qPCR. Use `serial` mode here for volume estimates, or the Serial Dilution Planner for pipette-rounded protocols.

### How do I design a dilution series for qPCR?

Dilute purified template across a range bracketing expected sample Ct values. Use consistent volume per tube, document the dilution factor, and avoid pipette volumes below your instrument minimum. If serial transfer volumes are sub-microliter, the web tool warns you and suggests the Serial Dilution Planner.

### What units does the Molarity Solution Calculator support?

Molar: `M`, `mM`, `uM`, `nM`. Powder and dilution final volumes: `mL`, `L`. Serial mode: `final_volume_ul` in microliters. Dilution mode also accepts `molecular_weight_g_per_mol` when mixing mass/volume stock with molar targets.

### What is the difference between this tool and the Serial Dilution Planner?

The Molarity Solution Calculator covers powder weighing, single-step dilution, and a lightweight serial table with ideal (unrounded) transfer volumes. The Serial Dilution Planner adds pipette-aware rounding, economy mode, and 96/384-well plate maps for execution-focused serial protocols.

### Can I move from powder result to dilution in the web app?

Yes. The web interface lets you send a powder result into the dilution tab as stock concentration, so you do not retype values when planning a two-stage prep (weigh stock, then dilute to working concentration).

### Do I need an API key for the Python client?

No key is required for `get_manifest()` or the CLI `manifest` command. `run()` and the CLI `run` command require an API key with tools:run scope.

### Can I run the tool offline?

The Python package calls the hosted Pepkio Tools API; an internet connection and valid API key are required for runs. Calculations are not bundled for fully offline use in this package.

### How do I share a solution prep protocol?

Open the web tool and use the shareable link feature, or share the `permalink` returned from an API run. The link restores the same mode, concentrations, volumes, and hydrate/purity settings.

### What are common mistakes in solution preparation?

Using anhydrous MW while weighing a hydrate; ignoring purity on the label; confusing mM with µM; mixing up stock volume and final volume in C₁V₁ = C₂V₂; and pipetting serial transfers that are below the pipette minimum. Following printed `protocol_steps` reduces execution errors.

### How do I convert between mass concentration and molarity?

**C_molar (M) = C_mass (g/L) / MW (g/mol)** with consistent units. Provide `molecular_weight_g_per_mol` in dilution mode when stock and target use different unit types.

### Does purity affect dilution mode?

Purity correction applies primarily to powder weighing. For liquid stocks, concentration is usually assumed as labeled on the bottle unless you apply a separate correction factor.

# Web Application

For interactive solution prep without writing code, use the hosted Pepkio Molarity Solution Calculator at [https://www.pepkio.com/tools/molarity-solution-calculator](https://www.pepkio.com/tools/molarity-solution-calculator).

The web interface provides three tabs—powder-to-solution, dilution, and serial dilution—with live results as you type. Enter molecular weight, optional hydrate notation, and label purity so weighed mass matches your reagent bottle. Results include grams to weigh, stock and diluent volumes, or a step-by-step serial table, plus plain-language bench instructions to copy or print.

The web version also supports:

- **Saved recipes** — store named buffer and reagent prep parameters in the browser for solutions you make weekly
- **Shareable links** — restore exact inputs for collaborators or lab notebooks
- **Powder-to-dilution handoff** — move a powder result into the dilution tab as stock with one click
- **Volume warnings** — flag impractical pipette volumes and open the Serial Dilution Planner when pipette-aware rounding is needed
- **Printable worksheets** — copy or print protocol text for use at the hood

**Web Application:** [https://www.pepkio.com/tools/molarity-solution-calculator](https://www.pepkio.com/tools/molarity-solution-calculator)

# Related Resources

- **GitHub Repository:** [https://github.com/pepkio/pepkio-molarity-solution-calculator](https://github.com/pepkio/pepkio-molarity-solution-calculator)
- **PyPI Package:** [https://pypi.org/project/pepkio-molarity-solution-calculator/](https://pypi.org/project/pepkio-molarity-solution-calculator/)
- **Web Application:** [https://www.pepkio.com/tools/molarity-solution-calculator](https://www.pepkio.com/tools/molarity-solution-calculator)

# About Pepkio

[Pepkio](https://www.pepkio.com) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (RNA-seq, single-cell RNA-seq, spatial transcriptomics, functional enrichment, and custom workflows).

# Citation

If you use Pepkio Molarity Solution Calculator in a publication or protocol, cite the web tool and optionally the Python package version:

```bibtex
@misc{pepkio_molarity_solution_calculator,
  title        = {Pepkio Molarity Solution Calculator},
  author       = {Pepkio},
  year         = {2026},
  howpublished = {\url{https://www.pepkio.com/tools/molarity-solution-calculator}},
  note         = {Python client: pepkio-molarity-solution-calculator on PyPI}
}
```

# License

See the [GitHub repository](https://github.com/pepkio/pepkio-molarity-solution-calculator) for license terms.

# Keywords

molarity calculator, molarity solution calculator, solution preparation calculator, how to make mM solution, powder to solution, mass from molarity, weigh powder for stock, molecular weight calculator, hydrate correction, hydrated salt molarity, CuSO4 pentahydrate mass, purity correction, reagent purity adjustment, C1V1=C2V2, dilution calculator, stock dilution volume, dilution factor, single step dilution, buffer dilution calculator, PBS dilution, serial dilution calculator, serial dilution table, mM to uM dilution, micromolar stock preparation, standard curve preparation, qPCR template dilution, cell culture media preparation, biochemistry solution prep, laboratory protocol generator, bench protocol, solution prep protocol, effective molecular weight, anhydrous vs hydrated MW, grams to moles calculator, mol/L calculator, concentration unit conversion, Pepkio, pepkio-molarity-solution-calculator, Python molarity API, lab automation solution prep, shareable lab protocol, printable worksheet dilution, stock volume calculator, diluent volume calculator, working solution from stock, molecular biology calculator, chemistry lab calculator

how to calculate molarity from mass and volume, how much powder to weigh for 10 mM solution in 50 mL, molarity calculator with hydrate correction, adjust mass for reagent purity percent, how to dilute 10x buffer to 1x volume, C1V1 C2V2 dilution calculator explained, how to make CuSO4 5H2O stock solution, anhydrous molecular weight vs hydrate weighing, calculate stock and diluent volumes for dilution, dilution factor from stock to working concentration, quick serial dilution from 1 M to 1 uM, serial dilution step volumes 100 uL per tube, when to use serial dilution planner vs molarity calculator, sub pipette volume warning serial dilution, save buffer recipe in browser lab tool, shareable link restore solution prep parameters, Python script calculate powder mass molarity, API for laboratory solution preparation, prepare ELISA standard from concentrated stock, qPCR working dilution from mM stock, convert mM to uM for dilution planning, common mistakes weighing hydrated salts, how purity affects grams to weigh, top up to final volume protocol steps, move powder result to dilution tab, Pepkio molarity solution calculator web tool, make stock solution from solid reagent protocol, calculate microliter transfer serial dilution estimate, laboratory notebook dilution worksheet, automated buffer prep from Python notebook, difference between molarity and dilution factor, prepare working concentration from weighed stock

# Contributing

Clone this repository, run `uv sync`, and execute `uv run pytest` for unit and integration tests. Integration tests require `PEPKIO_API_KEY` or `LOCAL_PEPKIO_API_KEY` in the environment.
