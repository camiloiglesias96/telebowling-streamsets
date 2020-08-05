#!/usr/bin/python3

from pubsub import pub

# ---------- DISPATCHER ---------- #
class Dispatcher:

    def dispatch(self, topic: str, **kwargs):
        pub.sendMessage(topic, **kwargs)