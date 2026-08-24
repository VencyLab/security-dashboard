from flask import Flask, jsonify
import database

app = Flask(__name__)

@app.route("/scans", methods=["GET"])
def get_scans():
    return jsonify(database.get_scanned_hosts())

@app.route("/scans/latest", methods=["GET"])
def get_latest():
    return jsonify(database.get_latest_hosts())

@app.route("/hosts", methods=["GET"])
def get_hosts():
    return jsonify(database.get_hosts())

@app.route("/hosts/<ip>/ports")
def get_port(ip):
    return jsonify({"ip": (ip), "open_ports": database.get_hosts_ports(ip)})