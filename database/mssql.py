import pymssql
from os import getenv

class SqlServer:

    connection = None

    def __init__(self):
        self.connection: pymssql.Cursor = None
        self.connect_to_server()

    def connect_to_server(self):
        """ Open connection with SQL Server """
        self.connection = pymssql.connect(server=getenv('MSSQL_HOST'), user=getenv('MSSQL_USER'),
                    password=getenv('MSSQL_PASSWORD'), port=getenv('MSSQL_PORT'))

    def cursor(self, as_dict: bool = True):
        """ Get the current cursor on SQL Server connection """
        return self.connection.cursor(as_dict=as_dict)

    def raw_query(self, query: str):
        """ Run a raw query with the current open connection """
        cursor = self.cursor(as_dict=False)
        cursor.execute(query)
        return cursor.fetchall()