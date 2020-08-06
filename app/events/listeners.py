#!/usr/bin/python3

from app.app import App
from pubsub import pub

# ---------- LISTENERS ---------- #
class Listeners:

    def onChecksumMismatch(self, msg: set):
        App().log('DEBUG', msg=msg)


listeners = Listeners()

# ---------- TOPICS SUSCRIPTIONS ---------- #
pub.subscribe(listeners.onChecksumMismatch, 'checksum_mismatch')
