#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
[*] Opis działania wielowątkowego serwera TCP
Najpierw definiujemy adres IP i numer portu, na którym ma nasłuchiwać nasz serwer
Następnie nakazujemy serwerowi aby rozpoczął nasłuchiwanie i ustawiamy maksymalną liczbę 
połączeń w kolejce na 5. Później włączamy pętlę główną serwera, w której będzie on czekał na połączenia.
Gdy jakiś kilent nawiąże z nim połączenie, pobieramy jego gniazdo do zmiennej client, a dane połączenia
do zmiennej addr. Następnie tworzymy nowy obiekt wątku wskaujący naszą funkcję handle_client i jako argument
przekazujemy jej obiekt gniazda klienta. Później uruchamiany wątek obsługujący połączenie
z klientem po czym główna pętla serwera jest gotowa do obsługi następnego połączenia.
Funkcja handle_client wywołuje funkcję recv() i wysyła prostą wiadomość do klienta.
"""
import socket
import threading

def handle_client (client_socket):
    request = client_socket.recv(1024).decode("utf-8")
    print ("[*] Odebrano: ", request)

    #klient wysyła ACK
    msg="ACK!"
    client_socket.send(msg.encode("utf-8"))
    client_socket.close()

# Definicja adresu IP i numeru portu do nasłuchiwania
bind_ip = "0.0.0.0"
bind_port = 9998

bind_source = (bind_ip, bind_port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Włączenie nasłuchu
server.bind(bind_source)
server.listen(5)

#info
print ( "[*] Nasłuchiwanie na porcie %s:%d" % (bind_ip,bind_port))

while (True):

    client,addr = server.accept()
    print ("[*] Przyjęto połączenie od żródła: %s:%d" % (addr[0],addr[1]))

    #utworzenie wątku klienta do obsługi przychodzących danych
    client_keeper = threading.Thread(target=handle_client, args=(client,))
    client_keeper.start()
