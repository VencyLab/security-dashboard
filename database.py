import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = os.getenv("DB_PASSWORD"),
        database = "netmonitor",
        autocommit=True
    )

def store_scanned_network(ip, status):
    db = get_connection()
    cursor = db.cursor(dictionary = True)
    cursor.execute("INSERT INTO hosts (ip, status) VALUES (%s, %s)", (ip, status))
    hosts_id = cursor.lastrowid
    cursor.close()
    db.close()
    return hosts_id

def store_network_detail(hosts_id, port, service):
    db = get_connection()
    cursor = db.cursor(dictionary = True)
    cursor.execute("INSERT INTO scan_result (hosts_id, port, service) VALUES (%s, %s, %s)", (hosts_id, port, service))
    cursor.close()
    db.close()

def get_scanned_hosts():
    db = get_connection()
    cursor = db.cursor(dictionary = True)
    cursor.execute("SELECT * FROM hosts")
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

def get_latest_hosts():
    db  = get_connection()
    cursor = db.cursor(dictionary = True)
    cursor.execute("SELECT * FROM hosts WHERE id IN(SELECT MAX(ID) FROM hosts)")
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result

def get_hosts():
    db = get_connection()
    cursor = db.cursor(dictionary = True)
    cursor.execute("SELECT ip, COUNT(ip) AS total_seen, MAX(last_seen) AS last_seen FROM hosts GROUP BY ip")
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

def get_hosts_ports(ip):
    db1 = get_connection()
    cursor1 = db1.cursor(dictionary=True, buffered=True)
    cursor1.execute("SELECT id FROM hosts WHERE ip = %s", (ip,))
    hosts = cursor1.fetchall()
    cursor1.close()
    db1.close()

    if not hosts:
        return None

    host_ids = [h["id"] for h in hosts]
    placeholders = ",".join(["%s"]*len(host_ids))

    db2 = get_connection()
    cursor2 = db2.cursor(dictionary=True, buffered=True)
    cursor2.execute(f"SELECT DISTINCT port, service FROM scan_result WHERE hosts_id IN ({placeholders})", host_ids)
    ports = cursor2.fetchall()
    cursor2.close()
    db2.close()
    return ports