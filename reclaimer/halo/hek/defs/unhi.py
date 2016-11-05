from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef
from .grhi import multitex_overlay, hud_background

warning_sound = Struct("warning sound",
    dependency("sound", ('lsnd', 'snd!')),
    BBool32("latched to",
        "shield recharging",
        "shield recharged",
        "shield low",
        "shield empty",
        "health low",
        "health empty",
        "health minor damage",
        "health major damage",
        ),
    BFloat("scale"),
    SIZE=56
    )

shield_panel_meter = Struct("shield panel meter",
    QStruct("anchor offset",
        BSInt16("x"),
        BSInt16("y"),
        ),
    BFloat("width scale"),
    BFloat("height scale"),
    BBool16("scaling flags", *hud_scaling_flags),

    Pad(22),
    dependency("meter bitmap", "bitm"),
    Pad(1),
    QStruct("color at meter minimum", INCLUDE=rgb_byte),
    Pad(1),
    QStruct("color at meter maximum", INCLUDE=rgb_byte),
    Pad(1),
    QStruct("flash color", INCLUDE=rgb_byte),
    QStruct("empty color", INCLUDE=argb_byte),
    Bool8("flags", *hud_panel_meter_flags),
    SInt8("minimum meter value"),
    BSInt16("sequence index"),
    SInt8("alpha multiplier"),
    SInt8("alpha bias"),
    BSInt16("value scale"),
    BFloat("opacity"),
    BFloat("translucency"),
    QStruct("disabled color", INCLUDE=argb_byte),
    Pad(17),
    QStruct("overcharge minimum color", INCLUDE=rgb_byte),
    Pad(1),
    QStruct("overcharge maximum color", INCLUDE=rgb_byte),
    Pad(1),
    QStruct("overcharge flash color", INCLUDE=rgb_byte),
    Pad(1),
    QStruct("overcharge empty color", INCLUDE=rgb_byte),
    SIZE=136
    )

health_panel_meter = Struct("health panel meter",
    QStruct("anchor offset",
        BSInt16("x"),
        BSInt16("y"),
        ),
    BFloat("width scale"),
    BFloat("height scale"),
    BBool16("scaling flags", *hud_scaling_flags),

    Pad(22),
    dependency("meter bitmap", "bitm"),
    Pad(1),
    QStruct("color at meter minimum", INCLUDE=rgb_byte),
    Pad(1),
    QStruct("color at meter maximum", INCLUDE=rgb_byte),
    Pad(1),
    QStruct("flash color", INCLUDE=rgb_byte),
    QStruct("empty color", INCLUDE=argb_byte),
    Bool8("flags", *hud_panel_meter_flags),
    SInt8("minimum meter value"),
    BSInt16("sequence index"),
    SInt8("alpha multiplier"),
    SInt8("alpha bias"),
    BSInt16("value scale"),
    BFloat("opacity"),
    BFloat("translucency"),
    QStruct("disabled color", INCLUDE=argb_byte),
    Pad(17),
    QStruct("medium health left color", INCLUDE=rgb_byte),
    BFloat("max color health fraction cutoff"),
    BFloat("min color health fraction cutoff"),
    SIZE=136
    )

motion_sensor_center = Struct("motion sensor center",
    QStruct("anchor offset",
        BSInt16("x"),
        BSInt16("y"),
        ),
    BFloat("width scale"),
    BFloat("height scale"),
    BBool16("scaling flags", *hud_scaling_flags),
    SIZE=16
    )

auxilary_overlay = Struct("auxilary overlay",
    Struct("background", INCLUDE=hud_background),
    BSEnum16("type",
        "team icon"
        ),
    BBool16("flags",
        "use team color"
        ),
    SIZE=0
    )

auxilary_meter = Struct("auxilary meter",
    Pad(18),
    Pad(2),  # BSEnum16("type", "integrated light"),
    Struct("background", INCLUDE=hud_background),

    QStruct("anchor offset",
        BSInt16("x"),
        BSInt16("y"),
        ),
    BFloat("width scale"),
    BFloat("height scale"),
    BBool16("scaling flags", *hud_scaling_flags),

    Pad(22),
    dependency("meter bitmap", "bitm"),
    Pad(1),
    QStruct("color at meter minimum", INCLUDE=rgb_byte),
    Pad(1),
    QStruct("color at meter maximum", INCLUDE=rgb_byte),
    Pad(1),
    QStruct("flash color", INCLUDE=rgb_byte),
    QStruct("empty color", INCLUDE=argb_byte),
    Bool8("flags", *hud_panel_meter_flags),
    SInt8("minimum meter value"),
    BSInt16("sequence index"),
    SInt8("alpha multiplier"),
    SInt8("alpha bias"),
    BSInt16("value scale"),
    BFloat("opacity"),
    BFloat("translucency"),
    QStruct("disabled color", INCLUDE=argb_byte),

    Pad(16),
    BFloat("minimum fraction cutoff"),
    Bool32("overlay flags",
        "show only when active",
        "flash once if activated while disabled",
        ),

    SIZE=324
    )

unhi_body = Struct("tagdata",
    BSEnum16("anchor", *hud_anchors),

    Pad(34),
    Struct("unit hud background", INCLUDE=hud_background),
    Struct("shield panel background", INCLUDE=hud_background),
    shield_panel_meter,
    Struct("health panel background", INCLUDE=hud_background),
    health_panel_meter,
    Struct("motion sensor background", INCLUDE=hud_background),
    Struct("motion sensor foreground", INCLUDE=hud_background),

    Pad(32),
    motion_sensor_center,

    Pad(20),
    BSEnum16("auxilary overlay anchor", *hud_anchors),
    Pad(34),
    reflexive("auxilary overlays", auxilary_overlay, 16),

    Pad(16),
    reflexive("warning sounds", warning_sound, 12),
    reflexive("auxilary meters", auxilary_meter, 16),

    SIZE=1388
    )

    
def get():
    return unhi_def

unhi_def = TagDef("unhi",
    blam_header("unhi"),
    unhi_body,

    ext=".unit_hud_interface", endian=">",
    )
