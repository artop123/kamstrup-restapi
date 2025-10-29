import os
from flask import Flask, jsonify
from kamstrup_modbus import KamstrupMBusClient

PORT = os.getenv("MBUS_PORT", "/dev/ttyUSB0")
ADDRESS = int(os.getenv("MBUS_ADDRESS", 0))
BAUD = int(os.getenv("MBUS_BAUD", 9600))
PARITY = os.getenv("MBUS_PARITY", "E")
BYTES = int(os.getenv("MBUS_BYTES", 8))
STOP = int(os.getenv("MBUS_STOP", 1))
TIMEOUT = float(os.getenv("MBUS_TIMEOUT", 1.0))

app = Flask(__name__)
client = KamstrupMBusClient(
    port=PORT,
    address=ADDRESS,
    baudrate=BAUD,
    bytesize=BYTES,
    parity=PARITY,
    stopbits=STOP,
    timeout=TIMEOUT
)

app = Flask(__name__)

@app.route("/")
def get_values():
    try:
        data = client.read_simple()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
