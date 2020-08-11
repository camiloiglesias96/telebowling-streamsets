from datetime import datetime
from database.mssql import SqlServer
from abc import ABC, abstractmethod
import pymssql

class BowlingSystem(ABC):
    """
    Bowling system abstract base class
    """

    # Represent SQL Server Connection
    mssql = None

    # Get mongo action collection
    mongo_actions = {}

    # Represent the most biggest datums for every BW system table
    big_datums = []

    # Represent every id field_name for every BW system table
    id_names = {}

    # Represent every table when the system needs casts the dates and decimals
    # FreeTDS bug on datetime format and decimal builtin python class
    table_has_casts = {}

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
        """ Get data from SQL Server based on last_id or None """
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
            return self.mssql.raw_query(query, as_dict=True)
        return self.mssql.raw_query(query.format(table_name=table_name), as_dict=True)

    def get_data_from_mssql_by_range_id(self, table_name:str, field: str, init: int, end: int):
        """ Get rows of data on specific ID range from SQL Server """
        query = """
            SELECT * FROM {table} WHERE {field} >= {init} AND {field} <= {end}
        """.format(
            table=table_name,
            field=field,
            init=init,
            end=end
        )
        return self.mssql.raw_query(query, as_dict=True)

    def get_last_id_from_mssql(self, table_name:str, field: str):
        """ Get the last ID from SQL Server Table """
        query = """
            SELECT MAX({field}) as last_id FROM {table}
        """
        return self.mssql.raw_query(query.format(
            field=field,
            table=table_name
        ), as_dict=False)[0][0]

    def get_table_field_name(self, table_name:str):
        """ Get the ID mapped from table name """
        field_name = self.id_names.get(table_name)
        if field_name is not None:
            return field_name
        else:
            return None

    def table_needs_cast(self, table_name: str):
        """ Retrieve if table data need casts """
        need_casts = self.table_has_casts.get(table_name)
        if need_casts is not None:
            return need_casts
        else:
            return False

    def get_mongo_action(self, collection: str):
        """ Get the specific mongo action to perform """
        action = self.mongo_actions.get(collection)
        if action is not None:
            return action
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