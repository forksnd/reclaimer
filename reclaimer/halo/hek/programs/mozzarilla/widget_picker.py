from supyr_struct.apps.binilla.widget_picker import *
from supyr_struct.apps.binilla.field_widgets import *
from ....field_types import *

__all__ = ("WidgetPicker", "def_widget_picker", "add_widget",
           "MozzarillaWidgetPicker", "def_halo_widget_picker")

class MozzarillaWidgetPicker(WidgetPicker):
    pass

def_halo_widget_picker = dhwp = MozzarillaWidgetPicker()

dhwp.add_widget(StringVarLen, NullFrame)  # PLACEHOLDER

dhwp.copy_widget(FlUTF16StrData, StrUtf16)
dhwp.copy_widget(FlStrUTF16, StrUtf16)

dhwp.copy_widget(FlUInt16, UInt16)
dhwp.copy_widget(FlUInt32, UInt32)
dhwp.copy_widget(FlUEnum16, UEnum16)
dhwp.copy_widget(FlUEnum32, UEnum32)
dhwp.copy_widget(FlBool16, FlBool16)
dhwp.copy_widget(FlBool32, FlBool32)
dhwp.copy_widget(FlSInt16, SInt16)
dhwp.copy_widget(FlSInt32, SInt32)
dhwp.copy_widget(FlSEnum16, SEnum16)
dhwp.copy_widget(FlSEnum32, SEnum32)

dhwp.copy_widget(RawdataRef, Struct)
dhwp.copy_widget(Reflexive, Struct)
dhwp.copy_widget(TagIndexRef, Struct)

dhwp.copy_widget(TagIndex, Array)
dhwp.copy_widget(Rawdata, BytearrayRaw)
dhwp.copy_widget(StrLatin1Enum, SEnum32)
