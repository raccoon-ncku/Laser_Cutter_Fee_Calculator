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