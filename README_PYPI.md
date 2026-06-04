# Pepkio Molarity Solution Calculator

Python client for the Pepkio Molarity Solution Calculator API: powder mass, single-step dilution volumes, and serial dilution tables with hydrate and purity correction from scripts or notebooks.

# What It Does

Preparing solutions at a defined molarity is routine in molecular biology, biochemistry, and cell culture. Researchers weigh solid reagents for stock solutions, dilute concentrated stocks to working concentrations, and plan serial dilution series for standard curves or dose–response experiments.

Spreadsheets and generic molarity calculators often ignore hydrate water in salts (for example CuSO₄·5H₂O), supplier purity on the bottle, or unit conversions between mM and µM. That can lead to under-weighed powder and solutions below the intended concentration.

This package calls the same Pepkio Tools calculation engine as the hosted web application. Use `PepkioClient.run()` from Python, Jupyter, or automation pipelines to obtain grams to weigh, stock and diluent volumes, serial step tables, plain-language protocol steps, and shareable run links.

Programmatic runs require a network connection and a Pepkio API key. Calculations are not bundled for offline use.

# Features

- Three modes: `powder` (mass from solid), `dilution` (C₁V₁ = C₂V₂), `serial` (multi-step concentration table)
- Powder mode: anhydrous molecular weight, hydrate notation (e.g. ·5H₂O), and purity percent; returns corrected mass and effective hydrated MW
- Dilution mode: stock and target concentration (`M`, `mM`, `uM`, `nM`); stock volume, diluent volume, and dilution factor
- Serial mode: step count, final volume per tube in µL, concentration and transfer/diluent volumes at each step
- Plain-language `protocol_steps` with every run
- Manifest and named examples: `get_manifest`, `list_examples`, `get_example_input`
- CLI: `pepkio-molarity-solution-calculator manifest` and `run`
- Configuration via `PEPKIO_API_KEY` and `PEPKIO_API_BASE_URL`

# Installation

```bash
pip install pepkio-molarity-solution-calculator
```

Set an API key with **tools:run** scope before calling `run()`:

```bash
export PEPKIO_API_KEY="your-key"
```

Create a key in your [Pepkio account API keys](https://www.pepkio.com/account/api-keys) settings.

# Quick Example

```python
from pepkio_molarity_solution_calculator import PepkioClient

with PepkioClient() as client:
    inp = client.get_example_input("powder_cuso4")
    result = client.run(inp)
    print(result.result["result"]["mass_display"])
    for step in result.result["protocol_steps"]:
        print(step)
```

CLI:

```bash
pepkio-molarity-solution-calculator run --example powder_cuso4
```

Manifest inspection does not require an API key.

# Typical Use Cases

- Weighing hydrated salts for stock solutions (for example CuSO₄·5H₂O at labeled purity)
- Diluting concentrated buffers (for example 10× PBS to 1× in a defined final volume)
- Quick serial dilution estimates (for example 1 M to 1 µM in four steps)
- Cell culture media and reagent stock preparation
- Standard curve and qPCR template dilution planning before bench work
- Scripting repeatable solution prep in notebooks or lab automation pipelines

# Scientific Background

To prepare a solution from solid: **mass (g) = M × V (L) × MW (g/mol)**. For hydrated salts, use the effective molecular weight that includes crystal water. Adjust mass upward when bottle purity is below 100%.

For a single dilution, **C₁V₁ = C₂V₂** relates stock concentration, final concentration, and volumes. Dilution factor DF = C_stock / C_final.

In serial dilution with constant ratio DF per step, concentration after n steps is **Cₙ = C₀ / DFⁿ**. The `serial` mode returns ideal transfer volumes; for pipette-aware rounding and plate maps, use the Pepkio Serial Dilution Planner web tool.

# Web Application

For researchers who prefer a graphical interface, an interactive [Molarity Solution Calculator](https://www.pepkio.com/tools/molarity-solution-calculator) is available in the browser.

The web interface adds live results as you type, saved recipes for buffers you prepare regularly, shareable links that restore inputs, one-click handoff from powder result to dilution tab, printable worksheets, and warnings when serial volumes are below practical pipetting limits (with a link to the Serial Dilution Planner).

# Documentation and Resources

Source code and issue tracking: [github.com/pepkio/pepkio-molarity-solution-calculator](https://github.com/pepkio/pepkio-molarity-solution-calculator)

Web application: [pepkio.com/tools/molarity-solution-calculator](https://www.pepkio.com/tools/molarity-solution-calculator)

# About Pepkio

Pepkio develops software tools and provides bioinformatics analysis services for life science research. See https://www.pepkio.com for additional tools and services.

# Keywords

molarity calculator, molarity solution calculator, solution preparation calculator, powder to solution, mass from molarity, hydrate correction, hydrated salt molarity, purity correction, C1V1=C2V2, dilution calculator, stock dilution volume, dilution factor, buffer dilution, serial dilution calculator, mM to uM dilution, standard curve preparation, qPCR dilution, cell culture media preparation, laboratory protocol, effective molecular weight, pepkio-molarity-solution-calculator, Python molarity API, lab automation solution prep, how much powder to weigh for mM solution, molarity calculator with hydrate correction, adjust mass for reagent purity, how to dilute 10x buffer to 1x, calculate stock and diluent volumes, make CuSO4 5H2O stock solution, quick serial dilution 1 M to 1 uM, Python script calculate powder mass molarity, API for laboratory solution preparation, shareable link restore solution prep parameters, common mistakes weighing hydrated salts
