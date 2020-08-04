from datetime import datetime
from database.mssql import SqlServer
from abc import ABC, abstractmethod

class BowlingSystem(ABC):
    """
    Bowling system abstract base class
    """

    # Represent SQL Server Connection
    mssql = None

    # Represent mapped MongoDB collections
    collections = {}

    # Represent the bowling system tables list
    tables = []

    def __init__(self):
        self.mssql = SqlServer()

    def get_collection_name_by_table(self, table_name: str):
        """ Get the mapped collection name from table name """
        if table_name in self.collections:
            return self.collections.get(table_name)
        else:
            return None

    @abstractmethod
    def get_bowling_system_name(self):
        """ Get the current Bowling System name"""
        pass

    def get_from_sql_server(self, query: str):
        """ Get data from SQL Server """
        cursor = self.mssql.cursor()
        cursor.execute(query)
        return cursor.fetchall()