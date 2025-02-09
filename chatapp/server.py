import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import json

# Load messages from a file
def load_messages():
    try:
        with open("messages.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save messages to a file
def save_message(user, message):
    messages = load_messages()
    messages[user] = messages.get(user, []) + [message]
    with open("messages.json", "w") as file:
        json.dump(messages, file)

# Handle client messages
def handle_client(client_socket, clients, chat_box):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            
            if message.startswith("/history"):
                user = message.split(" ")[1] if len(message.split(" ")) > 1 else "Unknown"
                history = load_messages().get(user, ["No history found."])
                client_socket.send("\n".join(history).encode('utf-8'))
            elif message.startswith("/users"):
                client_socket.send(f"Connected users: {len(clients)}".encode('utf-8'))
            else:
                broadcast(message, client_socket, clients, chat_box)
                save_message("User", message)  # Save message to file
        except:
            break
    clients.remove(client_socket)
    client_socket.close()

# Broadcast messages to all clients
def broadcast(message, sender_socket, clients, chat_box):
    chat_box.insert(tk.END, f"{message}\n")
    for client in clients:
        if client != sender_socket:
            client.send(message.encode('utf-8'))

# Start server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))
    server.listen()
    print("Server started on port 5555")
    clients = []
    
    root = tk.Tk()
    root.title("Chat Server")
    chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
    chat_box.pack()
    chat_box.insert(tk.END, "Server started...\n")
    
    def accept_clients():
        while True:
            client_socket, _ = server.accept()
            clients.append(client_socket)
            threading.Thread(target=handle_client, args=(client_socket, clients, chat_box)).start()
    
    threading.Thread(target=accept_clients, daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    start_server()
