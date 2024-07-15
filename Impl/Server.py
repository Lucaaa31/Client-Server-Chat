# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 13:33:36 2024

@author: Luca
"""

import socket
import threading

clients = []

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"Received message: {message.decode('utf-8')}")
                broadcast(message, client_socket)
            else:
                client_socket.close()
                clients.remove(client_socket)
                break
        except:
            client_socket.close()
            clients.remove(client_socket)
            break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    print("Server is listening on port 5555...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr} has been established.")
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()
