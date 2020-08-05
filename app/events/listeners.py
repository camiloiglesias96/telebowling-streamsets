#!/usr/bin/python3

from pubsub import pub

# ---------- LISTENERS ---------- #
class ChecksumMismatch:

    def __call__(self, topic=pub.AUTO_TOPIC):
        print('All rigth')


# ---------- TOPICS SUSCRIPTIONS ---------- #
pub.subscribe(ChecksumMismatch(), 'daemon.checksum_mismatch')