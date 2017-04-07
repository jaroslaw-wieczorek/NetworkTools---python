#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import socket
import getopt
import threading
import subprocess

'''
jackknife - program typu netcat
Opis działania:

Najpierw skrypt wczytuje wszystkie opcje wiersza poleceń i ustawiamy wartości
 zmiennych na podstawie wykrytych opcji. Jeśli któryś z parametrów wiersza
 poleceń nie spełnia naszych kryteriów, drukujemy instrukcję obsługi.

W następnym bloku kodu próbujemy naśladować funkcje netcata dotyczące
 odczytywania danych ze standardowego strumienia wejściowego i przesyłania ich
 przez sieć.

CTRL-D wyjście z trybu nasłuchu i włączenie interaktywnego terminala
 z nasłuchem. W ostatniej części kodu wykrywamy, że mamy utworzyć gniazdo
 nasłuchujące i przetwarzać dalsze polecenia (wysyłanie pliku, wykonanie
 polecenia, uruchomienie wiersza poleceń).

Napierw tworzymy obiekt gniazda TCP i sprawdzamy czy otrzymaliśmy jakieś dane
 w standardowym strumieniu wejściowym. Jeśli wszystko jest w porządku,
 przesyłamy dane do komputera docelowego i pobieramy dane w odpowiedz,
 aż się wyczerpią. Wszystko z odbieraniem i wysyłaniem jest powtarzane do
 meomentu aż użytkownikwyłączy skrypt.

'''
# defnicje kilku zminenych
listen = False
command = False
upload = False
execute = ''
target = ''
upload_destination = ''
port = 0


def showHelp():
    print("Narzędzia Jackknife - BHP Netcat")
    print("Sposób użycia:\n jackknife.py -t target_host -p port\n")
    print("-l --listen\t\t -nasłuchuje na [host]:[port] połączeń " +
          "przychodzących\n")
    print("-e --execute=file_to_run\t\t -wykonuje dany plik, gdy odbierze " +
          "połączenie\n")
    print("-c --command\t\t -inicjuje wiersz poleceń\n")
    print("-u --upload=destination\t\t -gdy odbierze połączenie, wysyła plik" +
          "i zapisuje go w [destination]\n")
    print("Przykłady:")
    print("jackknife.py -t 192.168.0.1 -p 5555 -l -c")
    print("jackknife.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("jackknife.py -t 192.168.0.1 -p 5555 -e=\'cat /etc/passwd\'")
    print("echo 'ABCDEFGHI' | ./jackknife.py -t 192.168.21.15 -p 135")
    sys.exit(0)


def client_sender(buffer):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # połączenie się z docelowym hostem
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)
        while True:

            # czekanie na zwrot danych
            recv_len = 1
            response = ''

            while recv_len:

                data = client.recv(4096)
                recv_len = len(data)
                response += data.decode('utf-8')

                if recv_len < 4096:
                    break

            print(response)

            # czekanie na więcej danych
            buffer = input()
            buffer += '\n'

            # wysłanie danych
            client.send(buffer.encode('utf-8'))
    except:
        print('[*] Wyjątek! Zamykanie')

        # zamknięcie połączenia
        client.close()


def server_loop():
    global target

    # Jeśli nie zdefiniowano celu nasłuchujemy na wszystkich interfejsach
    if not len(target):
        target = '0.0.0.0'

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        # wątek do obsługi naszego nowego klienta
        client_thread = threading.Thread(target=client_handler,
                                         args=(client_socket, ))
        client_thread.start()


def client_handler(client_socket):
    global upload
    global execute
    global command

    # Sprawdzanie czy coś jest wysyłane
    if len(upload_destination):

        # Wczytanie wszystkich bajtów i zapis ich w miejscu docelowym
        file_buffer = ''

        # wczytanie danych do końca
        while True:
            data = client_socket.recv(4096).decode('utf-8')

            if not data:
                break
            else:
                file_buffer += data

        # próba zapisania wczytanych bajtów
        try:
            file_descriptor = open(upload_destination, 'wb')
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            # potwierdzenie zapiasnia pliku
            info = ('Zapisano plik w %s\r\n' % upload_destination)
            client_socket.send(info).encode('utf-8')
        except:
            info = 'Nie udało się zapisać pliku w %s\r\n' % upload_destination
            client_socket.send(info).encode('utf-8')

    # sprawdzanie czy wykonano polecenia
    if len(execute):
        # wykonanie polecenia
        output = run_command(execute)

        client_socket.send(output).encode('utf-8')

    # Jeśli zażądano wiersza poleceń, przechodzimy do innej pętli
    if command:

        while True:
            # wyświetlanie prostego wiersza poleceń
            term = '<jackknife:#> '
            client_socket.send(term.encode('utf-8'))

            # Pobierany tekst do napotkania znaku nowego wiersza (enter)
            cmd_buffer = ''
            while ('\n' not in cmd_buffer):
                cmd_buffer += client_socket.recv(1024).decode('utf-8')

            # Odesłanie wyniku polecenia
            response = run_command(cmd_buffer)

            # Odesłanie odpowiedzi
            client_socket.send(response.encode('utf-8'))


def run_command(command):
    # odcięcie znaku nowego wiersza
    command = command.rstrip()

    # wykonanie polecenia i odebranie wyniku
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT,
                                         shell=True)
    except CalledProcessError as error:
        output = 'Nie udało się wykonać polecenia.\r\n'
    except any:
        output = 'Inny błąd podczas wykonywania polecenia.\r\n'
    # wysyłanie wyniku do klienta
    return(str(output))


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        showHelp()

    # odczytanie wiersza poleceń
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hle:t:p:cu:',
                                   ['help', 'listen', 'execute',
                                    'target', 'port', 'command',
                                    'upload'])
    except getopt.GetoptError as error:
        print('Błąd getopt: \n', error)
        showHelp()
    for o, a in opts:
        if o in ('-h', '--help'):
            showHelp()
        elif o in ('-l', '--listen'):
            listen = True
        elif o in ('-e', '--execute'):
            execute = a
        elif o in ('-c', '--commandshell', '--terminall'):
            command = True
        elif o in ('-t', '--target'):
            target = a
        elif o in ('-p', '--port'):
            port = int(a)
        else:
            assert('Nieobsługiwana opcja')

    # Będziemy nasłuchiwać czy tylko wysyłać dane ze sdtin?
    if not listen and len(target) and port > 0:
        # Wczytuje bufor z wiersza poleceń
        # spowoduje to blokadę terminala,
        # aby kontynuować należy wysłać CTRL-D,
        # gdy nie wysyłasz danych do stdin.

        buffer = sys.stdin.read().encode('utf-8')
        # Wysyła dane
        client_sender(buffer)

    # Będziemy nasłuchiwać i ewentalnie coś wysyłać, wykonywać polecenia oraz
    # włączać powłokę w zależności od opcji wiersza poleceń
    if listen:
        server_loop()


# if __name__ == "main()":
main()
