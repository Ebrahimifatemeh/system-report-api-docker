from flask import Flask, jsonify
import psutil
import platform
import socket
import time

app = Flask(__name__)

boot_time = time.time() - psutil.boot_time()

@app.route("/")
def home():
    return "System Report API is running"

@app.route("/system")
def system_info():
    data = {
        "hostname": socket.gethostname(),
        "operating_system": platform.system(),
        "cpu_usage_percent": psutil.cpu_percent(interval=1),
        "memory_usage_percent": psutil.virtual_memory().percent,
        "disk_usage_percent": psutil.disk_usage('/').percent,
        "uptime_seconds": int(time.time() - psutil.boot_time())
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
