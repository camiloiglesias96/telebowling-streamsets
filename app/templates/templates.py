from pathlib import Path
from string import Template
from termcolor import cprint, colored
import os, shutil, colorama, subprocess, getpass

colorama.init()

class DaemonGenerator:
    """ Generate and install ssh daemon """

    __ALLOWED_PLATFORMS = ['linux', 'linux2', 'darwin']
    __STUB_FILE_NAME = 'autossh-systemd.stub'
    __TUNNEL_FILE_DST = '/etc/systemd/system/{file}'
    __TUNNEL_FILE_NAME = 'telebowling-ssh-{bid}.service'
    __TUNNEL_FILE_STUB = os.getenv('TUNNEL_STUB_FILE')
    __TUNNEL_DOMAIN = os.getenv('TUNNEL_HOST_DOMAIN')
    __TUNNEL_USER = os.getenv('TUNNEL_USER')
    __TUNNEL_CERT = os.getenv('TUNNEL_SSH_KEY_PATH')
    __TUNNEL_REMOTE_PORT = os.getenv('TUNNEL_REMOTE_PORT')

    def make_daemon_file(self):
        if not os.path.isfile(self.__TUNNEL_CERT):
            raise Exception('SSH key file doesn`t exist')
        stub = open(self.__TUNNEL_FILE_STUB)
        template = Template(stub.read())
        replaces = {
            'domain': self.__TUNNEL_DOMAIN,
            'board_id': os.getenv('BOARD_ID'),
            'ssh_port': self.__TUNNEL_REMOTE_PORT,
            'user': self.__TUNNEL_USER,
            'cert': self.__TUNNEL_CERT
        }
        result = template.substitute(replaces)
        daemon_file_path = self.__TUNNEL_FILE_STUB.replace(
            self.__STUB_FILE_NAME,
            self.__TUNNEL_FILE_NAME.format(bid=os.getenv('BOARD_ID')) 
        )
        daemon_file = open(daemon_file_path, 'w')
        daemon_file.write(result)
        daemon_file.close()
        if os.sys.platform in self.__ALLOWED_PLATFORMS:
            cprint('######### DAEMON FILE GENERATED DAEMON #########', 'white', 'on_yellow')
            shutil.move(daemon_file_path, self.__TUNNEL_FILE_DST.format(
                file=self.__TUNNEL_FILE_NAME.format(bid=os.getenv('BOARD_ID'))
            ))
            print("""
                {remember}
                sudo cp {file_path} {dst}
                sudo systemctl daemon-reload
                systemctl start {tunnel_file}
                systemctl enable {tunnel_file}
            """.format(
            file_path=daemon_file_path,
            dst=self.__TUNNEL_FILE_DST.format(
                file=self.__TUNNEL_FILE_NAME.format(bid=os.getenv('BOARD_ID'))
            ),
            tunnel_file=daemon_file_path,
            remember=colored('########## REMEMBER EXECUTE ##########', 'white', 'on_green')
        ))