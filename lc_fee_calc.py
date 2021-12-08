import rhinoscriptsyntax as rs
from System.Drawing import Color

ENGRAVE_COLOR = Color.FromArgb(0,0,0)
CUTTING_COLOR = Color.FromArgb(0,255,0)
# at 100% in mm/s
CUTTER_SPEED = 100
# Acrylic: 1, Chipboard: 2, Paperboard: 3
material_input = rs.GetInteger("Material: 0=Acrylic, 1=Chipboard, 2=Paperboard")
MATERIAL_LIST = ("acrylic", "chipboard", "paperboard")
MATERIAL = MATERIAL_LIST[material_input]
# Material Thickness in mm
THICKNESS = rs.GetInteger("Material thickness in mm")

total_engraving_length = 0
total_cutting_length = 0

layers = rs.LayerIds()

for layer in layers:
    if rs.LayerPrintColor(layer)== ENGRAVE_COLOR:
        layer_type = "E"
    elif rs.LayerPrintColor(layer)== CUTTING_COLOR:
        layer_type = "C"
    else:
        continue
        
    guids = rs.ObjectsByLayer(layer, False)
    layer_curve_length = 0
    for guid in guids:
        if rs.ObjectType(guid) == 4:
            layer_curve_length += rs.CurveLength(guid)
    
    if layer_type == "C":
        total_cutting_length += layer_curve_length
    elif layer_type == "E":
        total_engraving_length += layer_curve_length

# print(total_engrave_length, total_cutting_length)
# L * THICKNESS * MAT / SPEED
MAT_FACTOR = {
    "acrylic":1,
    "chipboard":1,
    "paperboard":1
}

equivalent_speed = CUTTER_SPEED / (MAT_FACTOR[MATERIAL]*THICKNESS)
equivalent_cutting_time = total_cutting_length / equivalent_speed

# As for engraving, we use a constant speed to calculate the fee
# no matter what parameters are actually used.
equivalent_cutting_time += total_engraving_length / CUTTER_SPEED

# Finally, we multiply the price with the operatiing factor to 
# cover the other expense of Maker Space laser cutters.

OPERATING_COST_FACTOR = 1.1

UNIT_PRICE = 5
fee = round(equivalent_cutting_time * UNIT_PRICE * OPERATING_COST_FACTOR, 0)

print(
    "{}mm {}\nTotal cutting length is {}mm\nTotal engraving length is {}mm\nCutting fee is NTD${}".format(
        THICKNESS,
        MATERIAL,
        round(total_cutting_length, 0),
        round(total_engraving_length, 0),
        fee
    )
)