# TODO

Open items before KURAI Pipe can be called fabrication-ready.

## Schematic and PCB

- [x] Drop the GPS connector: J2, the `GPS_*` labels, the stale Q1/JP2/JP3 note and the J2 line in the silkscreen note are gone from the schematic.
- [ ] Update the PCB from the schematic; the board still carries the old `GPS_TX`/`GPS_RX`/`GPS_EN` net names (no pads use them) and has to be checked against the schematic.
- [ ] Run DRC with the fab limits and fix leftovers (stale ratsnest: P0.31, VCC_MCU ×2, MPPT VIN/BAT, R1→BAT+).
- [ ] Rename the project files `masn-v2-htra62-lto.*` → `kurai-pipe.*`.

## Fabrication

- [ ] Export Gerbers, drill files, BOM, pick-and-place and STEP into `fabrication/`.
- [ ] Check panelisation if the boards are ordered as a panel.

## Media

- [ ] Make own board renders and photos (top and bottom) — the MASN images were removed with the upstream files.
- [ ] Make a 3D-printable pipe mount/enclosure and add the STEP/STL.
