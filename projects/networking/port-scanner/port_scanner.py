import socket
import sys
from datetime import datetime

#Definir o alvo (neste caso, o localhost)
target_host = "127.0.0.1"

print("-" * 50)
print(f"Scanning Target: {target_host}")
print(f"Time Started: {str(datetime.now())}")
print("-" * 50)

try:
    #Vamos testar 1 porta por enquanto
    port = 80
    print(f"Scanning port {port}")

    #Criar o socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0) #timetout de 1s para não ficar preso

    #Tentar ligar ao alvo e porta
    result = s.connect_ex((target_host, port))

    if result == 0:
        print(f"Port {port} is OPEN!")
    else:
        print(f"Port {port} is CLOSED")

    s.close()

except KeyboardInterrupt:
    print("\nExiting Script.")
    sys.exit()

except socket.gaierror:
    print("\nHostname could not be resolved.")
    sys.exit()

except socket.error:
    print("\nCould not connect to server.")
    sys.exit()