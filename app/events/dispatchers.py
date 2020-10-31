#!/usr/bin/python3

from app.app import App
from pubsub import pub

# ---------- DISPATCHERS ---------- #

def doChecksumMismatch(msg):
    App().log('DEBUG', 'EVENT STARTED WITH MSG {msg}'.format(msg=msg))
    pub.sendMessage('checksum_mismatch', msg=msg)

def doBoardPushedData(msg):
    App().log('DEBUG', 'BOARD HAS BEEN PUSHED DATA FROM {msg}'.format(msg=msg))
    pub.sendMessage('board_pushed_data', msg=msg)