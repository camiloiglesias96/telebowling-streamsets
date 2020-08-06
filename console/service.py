import threading
from time import sleep
from os import getenv
from app.app import App
from app.events import *
from checksum_system.checksums import Checksum

class Main:

    app = App()

    def run(self):
        try:
            daemon_interval = int(getenv('DAEMON_INTERVAL'))
            checksum_check = Checksum().get_checksum_differences()
            if checksum_check is not None:
                table_diff = [table['table_name'] for table in checksum_check]
                self.app.log('DEBUG', 'TABLE WITH DIFFERENCES {tables}'.format(tables=table_diff))
                dispatchers.doChecksumMismatch(table_diff)
                sleep(daemon_interval)
            sleep(daemon_interval)
        except KeyboardInterrupt:
            self.app.log('WARNING', KeyboardInterrupt('Daemon keyboard killed'))
            exit()


if __name__ == '__main__':
    main_service = Main()
    while True:
        threading.Thread(target=main_service.run(), daemon=True).start