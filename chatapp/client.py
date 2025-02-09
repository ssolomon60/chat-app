import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Function to receive messages from the server
def receive_messages(client_socket, chat_box):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            chat_box.insert(tk.END, f"{message}\n")
        except:
            break

# Function to send messages to the server
def send_message(client_socket, entry_field):
    message = entry_field.get()
    entry_field.delete(0, tk.END)
    client_socket.send(message.encode('utf-8'))

# Function to start the client GUI
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5555))  # Connect to the server

    # Create GUI
    root = tk.Tk()
    root.title("Chat Client")

    chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
    chat_box.pack()

    entry_field = tk.Entry(root, width=50)
    entry_field.pack()
    entry_field.bind("<Return>", lambda event: send_message(client_socket, entry_field))

    send_button = tk.Button(root, text="Send", command=lambda: send_message(client_socket, entry_field))
    send_button.pack()

    # Start receiving messages
    threading.Thread(target=receive_messages, args=(client_socket, chat_box), daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    start_client()
