import socket
import threading

HOST = '0.0.0.0'  # Server's public IP address
PORT = 5050            # Updated port number

# Dictionary to store client sockets and their nicknames
clients = {}
clients_lock = threading.Lock()

# Variable to track the current talker
talking_user = None
talking_lock = threading.Lock()

def broadcast(message, exclude_client=None):
    """
    Send a message to all connected clients except the excluded one.
    Each message is terminated with a newline character.
    """
    with clients_lock:
        for client in clients:
            if client != exclude_client:
                try:
                    client.sendall((message + '\n').encode('utf-8'))
                except:
                    # If sending fails, remove the client
                    remove_client(client)

def remove_client(client):
    """
    Remove a client from the clients dictionary and notify others.
    """
    global talking_user
    with clients_lock:
        if client in clients:
            nickname = clients[client]
            del clients[client]
            print(f"{nickname} has disconnected.")
            broadcast(f"SERVER: {nickname} has left the chatroom.")
            update_user_list()

    # If the disconnected client was talking, reset talking_user
    with talking_lock:
        if talking_user == nickname:
            talking_user = None
            broadcast(f"STATUS:STOP:{nickname}")

def update_user_list():
    """
    Send the updated list of online users to all clients.
    """
    with clients_lock:
        user_list = ','.join(clients.values())
    broadcast(f"USERLIST:{user_list}")

def handle_client(client_socket, address):
    """
    Handle communication with a connected client.
    """
    global talking_user
    buffer = ""
    try:
        # Receive the nickname
        while '\n' not in buffer:
            data = client_socket.recv(1024)
            if not data:
                client_socket.close()
                return
            buffer += data.decode('utf-8')
        nickname, buffer = buffer.split('\n', 1)
        nickname = nickname.strip()
        if not nickname:
            client_socket.close()
            return

        with clients_lock:
            clients[client_socket] = nickname
        print(f"{nickname} connected from {address}.")
        broadcast(f"SERVER: {nickname} has joined the chatroom.", exclude_client=client_socket)
        update_user_list()

        while True:
            data = client_socket.recv(4096)
            if not data:
                break  # Client disconnected
            buffer += data.decode('utf-8', errors='ignore')
            while '\n' in buffer:
                message, buffer = buffer.split('\n', 1)
                message = message.strip()
                if not message:
                    continue
                # Handle different message types
                if message.startswith("STATUS:"):
                    parts = message.split(':', 2)
                    if len(parts) >= 3:
                        _, action, user = parts
                        if action == "START":
                            with talking_lock:
                                if talking_user is None:
                                    talking_user = user
                                    broadcast(f"STATUS:START:{user}")
                                else:
                                    if user != talking_user:
                                        # Send BUSY status to the requester
                                        try:
                                            client_socket.sendall("STATUS:BUSY\n".encode('utf-8'))
                                        except:
                                            remove_client(client_socket)
                        elif action == "STOP":
                            with talking_lock:
                                if talking_user == user:
                                    talking_user = None
                                    broadcast(f"STATUS:STOP:{user}")
                elif message.startswith("MSG:"):
                    # Broadcast the message with the sender's nickname
                    msg_content = message[len("MSG:"):].strip()
                    broadcast(f"MSG:{nickname}: {msg_content}", exclude_client=None)  # Broadcast to all, including sender
                elif message.startswith("VOICE:"):
                    # Broadcast voice data as is
                    broadcast(message, exclude_client=None)
                else:
                    # For any other messages, broadcast as is
                    broadcast(message, exclude_client=None)

    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        remove_client(client_socket)
        client_socket.close()

def start_server():
    """
    Initialize and start the chat server.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
    except Exception as e:
        print(f"Failed to bind server on {HOST}:{PORT}: {e}")
        return

    server.listen()
    print(f"Chat server started on {HOST}:{PORT}")

    try:
        while True:
            client_socket, address = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.daemon = True  # Allows thread to be killed when main thread exits
            client_thread.start()
    except KeyboardInterrupt:
        print("\nShutting down the server.")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
