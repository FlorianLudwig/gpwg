#!/usr/bin/python
# copyright 2012 Florian Ludwig <f.ludwig@greyrook.com>

import os
import time
import signal
import socket
import select

from gi.repository import Gtk, Gdk, GLib, Notify

import gpwg


SOCKET_PATH = '/tmp/gpwg'
LAST_NOTIFICATION = None


def clear_notification():
    if LAST_NOTIFICATION:
        LAST_NOTIFICATION.close()


def show_notification(msg, details='', urgent=False):
    global LAST_NOTIFICATION
    clear_notification()
    n = Notify.Notification.new(msg, details, None)
    n.set_hint("transient", GLib.Variant.new_boolean(True))
    n.set_urgency(Notify.Urgency.CRITICAL if urgent else Notify.Urgency.NORMAL)
    n.show()
    LAST_NOTIFICATION = n




def main():
    # setup ctrl + c handler
    def handler(signum, frame):
        print 'ctrl + c received'
        Gtk.main_quit()

    # Set the signal handler and a 5-second alarm
    signal.signal(signal.SIGINT, handler)

    # setup socket
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)


    Notify.init("GNOME password generator")

    print SOCKET_PATH
    s.bind(SOCKET_PATH)
    s.listen(2)
    s.settimeout(0)
    def do():
        clip = Gtk.Clipboard.get (Gdk.SELECTION_PRIMARY)

        if select.select([s], [], [], 0)[0]:
            conn, _ = s.accept()
            print conn, _
            if conn:
                while 1:
                    master_pw = conn.recv(1024)
                    if not master_pw:
                        break
                    print 'update'
                    text = clip.wait_for_text()
                    if text:
                        show_notification('password for %s' % text.decode('utf-8'))
                        text = gpwg.generate_pw(text, master_pw)
                        clip.set_text(text, len(text))
                conn.close()
        return True


    #print 'kill -USR1 ' + str(os.getpid())
    GLib.timeout_add_seconds(1, do)
    Gtk.main()


if __name__ == '__main__':
    main()


