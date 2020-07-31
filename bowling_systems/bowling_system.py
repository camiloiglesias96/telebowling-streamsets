from datetime import datetime
from database.mssql import SqlServer
from abc import ABC, abstractmethod

class BowlingSystem(ABC):
    """
    Bowling system abstract base class
    """
    # Date fields function paths
    date_paths = {}
    
    # Bowling date format
    date_format = '%Y-%m-%d %H:%M:%S'

    # Represent the start time to query
    start_time = None

    # Represent the end time to query
    end_time = None

    # Represent SQL Server Connection
    mssql = None

    # Represent the bowling system tables list
    tables = []

    def __init__(self):
        self.mssql = SqlServer()
        self.set_datetime()

    @abstractmethod
    def get_log_lanes(self):
        """ Get current status of lanes """
        pass
    
    @abstractmethod
    def get_lane_errors_and_events(self):
        """ Get current lanes errors and events """
        pass

    @abstractmethod
    def get_lanes_reservations(self):
        """ Get current lanes reservations """
        pass

    @abstractmethod
    def get_sales_details(self):
        """ Get sales details """
        pass

    @abstractmethod
    def get_customers_waiting_list(self):
        """ Get the customers waiting list """
        pass

    @abstractmethod
    def get_bowling_system_name(self):
        """ Get the current Bowling System name"""
        pass

    @abstractmethod
    def get_pos_tickets(self):
        pass
    
    def set_datetime(self):
        today = datetime.today()
        day_start = datetime(year=today.year, month=today.month, day=today.day, hour=0, second=0)
        day_end = datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=59, second=59)
        self.start_time = day_start.strftime(self.date_format)
        self.end_time = day_end.strftime(self.date_format)

    def get_from_sql_server(self, query: str):
        cursor = self.mssql.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def get_date_path(self, table: str):
        path = self.date_paths.get(table)
        if path is not None:
            return path
        else:
            return None
