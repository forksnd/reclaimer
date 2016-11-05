from .shdr import *
from supyr_struct.defs.tag_def import TagDef

spla_attrs = Struct("spla attrs",
    Pad(4),
    #Intensity
    BSEnum16("intensity source", *function_outputs),
    Pad(2),
    BFloat("intensity exponent"),

    #Offset
    BSEnum16("offset source", *function_outputs),
    Pad(2),
    BFloat("offset amount"),
    BFloat("offset exponent"),

    Pad(32),

    #Color
    BFloat("perpendicular brightness", MIN=0.0, MAX=1.0),
    QStruct("perpendicular tint color", INCLUDE=rgb_float),
    BFloat("parallel brightness", MIN=0.0, MAX=1.0),
    QStruct("parallel tint color", INCLUDE=rgb_float),
    BSEnum16("tint color source", *function_names),

    Pad(62),
    #Primary Noise Map
    BFloat("primary animation period"),
    QStruct("primary animation direction", INCLUDE=ijk_float),
    BFloat("primary noise map scale"),
    dependency("primary noise map", "bitm"),

    Pad(36),
    #Secondary Noise Map
    BFloat("secondary animation period"),
    QStruct("secondary animation direction", INCLUDE=ijk_float),
    BFloat("secondary noise map scale"),
    dependency("secondary noise map", "bitm"),
    SIZE=292
    )

spla_body = Struct("tagdata",
    shdr_attrs,
    spla_attrs,
    SIZE=332,
    )


def get():
    return spla_def

spla_def = TagDef("spla",
    blam_header('spla'),
    spla_body,

    ext=".shader_transparent_plasma", endian=">"
    )
