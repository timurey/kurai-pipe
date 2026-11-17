# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

KURAI Pipe is an open-hardware solar Meshtastic node on LTO cells, sized for a 50 mm pipe. It is a rework of MASN V2.0 HT-RA62 by EA1REX. There is **no software, build system or tests** here: the repo holds the KiCad project, its local libraries and the licence/attribution files.

## Layout

- `pcb/kurai-pipe/kicad/` — KiCad 10 project `masn-v2-htra62-lto.kicad_pro` (schematic, board, local footprint library `masn.pretty`, 3D models `masn.3dshapes`).
- `pcb/kurai-pipe/NOTICE.md` — modification notice required by CERN-OHL-S v2 (original author, source, list of changes, our source location).
- `LICENSE.txt` — CERN-OHL-S v2. `TODO.md` — open items.
- `**/raw/` is git-ignored and is where working files go.

## Working with the project

- Files are in the **KiCad 10** format; older KiCad will not open them.
- Refs are annotated; "Update PCB from Schematic" must run **without** "re-link by reference" (that option breaks UUID paths and duplicates footprints).
- The user places and routes vias himself (based on the Faketec layout) — do not add vias unless asked.
- Check for `*.lck` files before writing `.kicad_sch` / `.kicad_pcb`; if KiCad has the project open, ask the user to close it first.
- Silkscreen text is **Russian**, documentation is **English**.
- Keep the licence notices intact: title blocks, `NOTICE.md`, the bottom-silkscreen notice (author, modification, source link).
