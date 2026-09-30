import socket
import sys
from datetime import datetime

#Definir o alvo (neste caso, o localhost)
target_input = input("Enter the target host (IP or hostname): ") 
start_port = int(input("Enter the starting port number (1-65535): "))
end_port = int(input("Enter the ending port number (1-65535): "))

if (start_port < 1 or start_port > 65535) or (end_port < 1 or end_port > 65535) or (start_port > end_port):
    print("Invalid port range. Please enter valid port numbers between 1 and 65535.")
    sys.exit()

print("-" * 50)
print(f"Scanning Target: {target_input}")
print(f"Time Started: {str(datetime.now())}")
print("-" * 50)

try:
    #Reolver o hostname para IP
    target_ip = socket.gethostbyname(target_input)

    ports_open = 0
    #definir um range de portas para escanear (1-65354)
    for port in range(start_port, end_port + 1):
        #Criar o socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5) #timetout de 0.5s

        # Tentar conectar ao alvo na porta especificada
        result = s.connect_ex((target_ip, port))

        if result == 0:
            print(f"Port {port} is OPEN!")
            ports_open += 1
        s.close()

    print(f"\nScan completed! Found {ports_open} open ports.")

except KeyboardInterrupt:
    print("\n[!] Script stopped by user (Ctrl+C). Exiting.")
    sys.exit()

except socket.gaierror:
    print("\n[!] Hostname could not be resolved.")
    sys.exit()

except socket.error:
    print("\n[!] Could not connect to server.")
    sys.exit()