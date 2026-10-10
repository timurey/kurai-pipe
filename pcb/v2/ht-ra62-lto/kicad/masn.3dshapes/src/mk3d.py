"""Build/convert 3D models for the masn footprint library.

Every model is produced directly in its footprint's frame: X = footprint x, Y = -footprint y,
Z up, our board's top surface at Z = 0. Footprints then reference them with zero offset/rotation.
"""
import math
import os
import sys

import cadquery as cq

OUT = sys.argv[1]
GY_STEP = sys.argv[2]
INA_STEP = sys.argv[3]
os.makedirs(OUT, exist_ok=True)

C = {  # colours
    "pcb_black": cq.Color(0.08, 0.08, 0.08), "pcb_purple": cq.Color(0.42, 0.18, 0.55),
    "pcb_blue": cq.Color(0.05, 0.25, 0.6), "gold": cq.Color(0.85, 0.7, 0.3),
    "ic": cq.Color(0.1, 0.1, 0.1), "metal": cq.Color(0.75, 0.75, 0.78), "ind": cq.Color(0.25, 0.25, 0.27),
    "cap": cq.Color(0.2, 0.3, 0.2), "trim": cq.Color(0.15, 0.35, 0.8), "ceramic": cq.Color(0.6, 0.5, 0.35),
    "white": cq.Color(0.92, 0.92, 0.9), "terminal": cq.Color(0.1, 0.35, 0.75), "plastic": cq.Color(0.15, 0.15, 0.15),
}


def box(x, y, z0, dx, dy, dz):
    """Axis-aligned box centred on (x, y) in plan, from z0 up by dz."""
    return cq.Workplane("XY").box(dx, dy, dz, centered=(True, True, False)).translate((x, y, z0))


def cyl(x, y, z0, r, h):
    return cq.Workplane("XY").circle(r).extrude(h).translate((x, y, z0))


def save(name, parts):
    a = cq.Assembly(name=name)
    for i, (shape, colour) in enumerate(parts):
        a.add(shape, name=f"p{i}", color=C[colour])
    a.save(os.path.join(OUT, name + ".step"), "STEP")
    print("saved", name)


def pcb(w, h, t, z0=0.0, holes=(), x=0.0, y=0.0):
    p = box(x, y, z0, w, h, t)
    for hx, hy, r in holes:
        p = p.cut(cyl(hx, hy, z0 - 1, r, t + 2))
    return p


# ---------------------------------------------------------------- SD30CRMA (CN3795), flat, VIN end at -X
def sd30(z0):
    t = 1.6
    holes = [(sx * 20.5, y3, 0.55) for sx in (-1, 1) for y3 in (2.08, -3.0)]          # pin holes (Y = -fp y)
    holes += [(sx * 20.0, sy * 7.5, 1.5) for sx in (-1, 1) for sy in (-1, 1)]           # corner mounting holes
    top = z0 + t
    parts = [(pcb(45, 20, t, z0, holes), "pcb_black")]
    parts += [(box(sx * 20.5, y3, top, 2.4, 2.4, 0.04), "gold") for sx in (-1, 1) for y3 in (2.08, -3.0)]
    parts += [
        (box(7.5, -0.5, top, 10.0, 10.0, 4.5), "ind"),                 # 47 uH power inductor
        (cyl(-14.5, 5.5, top, 3.15, 7.0), "cap"),                      # input electrolytic
        (cyl(15.5, 5.5, top, 3.15, 7.0), "cap"),                       # output electrolytic
        (box(-0.5, -3.0, top, 4.8, 9.5, 4.8), "trim"),                 # CV trimmer
        (box(-7.0, -3.5, top, 5.0, 4.0, 1.6), "ic"),                   # CN3795 SOP-10
        (box(-6.0, 5.0, top, 5.0, 4.0, 1.6), "ic"),                    # P-MOSFET SOP-8
        (box(1.5, 6.5, top, 4.3, 2.6, 2.1), "ic"),                     # Schottky SMA
        (box(15.5, -5.0, top, 3.2, 1.6, 0.6), "white"),                # Rcs
    ]
    return parts


save("SD30CRMA_CN3795_45x20mm", sd30(0.0))


# ---------------------------------------------------------------- Jessinie TPS63802 module, flat
def tps():
    t = 1.0
    holes = [(sx * 3.81, sy * 2.54, 0.5) for sx in (-1, 1) for sy in (-1, 1)]
    parts = [(pcb(10, 8, t, 0, holes), "pcb_black")]
    parts += [(box(sx * 3.81, sy * 2.54, t, 1.6, 1.6, 0.04), "gold") for sx in (-1, 1) for sy in (-1, 1)]
    parts += [
        (box(0, 2.6, t, 3.2, 2.5, 1.2), "ind"),
        (box(0, -0.3, t, 2.0, 3.0, 0.8), "ic"),
        (box(-2.4, 0.2, t, 1.0, 2.0, 1.0), "ceramic"), (box(-1.4, 0.2, t, 1.0, 2.0, 1.0), "ceramic"),
        (box(2.4, 0.2, t, 1.0, 2.0, 1.0), "ceramic"), (box(3.4, 0.2, t, 1.0, 2.0, 1.0), "ceramic"),
    ]
    return parts


save("TPS63802_Jessinie_10x8mm", tps())


