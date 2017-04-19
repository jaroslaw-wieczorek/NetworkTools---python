# /bin/usr/python
# -*- coding: utf-8 -*-

"""
Proxy TCP serwer służący do przekazywania połączenie z hosta do hosta.

"""

import sys
import socket
import threading
from threading import Thread


def server_loop(local_host, local_port, remote_host, remote_port,
                recive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target = (local_host, local_port)
    try:
        server.bind(target)
    exec Exception as err:
        print("[!] Nieudana próba nasłuchu na porcie %s:%d"
              % target[0], target[1])
        print("[!] Poszukaj innego gniazda lub zdobądź odpowiednie uprawienia")
        sys.exit(0)
        print("[*] Nasłuchiwanie na porcie %s:%d" % (target[0], target[1]))
        server.listen(5)

        while True:
            client_socket, addr = server.accept()

            # wydruk informacji o połączeniu lokalnym
            print("[==>] Otrzymano połączenie przychodzące od %s:%d"
                  % addr[0], addr[1])

            # uruchomienie wątku do współpracy ze zdalnym hostem
            proxy_thread = Thread(target=proxy_handler, args=(client_socket,
                                  remote_host, remote_port, recive_first))
            proxy_thread.start()


def main():

    # żadnego dzwinego przetwarzania wiersza poleceń
    if len(sys.argv[1:]) != 5:
        print("Sposób użycia: ./proxy_tcp.py [local_host] [local_port] "
              + "[remotehost] [remoteport] [recive_first]\n")
        print("Przykład: ./proxy_tcp.py 127.0.0.1 9000 10.12.132.1 90000 True")
        sys.exit(0)

    # konfiguracja lokalnych parametrów nasłuchu
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    # ustawienie zdalnego celu
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # nakazujemy proxy nawiązanie połączenia i odberania danych
    # przed wysyłaniem danych do zdalnego hosta
    recive_first = sys.argv[5]
    if "True" in recive_first:
        recive_first = True
    else:
        recive_first = False
    # włączamy gniazdo do nasłuchu
    server_loop(local_host, local_port, remote_host, remote_port, recive_first)


main()
