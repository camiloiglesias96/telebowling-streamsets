from app.app import App
from datetime import datetime
from database.mysql import TableChecksum
from database.mssql import SqlServer

class Checksum(SqlServer):

    app = None

    def __init__(self):
        self.app = App()
        super().__init__()

    def get_base_checksum_from_table(self, table_name: str):
        query = """
            SELECT CHECKSUM_AGG(CHECKSUM(*)) FROM {table_name}
        """
        return self.raw_query(query.format(
            table_name=table_name
        ))

    def update_table_checksums(self):
        bowling_sys = self.app.get_current_bowling_system().tables
        for table in bowling_sys:
            checksum = self.get_base_checksum_from_table(table)
            query = TableChecksum().update(
                checksum=checksum[0][0],
                last_update=datetime.today()
            ).where(TableChecksum.table_name == table)
            query.execute()

