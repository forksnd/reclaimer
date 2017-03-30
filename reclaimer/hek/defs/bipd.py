from .objs.tag import HekTag
from .obje import *
from .unit import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=0)

contact_point = Struct("contact point",
    Pad(32),
    ascii_str32('marker name'),
    SIZE=64
    )

bipd_attrs = Struct("bipd attrs",
    BFloat("moving turning speed",
        SIDETIP="degrees/sec", UNIT_SCALE=180/pi),  # radians
    BBool32("flags",
        "turns without aiming",
        "uses player physics",
        "physics pill centered at origin",
        "spherical",
        "passes through other bipeds",
        "can climb any surface",
        "immune to falling damage",
        "rotate while airborne",
        "uses limp body physics",
        "has no dying airborne",
        "random speed increase",
        "uses old player physics",
        ),
    float_rad("stationary turning threshold"),  # radians

    Pad(16),
    BSEnum16('A in', *biped_inputs),
    BSEnum16('B in', *biped_inputs),
    BSEnum16('C in', *biped_inputs),
    BSEnum16('D in', *biped_inputs),
    dependency('DONT USE', "jpt!"),

    ####################################################
    #####                   IMPORTANT              #####
    ##### Because of how halo handles some things, #####
    ##### the below accelerations unit scales for  #####
    ##### 60fps must be cut by 2 rather than 4     #####
    ####################################################
    QStruct("flying",
        float_rad("bank angle"),  # radians
        float_sec("bank apply time", UNIT_SCALE=sec_unit_scale),  # seconds
        float_sec("bank decay time", UNIT_SCALE=sec_unit_scale),  # seconds
        BFloat("pitch ratio"),
        float_wu_sec("max velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        float_wu_sec("max sidestep velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        float_wu_sec_sq("acceleration",
                        UNIT_SCALE=per_sec_unit_scale),  # world units/second^2
        float_wu_sec_sq("deceleration",
                        UNIT_SCALE=per_sec_unit_scale),  # world units/second^2
        float_rad_sec("angular velocity maximum"),  # radians/second
        float_rad_sec_sq("angular acceleration maximum"),  # radians/second^2
        float_zero_to_one("crouch velocity modifier"),
        ),

    Pad(8),
    Struct("movement",
        float_rad("maximum slope angle"),  # radians
        float_rad("downhill falloff angle"),  # radians
        float_rad("downhill cutoff angle"),  # radians
        BFloat("downhill velocity scale"),
        float_rad("uphill falloff angle"),  # radians
        float_rad("uphill cutoff angle"),  # radians
        BFloat("uphill velocity scale"),

        Pad(24),
        dependency('footsteps', "foot"),
        ),

    Pad(24),
    QStruct("jumping and landing",
        float_wu_sec("jump velocity", UNIT_SCALE=per_sec_unit_scale),
        Pad(28),
        float_sec("maximum soft landing time", UNIT_SCALE=sec_unit_scale),
        float_sec("maximum hard landing time", UNIT_SCALE=sec_unit_scale),
        float_wu_sec("minimum soft landing velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        float_wu_sec("minimum hard landing velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        float_wu_sec("maximum hard landing velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        float_wu_sec("death hard landing velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        ),

    Pad(20),
    QStruct("camera, collision, and autoaim",
        float_wu("standing camera height"),
        float_wu("crouching camera height"),
        float_sec("crouch transition time", UNIT_SCALE=sec_unit_scale),

        Pad(24),
        float_wu("standing collision height"),
        float_wu("crouching collision height"),
        float_wu("collision radius"),

        Pad(40),
        float_wu("autoaim width"),
        ),

    Pad(108),
    QStruct("unknown struct",
        FlFloat("unknown1", DEFAULT=1.0),
        FlFloat("unknown2", DEFAULT=1.0),
        FlFloat("unknown3", DEFAULT=1.0),
        FlFloat("unknown4", DEFAULT=-0.0),
        FlFloat("unknown5", DEFAULT=-0.0),
        FlFloat("unknown6", DEFAULT=0.0),
        FlFloat("unknown7", DEFAULT=0.0),
        FlSInt16("unknown8", DEFAULT=-1),
        FlSInt16("unknown9", DEFAULT=-1),
        COMMENT=(
            "\nI think these are physics values, but I havent experimented.\n" +
            "If they are, they probably include a normal k0 and k1 like\n" +
            "you'd find oin a physics tag, which determine the maximum\n" +
            "angles the biped can go up a slope before sliding.\n"
            )
        ),

    reflexive("contact points", contact_point, 2,
        DYN_NAME_PATH='.marker_name'),
    
    SIZE=516
    )

bipd_body = Struct("tagdata",
    obje_attrs,
    unit_attrs,
    bipd_attrs,
    SIZE=1268,
    )


def get():
    return bipd_def

bipd_def = TagDef("bipd",
    blam_header('bipd', 3),
    bipd_body,

    ext=".biped", endian=">", tag_cls=HekTag
    )
