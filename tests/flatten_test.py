from app.kamstrup_modbus import KamstrupMBusClient as K

SAMPLE = {
    "body": {
        "records": [
            {"type": "VIFUnit.ENERGY_WH", "unit": "MeasureUnit.WH", "value": 1925000},
            {"type": "VIFUnit.VOLUME", "unit": "MeasureUnit.M3", "value": 12.34},
            {"type": "VIFUnit.FLOW_TEMPERATURE", "unit": "MeasureUnit.C", "value": 68.53},
            {"type": "VIFUnit.RETURN_TEMPERATURE", "unit": "MeasureUnit.C", "value": 39.01},
            {"type": "VIFUnit.TEMPERATURE_DIFFERENCE", "unit": "MeasureUnit.K", "value": 29.52},
            {"type": "VIFUnit.POWER_W", "unit": "MeasureUnit.W", "value": 2000},
            {"type": "VIFUnit.VOLUME_FLOW", "unit": "MeasureUnit.M3_H", "value": 0.123},
            {"type": "VIFUnit.ON_TIME", "unit": "MeasureUnit.SECONDS", "value": 543210},
            {"type": "VIFUnit.ON_TIME", "unit": "MeasureUnit.SECONDS", "value": 3600}, 
            {"type": "VIFUnit.FABRICATION_NO", "unit": "MeasureUnit.NONE", "value": 123456789},
        ]
    }
}

def test_flatten_basic_energy_to_kwh():
    data = K._flatten_kamstrup(SAMPLE)

    assert data["energy_wh"] == 1925000
    assert data["volume_m3"] == 12.34
    assert data["flow_temperature_c"] == 68.53
    assert data["return_temperature_c"] == 39.01
    assert data["temperature_difference_k"] == 29.52
    assert data["power_w"] == 2000
    assert data["volume_flow_m3_h"] == 0.123
    assert data["on_time_seconds"] == 543210
    assert data["on_time_seconds_2"] == 3600 # duplicate key is _2
    assert data["fabrication_no"] == 123456789
