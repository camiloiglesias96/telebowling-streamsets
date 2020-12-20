#!/usr/bin/python3

import os
import platform
import subprocess

class Tools:

    __WINDOWS = 'windows'

    def ping_to_host(self, host: str) -> bool:
        param = '-n' if platform.system().lower() == self.__WINDOWS else '-c'

        command = ['ping', param, '1', host]

        return subprocess.call(command,stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT) == 0
