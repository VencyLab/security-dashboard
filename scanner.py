import socket
import ipaddress
import threading
import time
import database

services = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    21: "FTP",
    3306: "MySQL",
}

def is_host_up(ip):
    open_ports = []
    for port in services:
        sock = socket.socket()
        sock.settimeout(1)
        result = sock.connect_ex((str(ip), port))
        sock.close()
        if result == 0:
            open_ports.append(port)

    if open_ports:
        hosts_id = database.store_scanned_network(str(ip), "UP")
        for port in open_ports:
            database.store_network_detail(hosts_id, port, services[port])
        return True
    return False

def scan_network(network):
    network = ipaddress.ip_network(network)
    while True:
        count = []
        lock = threading.Lock()

        def thread_task(ip):
            if is_host_up(ip):
                with lock:
                    count.append(1)

        threads = []

        for ip in network.hosts():
            t = threading.Thread(target=thread_task, args=(ip,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        print(f"\nScan and store complete. {len(count)} hosts found.")
        time.sleep(60)