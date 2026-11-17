# KURAI Pipe

Solar-powered Meshtastic node on LTO cells, built to slide into a 50 mm pipe.

KURAI Pipe is a rework of the [MASN V2.0 HT-RA62](https://github.com/danielcharrua/masn-meshtastic-autonomous-solar-node) board by Daniel Pereyra Costas (EA1REX). The radio (HT-RA62 / SX1262) and the nice!nano-compatible ProMicro nRF52840 stay; the power path, the board shape and the connectors are new.

> **Status:** work in progress. This repository holds the KiCad sources only. There is no fabrication output yet, and the PCB still has to be updated from the schematic — see [TODO.md](TODO.md) for the open items.

## Features

- 39 × 99 mm board (under the 100 mm price step), three M2.5 mounting holes, fits a 50 mm pipe
- 1S (2.7 V) or 2S (5.4 V) LTO pack — **no Li-ion or Na-ion cells**
- SD30CRMA (CN3795) MPPT charger module with a trimmer-set charge voltage
- TPS63802 buck-boost module (set to 4.2 V) feeding the MCU; the ProMicro's own 3.3 V LDO powers the radio and sensors
- JP1 "2S DIRECT" to bypass the converter on 2S builds without the module
- HT-RA62 (SX1262) LoRa module on flat SMD pads
- INA3221 (panel / MPPT output / battery) and BME280 on the bottom side
- I2C header, GPS and second-serial wire pads, RESET and USER buttons
- BLE antenna keepout zone
- Assembly notes on the silkscreen (Russian)

## Power path

```
solar panel ──► SD30CRMA (CN3795, MPPT) ──► LTO pack 1S/2S ──► TPS63802 (4.2 V) ──► ProMicro B+ ──► 3.3 V LDO ──► HT-RA62, INA3221, BME280
```

The ProMicro/nice!nano has its own regulator between B+ and the 3.3 V rail. Feeding B+ with 3.3 V leaves that regulator in dropout — the rail sags to about 3.0 V, which costs radio output power. 4.2 V gives the regulator enough headroom while dissipating less than 5 V would (a 330 kΩ resistor across the TPS63802 module's voltage-select pads sets 4.2 V; the module leaves the factory at 5 V).

On a 1S pack the converter is required. On 2S the converter is optional: without it, close JP1 "2S DIRECT" to feed B+ straight from the pack. Never close JP1 with the TPS63802 module fitted.

## Connectors

| Ref | What | Pins |
| --- | --- | --- |
| J1 | I2C header, 2.54 mm THT | GND, +3.3 V, SCL, SDA |
| J2 | GPS wire pads, 2.54 mm SMD | GND, VCC, TX (P0.20), RX (P0.22) |
| J3 | Second serial port pads, 2.54 mm SMD | GND, +3.3 V, TX (P0.08), RX (P0.06) |
| SOLAR, BATTERY | Screw terminals, 5.08 mm | +, − |
| SOLAR_SW1, NODE_SW1 | SS12D10 slide switches | — |

J2 and J3 are solder pads, not headers, and are excluded from the BOM/CPL. TX/RX cross over: the MCU's TX goes to the module's RX.

## Firmware

A Meshtastic build for this board lives in the author's fork, with the environment `nrf52_promicro_diy-solar-lto-2s`:

- low-battery cutoff and wake-up are handled in firmware (LPCOMP) — there is no hardware supervisor;
- the variant has `MESHTASTIC_EXCLUDE_GPS` and `MESHTASTIC_EXCLUDE_SERIAL` set; both have to be removed before J2/J3 are usable;
- the INA3221 channel labels in the MASN footprint are swapped relative to a CJMCU-3221 module, so the battery is on CH3 and the panel on CH1.

## Assembly notes

These are repeated on the bottom silkscreen (in Russian), because they are easy to get wrong:

- Set the SD30CRMA charge voltage with the ADJ trimmer **before** connecting the pack: 2.70 V for 1S, 5.40 V for 2S.
- MPPT resistor on the SD30CRMA: 16 kΩ for a 9 V panel, 22.1 kΩ for a 12 V panel.
- Pack voltage must not exceed 5.5 V. 2S Li-ion and 2S Na-ion are not allowed.
- Re-solder the SD30CRMA electrolytics lying flat, or the module will not fit the pipe.
- INA3221 must be the version with separate + and − per channel. A module with a common − will short the panel to the battery through the shunt.
- BME280: either the 6-pin or the 4-pin module fits the footprint.
- Battery voltage divider: 1 MΩ / 1 MΩ to P0.31.
- All modules and SMD parts are mounted flat; the INA3221 and BME280 go on the bottom side.

## Repository layout

```
pcb/kurai-pipe/
  NOTICE.md                modification notice and attribution (CERN-OHL-S v2)
  kicad/
    masn-v2-htra62-lto.kicad_pro/.kicad_sch/.kicad_pcb
    masn.pretty/           project footprint library
    masn.3dshapes/         3D models used by the board
LICENSE.txt                CERN-OHL-S v2
TODO.md                    open items
```

Open `pcb/kurai-pipe/kicad/masn-v2-htra62-lto.kicad_pro` with **KiCad 10.0 or newer** (the files are saved in the KiCad 10 format). The project libraries are local, so no extra installation is needed.

## Fabrication

Gerbers, drill files, BOM, pick-and-place and STEP export are not published yet. They will be added once the PCB is updated from the schematic and checked with DRC at the fab limits.

## Credits and licence

KURAI Pipe is based on MASN V2.0 HT-RA62 by Daniel Pereyra Costas (EA1REX), released under the CERN Open Hardware Licence v2 — Strongly Reciprocal. The original notices are kept in the PCB file and in [NOTICE.md](pcb/kurai-pipe/NOTICE.md), and the licence notice is on the bottom silkscreen.

This modified design is licensed under CERN-OHL-S v2 as well; the full text is in [LICENSE.txt](LICENSE.txt). It is provided **without any express or implied warranty** — you build and deploy your own node at your own risk, and you are responsible for complying with local radio regulations.
