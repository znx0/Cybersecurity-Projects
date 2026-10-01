# Implementation Guide: Python TCP Port Scanner

This document provides a technical deep-dive into `port_scanner.py`, breaking down how command-line argument parsing, network sockets, active connection testing, service identification, and error handling are implemented.

## 📁 Architecture Overview

The project relies entirely on Python's standard library, keeping dependencies at zero and maximizing portability:
* **`socket`**: Manages low-level network connections and service lookups.
* **`argparse`**: Handles robust command-line argument parsing.
* **`sys`**: Manages clean script termination and exit codes.
* **`time`**: Measures total execution performance with high precision (`perf_counter`).

---

## ⚙️ Complete Code Breakdown

### 1. Initialization & CLI Argument Parsing
The script starts by initializing the performance timer and setting up `argparse` to capture required positional parameters from the terminal.

```python
import socket
import sys
import argparse
import time

start_time = time.perf_counter()
parser = argparse.ArgumentParser(description="Start port scanning")

parser.add_argument("target", help="Target IP address or hostname")
parser.add_argument("start_port", type=int, help="Starting port number")
parser.add_argument("end_port", type=int, help="Ending port number")

args = parser.parse_args()

target_input = args.target
start_port = args.start_port
end_port = args.end_port
```

###2. Port Range Validation

Before initiating network traffic, validation rules ensure that ports fall within the valid TCP range and that the range is logically consistent.

```python
if (start_port < 1 or start_port > 65535) or (end_port < 1 or end_port > 65535) or (start_port > end_port):
    print("Invalid port range. Please enter valid port numbers between 1 and 65535.")
    sys.exit()

print("-" * 50)
print(f"Scanning Target: {target_input}")
print(f"Port Range: {start_port} to {end_port}")
print("-" * 50)
```

###3. DNS Resolution & Core Scanning Loop

The application resolves hostnames into IPV4 addresses and loops sequentially through the specified port range.

```python
try:
    # Resolve hostname to IP
    target_ip = socket.gethostbyname(target_input)

    ports_open = 0
    for port in range(start_port, end_port + 1):
        # Create a new socket for each port iteration
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5) # 0.5s timeout to prevent hanging

        # Attempt TCP connection
        result = s.connect_ex((target_ip, port))
```

* **Socket.gethostbyname():** Converts doamains like scanme.nmao.org into raw IPs.
* **s.settimeout(0.5):** Restricts connection attempts so unresponsive ports don't block execution indefinitely
* **connect_ex():** Returns 0 on a successful connection without triggering exceptions for closed ports.

###4. Service Identification & Banner Grabbing

When an open port is found (result == 0), the script queries the service name and sends an HTTP/1.0 probe to capture the server banner.

```python
	if result == 0:
            request = f"GET / HTTP/1.0\r\nHost: {target_ip}\r\n\r\n"
            service = socket.getservbyport(port)
            s.send(request.encode())  # Send basic HTTP payload
            version = s.recv(1024)    # Read server response
            
            # Safely decode banner and extract the first line
            banner = version.decode(errors='ignore').splitlines()[0] if version else "No banner received"
            print(f" {port} OPEN {service} {banner}")
            ports_open += 1

        s.close()

    print(f"\nScan completed! Found {ports_open} open ports.")

    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"Scan completed in {duration:.2f} seconds.")
```

* **Service Mapping (socket.getservbyport):** Automatically maps standad port number to their commom protocol names
* **The Limitation of Universal Probing:** The script sends an HTTP/1.0 GET request blindly to every open port. While effective for web servers, non-HTTP services (like SSH, FTP, or SMTP) use completely different application-layer rules. For instance, SSH sends its version string immediately upon connection without waiting for a client request, whereas FTP expects specific commands. To grab banners accurately across diverse services, each protocol would need to be manually identified and matched with its specific request payload.

###5. Exception Handling

Targeted exception handlers prevent stack traces and ensure a graceful user experience during interruptions or network failures.

```Python
except KeyboardInterrupt:
    print("\n[!] Script stopped by user (Ctrl+C). Exiting.")
    sys.exit()

except socket.gaierror:
    print("\n[!] Hostname could not be resolved.")
    sys.exit()

except socket.error:
    print("\n[!] Could not connect to server.")
    sys.exit()
```

* **KeyboardInterrupt:** Catches Ctrl+C cleanly.
* **socket.gaierror:** Handles invalid or unresolvable domain names.
* **socket.error:** Manages general lower-level socket connection failures.
