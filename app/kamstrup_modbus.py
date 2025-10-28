import json
import re
import serial
import meterbus

class KamstrupMBusClient:
    def __init__(
        self,
        port: str,
        address: int,
        baudrate: int = 9600,
        bytesize: int = 8,
        parity: str = "E",
        stopbits: int = 1,
        timeout: float = 0.5
    ):
        self.port = port
        self.address = address
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout

    def read_raw(self) -> dict:
        with serial.Serial(
            self.port,
            self.baudrate,
            self.bytesize,
            self.parity,
            self.stopbits,
            timeout=self.timeout
        ) as ser:
            # Thanks to hansij66
            # https://github.com/hansij66/kamstrup2mqtt/blob/main/kamstrup_mbus.py#L129
            # ACK
            meterbus.send_ping_frame(ser, self.address)
            frame = meterbus.load(meterbus.recv_frame(ser, 1))
            if not isinstance(frame, meterbus.TelegramACK):
                raise RuntimeError("Meterbus did not return TelegramACK")

            # LONG
            meterbus.send_request_frame(ser, self.address)
            frame = meterbus.load(meterbus.recv_frame(ser, meterbus.FRAME_DATA_LENGTH))
            if not isinstance(frame, meterbus.TelegramLong):
                raise RuntimeError("Meterbus did not return TelegramLong")

            kamstrup_json = frame.to_JSON()
            return json.loads(kamstrup_json)

    def read_simple(self, convert_energy_to_kwh: bool = True) -> dict:
        # Get the raw values
        raw = self.read_raw()

        # Translate to more readable format
        return self._flatten_kamstrup(raw, convert_energy_to_kwh=convert_energy_to_kwh)

    # Static helpers
    @staticmethod
    def _last_part(s: str) -> str:
        return s.split(".")[-1].strip() if isinstance(s, str) else str(s)

    @staticmethod
    def _norm(s: str) -> str:
        # 'VIFUnit.ENERGY_WH' -> 'energy_wh'
        return re.sub(r"[^a-z0-9_]+", "_", KamstrupMBusClient._last_part(s).lower())

    @staticmethod
    def _unit_suffix(unit: str) -> str:
        u = KamstrupMBusClient._norm(unit)
        mapping = {
            "wh": "wh",
            "w": "w",
            "m3": "m3",
            "m3_h": "m3_h",
            "c": "c",
            "k": "k",
            "seconds": "seconds",
            "none": "",
        }
        return mapping.get(u, u)

    @staticmethod
    def _merge_unit(key_base: str, unit_suffix: str) -> str:
        if not unit_suffix:
            return key_base
        if key_base.endswith("_" + unit_suffix) or key_base.endswith(unit_suffix):
            return key_base
        if key_base.endswith("_wh") and unit_suffix == "wh":
            return key_base
        return f"{key_base}_{unit_suffix}"

    @classmethod
    def _flatten_kamstrup(cls, kamstrup_dict: dict, convert_energy_to_kwh: bool = True) -> dict:
        out = {}
        records = kamstrup_dict.get("body", {}).get("records", [])
        for rec in records:
            rtype = rec.get("type", "")
            unit = rec.get("unit", "MeasureUnit.NONE")
            value = rec.get("value", None)
            if value is None:
                continue

            base = cls._norm(rtype)
            unit_suf = cls._unit_suffix(cls._last_part(unit))
            key = cls._merge_unit(base, unit_suf)

            # Change Wh -> kWh
            if convert_energy_to_kwh and base == "energy_wh":
                key = key.replace("energy_wh", "energy_kwh").replace("_wh", "")
                try:
                    value = float(value) / 1000.0
                except Exception:
                    pass

            # Handle duplicate keys, append _2, _3, ...
            if key in out:
                i = 2
                alt = f"{key}_{i}"
                while alt in out:
                    i += 1
                    alt = f"{key}_{i}"
                key = alt

            out[key] = value

        return out
