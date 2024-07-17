import socket
import paramiko
import threading

# SSH sunucu bilgileri
SSH_HOST = "192.168.64.5"
SSH_PORT = 22
SSH_USERNAME = "skonuvs"
SSH_PASS = "Ms180809"

# TCP sunucu bilgileri
TCP_HOST = "0.0.0.0"
TCP_PORT = 53947

def ssh_connect(command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USERNAME, password=SSH_PASS)
        print(f"Connected to {SSH_HOST}")

        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read() + stderr.read()
        return output

    except Exception as e:
        print(f"Failed to connect to {SSH_HOST}: {e}")
        return str(e).encode()

    finally:
        client.close()

def handle_client(client_socket):
    print("Client handler started")
    while True:
        try:
            command = client_socket.recv(1024).decode()
            if not command:
                break

            print(f"Executing command: {command}")
            output = ssh_connect(command)
            client_socket.send(output)

        except Exception as e:
            print(f"Error handling client: {e}")
            break

    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((TCP_HOST, TCP_PORT))
    server.listen(5)
    print(f"Listening on {TCP_HOST}:{TCP_PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
