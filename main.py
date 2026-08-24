import argparse
import threading
import scanner
import api

parser = argparse.ArgumentParser()
parser.add_argument("--network", help="IP/Network")
args = parser.parse_args()

if __name__ == "__main__":
    if args.network:
        scanner_thread = threading.Thread(target=scanner.scan_network, args=(args.network,))
        scanner_thread.daemon = True
        scanner_thread.start()

        api.app.run(debug=False)
    else:
        print("Unknown")