# ---------------------------------------------------------------- nice!nano / Pro Micro nRF52840, flat
def nicenano():
    t = 1.0
    # board outline from the footprint: x +-9.0, fp y -18.54 .. 15.37  ->  Y 18.54 .. -15.37
    cy = (18.54 - 15.37) / 2
    holes = [(sx * 7.62, -(-16.51 + 2.54 * i), 0.45) for sx in (-1, 1) for i in range(13)]
    parts = [(pcb(18.0, 33.9, t, 0, holes, 0, cy), "pcb_blue")]
    parts += [(cyl(sx * 7.62, -(-16.51 + 2.54 * i), t, 0.75, 0.04), "gold") for sx in (-1, 1) for i in range(13)]
    parts += [
        (box(0, 17.4, t, 8.9, 7.3, 3.2), "metal"),                     # USB-C, overhangs the top edge
        (box(0, 5.0, t, 7.0, 7.0, 0.9), "ic"),                         # nRF52840
        (box(0, -4.5, t, 3.0, 3.0, 1.0), "ic"),                        # charger / LDO
        (box(-3.5, 10.5, t, 2.0, 1.2, 0.6), "white"), (box(3.5, -9.5, t, 2.0, 1.2, 0.6), "white"),
    ]
    return parts


save("NICENANO", nicenano())


# ---------------------------------------------------------------- HT-RA62 (SX1262) castellated module
def htra62():
    parts = [(box(0, 0, 0, 16.0, 16.5, 0.8), "pcb_blue")]
    parts += [(box(-7.0 + 2 * i, sy * 7.75, 0.8, 1.0, 1.0, 0.03), "gold") for i in range(8) for sy in (-1, 1)]
    parts += [(box(0, 0, 0.8, 14.0, 13.5, 1.7), "metal")]              # RF shield can
    return parts


save("HT-RA62", htra62())


# ---------------------------------------------------------------- SS12D10 slide switch, pins at x -4.8/0/4.8
def ss12d10():
    parts = [(box(0, 0, 0, 12.7, 6.6, 6.6), "plastic"), (box(0, 0, 6.6, 2.0, 2.0, 4.0), "plastic")]
    parts += [(box(x, 0, -3.5, 0.7, 0.4, 3.5), "metal") for x in (-4.8, 0, 4.8)]
    return parts


save("SW_SS12D10", ss12d10())


# ---------------------------------------------------------------- PA001-2P 5.08 mm screw terminal
def pa001():
    # body: footprint x +-5.08, fp y -3.13 .. 5.13 -> Y 3.13 .. -5.13; wire entry faces -Y (the board edge)
    body = box(0, -1.0, 0, 10.16, 8.26, 10.0)
    for x in (-2.54, 2.54):
        body = body.cut(box(x, -4.6, 1.5, 3.4, 3.0, 3.4))              # wire entry
        body = body.cut(cyl(x, 0.5, 6.0, 1.7, 5))                      # screw well
    parts = [(body, "terminal")]
    parts += [(cyl(x, 0.5, 7.5, 1.5, 1.5), "metal") for x in (-2.54, 2.54)]
    parts += [(box(x, 0, -3.5, 1.0, 0.6, 3.5), "metal") for x in (-2.54, 2.54)]
    return parts


save("PA001-2P_P5.08mm", pa001())


# ---------------------------------------------------------------- vendor STEP models re-placed into footprint frames
def place(path, name, colour, transform):
    shape = cq.importers.importStep(path)
    shape = transform(shape)
    print("  holes r1.5/1.7:", circle_centres(shape, 1.5)[:6], circle_centres(shape, 1.7)[:6])
    print("  pin holes r0.5:", circle_centres(shape, 0.5)[:8])
    bb = shape.val().BoundingBox()
    print(f"  {name}: bbox x {bb.xmin:.2f}..{bb.xmax:.2f} y {bb.ymin:.2f}..{bb.ymax:.2f} z {bb.zmin:.2f}..{bb.zmax:.2f}")
    save(name, [(shape, colour)])


def rot(*steps, move=(0, 0, 0)):
    """Chain of rotations ((axis), degrees) about the origin, then a translation."""
    def f(s):
        for axis, deg in steps:
            s = s.rotate((0, 0, 0), axis, deg)
        return s.translate(move)
    return f


def circle_centres(shape, r, tol=0.05):
    out = set()
    for e in shape.edges().vals():
        if e.geomType() == "CIRCLE" and abs(e.radius() - r) < tol:
            c = e.Center()
            out.add((round(c.x, 2), round(c.y, 2)))
    return sorted(out)


# GY-BME280 (4-pin): STEP is Z-up. Rotate +90 deg about Z and put the four pins on pads 1-4
# (fp x 10.16, y 6.35/3.81/1.27/-1.27); module PCB bottom (z = 1.4 after the raw move) lifted to 2.5 mm.
place(GY_STEP, "GY-BME280_4pin", "pcb_purple",
      rot(((0, 0, 1), 90), move=(10.16 + 1.5 + 0.32, -6.35 + 3.85, 2.5 + 1.1)))


# CJMCU-3221 (INA3221): imported STEP has its board in the XZ plane (y 2.46..4.06); components and the
# header's plastic body are on the -y side, long pin ends point -y, short ends +y.
#   (x, y, z) -> (-z + 21.95, x - 9.3, -y + 4.06)  = rotX 90, rotZ 90, rotY 180, move
# i.e. component side up, short pin ends down into our board, module PCB resting on it.
# check: mounting holes should land on fp (2.8, 2.57), (2.8, 20.6), (34.8, 20.7) -> 3D Y = -fp y.
# Note the module's own CH1..CH3 silk is reversed w.r.t. the MASN footprint labels.
place(INA_STEP, "CJMCU-3221_INA3221", "pcb_purple",
      rot(((1, 0, 0), 90), ((0, 0, 1), 90), ((0, 1, 0), 180), move=(21.95, -9.9, 4.06)))  # Y -0.6: best fit between header (-1.2) and shunts (-0.6)
