# security-dashboard

A network security monitoring tool built with Python, Flask, and MySQL.
Continuosly scans a network for active hosts and open ports, stores result in a database, and exposes the data through a REST API.

> ⚠️ This tool is intended for use on your own network only.
> Scanning networks without permission is illegal.

## Requirements

- Python 3.x
- MySQL

## Environment Variables

Create a `.env` file in the project root:

```
DB_PASSWORD = your_mysql_password
```

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create database
mysql -u root -p

CREATE DATABASE netmonitor;
USE netmonitor;

CREATE TABLE hosts(
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip VARCHAR(15) NOT NULL,
    status ENUM('up', 'down') DEFAULT 'up',
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE scan_result(
    id INT AUTO_INCREMENT PRIMARY KEY,
    hosts_id INT,
    port INT,
    service VARCHAR(50),
    scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hosts_id) REFERENCES hosts(id)
);

# Run
python main.py --network <ip>/<netmask>
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /scans | Get all scan result |
| GET | /scans/latest | Get lastest scan result |
| GET | /hosts | Get all detected hosts |
| GET | /hosts/<ip>/ports | Get open port for a spesific host |

### Example

```bash
# Start the dashboard
python main.py --network 192.168.1.0/24

# Query the API
GET /scans
GET /scans/latest
GET /hosts
GET /hosts/192.168.1.1/ports
```