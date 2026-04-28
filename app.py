from flask import Flask, jsonify, request
import psutil
import platform
import socket
import time
import datetime
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY", "my-secret-key")


def require_api_key():
    user_key = request.headers.get("X-API-Key")
    return user_key == API_KEY


@app.route("/")
def home():
    return jsonify({
        "message": "Secure System Report API is running",
        "endpoints": {
            "health_check": "/health",
            "system_report": "/system"
        },
        "security": "API key required for /system endpoint"
    })


@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


@app.route("/system")
def system_report():
    if not require_api_key():
        return jsonify({
            "error": "Unauthorized access",
            "message": "Valid API key is required"
        }), 401

    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())

    data = {
        "hostname": socket.gethostname(),
        "operating_system": platform.system(),
        "os_version": platform.version(),
        "processor": platform.processor(),
        "cpu_usage_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2),
            "used_percent": psutil.virtual_memory().percent
        },
        "disk": {
            "total_gb": round(psutil.disk_usage('/').total / (1024 ** 3), 2),
            "used_percent": psutil.disk_usage('/').percent
        },
        "system_boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        "uptime_seconds": int(time.time() - psutil.boot_time())
    }

    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
