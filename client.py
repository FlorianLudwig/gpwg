#!/usr/bin/python
# copyright 2012 Florian Ludwig <f.ludwig@greyrook.com>

import os
import socket
from gi.repository import GnomeKeyring, GLib
import glib

import gpwg


SOCKET_PATH = '/tmp/gpwg'
KEYRING = GnomeKeyring.get_default_keyring_sync()[1]


def insert_master_key(master_key):
    GnomeKeyring.item_create_sync(KEYRING, GnomeKeyring.ItemType.GENERIC_SECRET, 'gpwg:masterkey', GLib.Array(), master_key, 1)


def get_master_key():
    ids = GnomeKeyring.list_item_ids_sync(KEYRING)[1]
    for id in ids:
        info = GnomeKeyring.item_get_info_sync('login', id)[1]
        if info.get_display_name() == 'gpwg:masterkey':
            return info.get_secret()
    return None


def main():
    GLib.set_application_name('GNOME password generator')
    master_key = get_master_key()
    if not master_key:
        master_pw = raw_input('need to generate master key:')
        master_key = gpwg.generate_master_key(master_pw)
        insert_master_key(master_pw)
        print 'saved master key to gnome keyring'
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(SOCKET_PATH)
    s.send(master_key)


if __name__ == '__main__':
    main()

