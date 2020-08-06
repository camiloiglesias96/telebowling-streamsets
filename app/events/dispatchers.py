#!/usr/bin/python3

from pubsub import pub

# ---------- DISPATCHERS ---------- #

def doChecksumMismatch(msg):
    pub.sendMessage('checksum_mismatch', msg=msg)