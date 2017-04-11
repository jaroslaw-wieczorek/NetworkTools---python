#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket
"""
 Klient TCP pobierający stronę duckduckgo
"""
target_host = "0.0.0.0"
target_port = 9998

# utworzenie obiektu gniazda
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("client object was created")

# połączenie się klienta z serwerem
client.connect((target_host, target_port))

# wysyłanie danych
data = "GET / HTTP/1.1\r\nHost: duckduckgo.com\r\n\r\n"
client.send(data.encode('utf-8'))

# odbieranie danych
response = client.recv(4096).decode('utf-8')

print(response)
