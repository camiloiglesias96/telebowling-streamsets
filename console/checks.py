#!/usr/bin/python3

import colorama
from os import getenv
from app.tools.tools import Tools
from termcolor import colored, cprint

colorama.init()

class Checks:

    check_msg = '########## {platform} [{status}] ##########'

    tools = Tools()

    def run(self):
        return {
            'API': self.check_api_server(),
            'BOWLING SQL SERVER': self.check_sql_server(),
            'SSH SUPPORT TUNNEL SERVER': self.check_tunnel_server()
        }

    def check_api_server(self):
        api_url = getenv('API_URL')
        return self.tools.ping_to_host(
            api_url.replace('http://', '')
        )

    def check_sql_server(self):
        return self.tools.ping_to_host(
            getenv('MSSQL_HOST')
        )

    def check_tunnel_server(self):
        tunnel_url = getenv('TUNNEL_HOST_DOMAIN')
        return self.tools.ping_to_host(
            tunnel_url.replace('http://', '')
        )

if __name__ == '__main__':
    ping = None
    checks = Checks().run()
    print('\n')
    for check, result in checks.items():
        if result:
            ping = colored(
                Checks().check_msg.format(
                    platform=check,
                    status='AVAILABLE'
                ),
                'white',
                'on_green',
                ['bold']
            )
        else:
            ping = colored(
                Checks().check_msg.format(
                    platform=check,
                    status='NOT AVAILABLE'
                ),
                'white',
                'on_red',
                ['bold']
            )
        print(ping)