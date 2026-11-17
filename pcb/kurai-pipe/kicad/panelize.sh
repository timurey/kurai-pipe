#!/bin/bash


kikit panelize \
    --layout 'grid; rows: 1; cols: 2; space: 2mm' \
    --tabs 'fixed; width: 5mm; hcount: 3' \
    --cuts 'mousebites; drill: 0.5mm; spacing: 1mm; offset: 0.2mm; prolong: 0.5mm' \
    --post 'millradius: 1mm' \
    kurai-pipe.kicad_pcb output.kicad_pcb

echo "more examples at https://yaqwsx.github.io/KiKit/latest/panelization/scripting/"
