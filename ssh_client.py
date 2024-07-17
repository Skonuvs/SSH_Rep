import socket

# TCP sunucu bilgileri
TCP_HOST = "server"
TCP_PORT = 53947

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((TCP_HOST, TCP_PORT))
    print(f"Connected to TCP server at {TCP_HOST}:{TCP_PORT}")

    while True:
        command = input("Enter command to execute: ")
        if command.lower() == 'exit':
            break

        client.send(command.encode())

        response = client.recv(4096).decode()
        print(f"Response:\n{response}")

    client.close()

if __name__ == "__main__":
    start_client()
