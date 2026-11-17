# KURAI Pipe — notices

KURAI Pipe is a solar Meshtastic node on LTO cells, sized to fit inside a 50 mm pipe. It is a modified version of the MASN V2.0 HT-RA62 board.

## Original work

- **MASN V2.0 (HT-RA62 variant)**
- Author: Daniel Pereyra Costas (EA1REX)
- Source: <https://github.com/danielcharrua/masn-meshtastic-autonomous-solar-node>
- Licence: CERN-OHL-S v2

The original board notices ("MESH AUTONOMOUS SOLAR NODE", "HT-RA62 V2.0 | 04/2026 | By EA1REX" and the MASN logo) are kept in the PCB file.

## Modification notice (CERN-OHL-S v2, section 3.3 b)

Modified in October 2026 by timurey (2026-10-10 … 2026-10-13):

- **KiCad port.** The design was ported from the EasyEDA Standard sources to KiCad 9; the project files are now saved with KiCad 10.
- **Power path for LTO cells (1S 2.7 V / 2S 5.4 V):**
  - The CN3791 charger was replaced by an SD30CRMA (CN3795) MPPT module.
  - A TPS63802 buck-boost module set to 4.2 V (330 kΩ across the module's voltage-select pads) now feeds the MCU. The ProMicro/nice!nano has its own 3.3 V LDO after B+, so its input needs headroom above 3.3 V.
  - The MCP1321 supervisor and the AO3407A were removed. Low-battery handling is done in firmware (LPCOMP).
  - JP1 "2S DIRECT" was added.
- **Board for a 50 mm pipe:**
  - The board is now 39 × 99 mm.
  - The modules are mounted flat as SMD parts, and the INA3221 and BME280 are on the bottom.
  - The board has three M2.5 mounting holes.
- **Additions:**
  - decoupling capacitors on 3.3 V and on the VBAT ADC;
  - RESET and USER buttons;
  - 2.54 mm wire pads for a GPS module and a second serial port;
  - a BLE antenna keepout zone;
  - assembly notes on the silkscreen.
- **New name and logos:** the board was renamed to KURAI Pipe and given new logos.

## Source location (CERN-OHL-S v2, section 3.3 c)

<https://github.com/timurey/kurai-pipe> — `pcb/kurai-pipe/`

## Licence

This modified design is licensed under the CERN Open Hardware Licence Version 2 – Strongly Reciprocal (CERN-OHL-S v2). The full text is in [`LICENSE.txt`](../../LICENSE.txt). It is provided WITHOUT ANY EXPRESS OR IMPLIED WARRANTY. See sections 6 and 7 of the licence.

If you make and distribute boards from this design, keep these notices. Also keep the notice on the bottom silkscreen (licence, original author, modification and source location) or another way of telling recipients where the source is.
