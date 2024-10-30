import socket

# Server setup
host = '0.0.0.0'  # listens on all interfaces
port = 4444       # port you want to use for your server

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print(f"Listening on {host}:{port}...")

while True:
    # Accept a client connection
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} has been established.")
    try:
        while True:
            command = input("Enter command: ")
            if command.lower() == "exit":
                client_socket.send(command.encode("utf-8"))
                print("Exiting connection.")
                break
            elif command.lower() == "clear":
                print("\033[H\033[J", end="")  # Clear the terminal on server side
                continue
            
            client_socket.send(command.encode("utf-8"))
            response = client_socket.recv(4096).decode("utf-8")
            print(response)
    except (ConnectionResetError, BrokenPipeError):
        print("Connection lost. Waiting for a new connection...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
