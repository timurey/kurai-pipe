# TODO

Open items before KURAI Pipe can be called fabrication-ready.

## Schematic and PCB

- [ ] Wire J2 (GPS) power pads in the schematic. After the GPS power switch was removed, `GPS_GND` and `GPS_VCC` are single-ended global labels; decide whether the pads go straight to GND/+3.3 V or keep a switch.
- [ ] Delete the leftover schematic note about Q1/JP2/JP3 — that circuit is no longer on the sheet.
- [ ] Update the PCB from the schematic: J2 is missing on the board, and the board's reference/net state has to be checked against the schematic.
- [ ] Remove the `GPS_EN` label if the switch is gone for good.
- [ ] Run DRC with the fab limits and fix leftovers (stale ratsnest: P0.31, VCC_MCU ×2, MPPT VIN/BAT, R1→BAT+).
- [ ] Rename the project files `masn-v2-htra62-lto.*` → `kurai-pipe.*`.

## Fabrication

- [ ] Export Gerbers, drill files, BOM, pick-and-place and STEP into `fabrication/`.
- [ ] Check panelisation if the boards are ordered as a panel.

## Media

- [ ] Make own board renders and photos (top and bottom) — the MASN images were removed with the upstream files.
- [ ] Make a 3D-printable pipe mount/enclosure and add the STEP/STL.
