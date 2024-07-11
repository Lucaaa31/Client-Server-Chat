# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 13:35:50 2024

@author: Luca
"""

import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")

        # Configurazione tema scuro
        self.master.configure(bg='black')

        self.chat_display = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, state='disabled', bg='black', fg='white', insertbackground='white', selectbackground='gray')
        self.chat_display.pack(padx=20, pady=5)

        self.message_entry = tk.Entry(self.master, width=50, bg='black', fg='white', insertbackground='white')
        self.message_entry.pack(padx=20, pady=5, side=tk.LEFT)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.master, text="Send", command=self.send_message, bg='gray', fg='black')
        self.send_button.pack(padx=5, pady=5, side=tk.LEFT)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('127.0.0.1', 5555)
        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.client_socket.connect(self.server_address)
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            self.display_message(f"Unable to connect to server: {e}")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.display_message(message)
                else:
                    self.client_socket.close()
                    break
            except Exception as e:
                self.display_message(f"Error receiving message: {e}")
                self.client_socket.close()
                break

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.display_message(f"You: {message}")
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                self.display_message(f"Error sending message: {e}")
                self.client_socket.close()

    def display_message(self, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, message + '\n')
        self.chat_display.configure(state='disabled')
        self.chat_display.yview(tk.END)

def main():
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()
