# /usr/bin/python2
# -*- coding: utf-8 -*-

import socket


def defineTarget(target_host, target_port):
    target_host = input("Podaj cel:")
    target_port = int(raw_input("Podaj port: "))
    target = (target_host, target_port)
    return target


def createTCPSocket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return client_socket


target_host = "0.0.0.0"
target_port = 9999

test = raw_input(" Wybierz tryb:\r\n1. Uruchom klienta TCP" +
                 " \n\r2. Uruchom tryb testowy - domyślny" +
                 " \n\r ( IP:0.0.0.0, Port:9999 )")

target = defineTarget(target_host, target_port)


if __name__ == "main":
    main()
