import socket
import concurrent.futures
import time

# Ask for target and port range
target = input("Enter target IP or domain: ")
start_port = int(input("Enter starting port: "))
end_port = int(input("Enter ending port: "))

# Ask if user wants to save to file
save_to_file = input("Save results to file? (y/n): ").strip().lower() == 'y'
if save_to_file:
    filename = f"port_scan_{target.replace('.', '_')}_{int(time.time())}.txt"
    file = open(filename, "w")

print(f"\nScanning ports {start_port} to {end_port} on {target}...\n")

# Port scanning function
def scan_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            msg = f"Port {port} is OPEN"
            print(msg)
            if save_to_file:
                file.write(msg + "\n")
        else:
            msg = f"Port {port} is CLOSED"
            if save_to_file:
                file.write(msg + "\n")

# Use ThreadPoolExecutor for faster scanning
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(scan_port, range(start_port, end_port + 1))

if save_to_file:
    file.close()
    print(f"\nResults saved to {filename}")

print("\nScan complete!")
