from datetime import datetime
from database.mssql import SqlServer
from abc import ABC, abstractmethod

class BowlingSystem(ABC):
    """
    Bowling system abstract base class
    """

    # Represent SQL Server Connection
    mssql = None

    # Represent every id field_name for every BW system table
    id_names = {}

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

    def get_data_from_system_table(self, table_name:str, last_id: int = None):
        query = """
            SELECT * FROM {table_name}
        """
        if last_id is not None:
            field_id = self.get_table_field_name(table_name)
            query += """ WHERE {field_id} >= {last_inserted} """
            query = query.format(
                table_name= table_name, 
                field_id=field_id, 
                last_inserted=last_id
            )
            print(query)
            return self.mssql.raw_query(query, as_dict=True)
        return self.mssql.raw_query(query.format(table_name=table_name), as_dict=True)

    def get_table_field_name(self, table_name:str):
        field_name = self.id_names.get(table_name)
        if field_name is not None:
            return field_name

    @abstractmethod
    def get_bowling_system_name(self):
        """ Get the current Bowling System name"""
        pass

    def get_from_sql_server(self, query: str):
        """ Get data from SQL Server """
        cursor = self.mssql.cursor()
        cursor.execute(query)
        return cursor.fetchall()