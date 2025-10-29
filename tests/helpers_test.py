from app.kamstrup_modbus import KamstrupMBusClient as K

def test_last_part_basic():
    assert K._last_part("VIFUnit.ENERGY_WH") == "ENERGY_WH"
    assert K._last_part("MeasureUnit.M3_H") == "M3_H"
    assert K._last_part("NoDots") == "NoDots"

def test_last_part_non_string():
    assert K._last_part(None) == "None"
    assert K._last_part(123) == "123"

def test_norm_basic():
    assert K._norm("VIFUnit.ENERGY_WH") == "energy_wh"
    assert K._norm("MeasureUnit.M3_H") == "m3_h"
    assert K._norm("Temp.DIFF°C") == "diff_c"
    assert K._norm(None) == "none"

def test_unit_suffix_and_merge():
    assert K._unit_suffix("MeasureUnit.NONE") == ""
    assert K._unit_suffix("MeasureUnit.WH") == "wh"
    assert K._unit_suffix(None) == ""

    assert K._merge_unit("energy_kwh", "wh") == "energy_kwh"
    assert K._merge_unit("volume", "m3") == "volume_m3"
    assert K._merge_unit("volume_m3", "m3") == "volume_m3"
    assert K._merge_unit(None, "m3") == None
    assert K._merge_unit("power", None) == "power"
