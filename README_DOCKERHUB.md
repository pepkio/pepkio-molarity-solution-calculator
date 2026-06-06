# Pepkio Molarity Solution Calculator

Run the Pepkio Molarity Solution Calculator CLI in a fixed container environment to obtain weighed masses, dilution volumes, and serial step tables through the hosted API.

# What It Does

The image runs `pepkio-molarity-solution-calculator`, a client for the Pepkio Molarity Solution Calculator REST API. It supports three calculation modes: powder mass from solid reagent (with hydrate and purity correction), single-step dilution (C₁V₁ = C₂V₂), and multi-step serial dilution tables with plain-language protocol steps and shareable permalinks.

Typical workflows include buffer and media preparation, weighing hydrated salts for stock solutions, diluting concentrated stocks to working concentration, and quick serial dilution estimates for standard curves or qPCR setup. Calculator logic runs on Pepkio servers; provide a network connection and API key for `run` commands.

# Features

- Three modes: `powder`, `dilution`, and `serial`
- Powder mode: anhydrous molecular weight, hydrate notation (e.g. ·5H₂O), and supplier purity percent
- Dilution mode: stock and target concentration (`M`, `mM`, `uM`, `nM`); stock volume, diluent volume, and dilution factor
- Serial mode: step count, per-tube volume in µL, concentration and transfer/diluent volumes at each step
- Plain-language `protocol_steps` returned with every run
- Named manifest examples (e.g. `powder_cuso4`, `dilution_pbs_10x`, `serial_1M_to_1uM`)
- Manifest inspection without an API key

# Quick Start

```bash
docker pull pepkio/molarity-solution-calculator:0.1.0
docker run --rm -e PEPKIO_API_KEY="your-key" pepkio/molarity-solution-calculator:0.1.0 \
  pepkio-molarity-solution-calculator run --example powder_cuso4
```

Manifest only (no API key):

```bash
docker run --rm pepkio/molarity-solution-calculator:0.1.0 \
  pepkio-molarity-solution-calculator manifest --examples
```

Set `PEPKIO_API_BASE_URL` to override the API host (default: `https://tools.pepkio.com`). Create an API key with **tools:run** scope at https://www.pepkio.com/account/api-keys.

# Quick Example

```bash
docker run --rm -e PEPKIO_API_KEY="$PEPKIO_API_KEY" pepkio/molarity-solution-calculator:0.1.0 \
  pepkio-molarity-solution-calculator run --input-json \
  '{"mode":"dilution","stock_concentration":10,"stock_unit":"M","target_concentration":1,"target_unit":"M","final_volume":1,"final_volume_unit":"L"}'
```

# Typical Use Cases

- Weighing hydrated salts for stock solutions (for example CuSO₄·5H₂O at labeled purity)
- Diluting concentrated buffers (for example 10× PBS to 1× in a defined final volume)
- Quick serial dilution estimates (for example 1 M to 1 µM in four steps)
- Cell culture media and reagent stock preparation
- CI or workflow runners that need a fixed client environment

# Scientific Background

To prepare a solution from solid: **mass (g) = M × V (L) × MW (g/mol)**. For hydrated salts, use the effective molecular weight that includes crystal water; adjust mass upward when bottle purity is below 100%.

For a single dilution, **C₁V₁ = C₂V₂** relates stock concentration, final concentration, and volumes. In serial dilution with constant ratio DF per step, concentration after n steps is **Cₙ = C₀ / DFⁿ**.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/molarity-solution-calculator

The web UI adds live results as you type, saved recipes for buffers you prepare regularly, shareable links that restore inputs, one-click handoff from powder result to dilution tab, printable worksheets, and warnings when serial volumes are below practical pipetting limits.

# Documentation and Resources

GitHub Repository: https://github.com/pepkio/pepkio-molarity-solution-calculator

Web Application: https://www.pepkio.com/tools/molarity-solution-calculator

PyPI package: https://pypi.org/project/pepkio-molarity-solution-calculator/

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services.
