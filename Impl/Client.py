# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 13:35:50 2024

@author: Luca
"""

import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(message.decode('utf-8'))
            else:
                client_socket.close()
                break
        except:
            client_socket.close()
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        if message:
            client_socket.send(message.encode('utf-8'))
        else:
            client_socket.close()
            break

if __name__ == "__main__":
    main()
