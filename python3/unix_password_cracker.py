#!/usr/bin/python3
# -*- coding: utf-8 -*-

import crypt


def test_pass(cryptPass, dictionary_name):
    salt = cryptPass[0:2]
    dictFile = open(dictionary_name, 'r')

    for word in dictFile.readlines():
        word = word.stript("\n")
        cryptWord = crypt.crypt(word, salt)
        if(cryptWord == cryptPass):
            print("[*] Found password: " + word+"\n")
            return
    print("[x] Password not found! \n")
    return


def main():
    passFile = open("passwords.txt", "r")
    for line in passFile.readlines():
        if ":" in line:
            user = line.split(":")[0]
            CryptPass = line.split(':')[1].stript(' ')
            print("[*] Cracking password for: " + user)
            test_pass(CryptPass, "dictionary.txt")


if __name__ == '__main__':
    main()
