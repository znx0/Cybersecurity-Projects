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

if (start_port < 1 or start_port > 65535) or (end_port < 1 or end_port > 65535) or (start_port > end_port):
    print("Invalid port range. Please enter valid port numbers between 1 and 65535.")
    sys.exit()

print("-" * 50)
print(f"Scanning Target: {target_input}")
print(f"Port Range: {start_port} to {end_port}")
print("-" * 50)

try:
    # Reolver o hostname para IP
    target_ip = socket.gethostbyname(target_input)

    ports_open = 0
    # Definir um range de portas para escanear (1-65354)
    for port in range(start_port, end_port + 1):
        # Criar o socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5) # Timetout de 0.5s

        # Tentar conectar ao alvo na porta especificada
        result = s.connect_ex((target_ip, port))

        if result == 0:
            request = f"GET / HTTP/1.0\r\nHost: {target_ip}\r\n\r\n"
            service = socket.getservbyport(port)
            s.send(request.encode())  # Enviar uma mensagem para o servidor
            version = s.recv(1024)  # Receber a resposta do servidor
            banner = version.decode(errors='ignore').splitlines()[0] if version else "No banner received"
            print(f" {port} OPEN {service} {banner}")
            ports_open += 1

        s.close()

    print(f"\nScan completed! Found {ports_open} open ports.")

    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"Scan completed in {duration:.2f} seconds.")

except KeyboardInterrupt:
    print("\n[!] Script stopped by user (Ctrl+C). Exiting.")
    sys.exit()

except socket.gaierror:
    print("\n[!] Hostname could not be resolved.")
    sys.exit()

except socket.error:
    print("\n[!] Could not connect to server.")
    sys.exit()