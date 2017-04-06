#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket
"""
Klient UDP do komunikacji bezpołączeniowej
"""
target_host = "127.0.0.1"
target_port = 80

serwer = (target_host,target_port)

# utworzenie obiektu gniazda UDP klienta
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# wiadomość do przesłania
msg = "ABBBBC"

#wysyłanie danych
client.sendto( msg.encode("utf-8"), serwer)

#odbieranie danych
data, addr = client.recvfrom(4096).decode("utf-8")
print (data)
