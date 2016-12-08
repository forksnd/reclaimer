from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef


scenario_description = Struct("scenario description",
    dependency("descriptive bitmap", "bitm"),
    dependency("displayed map name", "ustr"),
    ascii_str32("scenario tag directory path"),
    SIZE=68
    )

mply_body = Struct("tagdata",
    reflexive("multiplayer scenario descriptions",
              scenario_description, 32),
    SIZE=12,
    )


def get():
    return mply_def

mply_def = TagDef("mply",
    blam_header('mply'),
    mply_body,

    ext=".multiplayer_scenario_description", endian=">"
    )
