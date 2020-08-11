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
        ), as_dict=False)

    def get_all_current_checksums_from_sql_server(self):
        checksums = []
        bowling_sys_tables = self.app.get_current_bowling_system().tables
        for table in bowling_sys_tables:
            checksum_value = self.get_base_checksum_from_table(table)
            checksums.append({'table_name': table, 'checksum': checksum_value[0][0]})
        return checksums

    def get_all_current_checksums(self):
        return [check for check in TableChecksum.select(TableChecksum.table_name, TableChecksum.checksum).dicts()]

    def get_checksum_differences(self):
        current_checksum = self.get_all_current_checksums_from_sql_server()
        sqlserver_checksum = self.get_all_current_checksums()
        diff = [i for i in current_checksum if i not in sqlserver_checksum]
        result = len(diff) == 0
        if result:
            return None
        else:
            return diff

    def update_table_checksums(self, install: bool):
        bowling_sys = self.app.get_current_bowling_system().tables
        for table in bowling_sys:
            checksum = self.get_base_checksum_from_table(table)[0][0] if not install else 0
            query = TableChecksum().update(
                checksum=checksum,
                last_update=datetime.today()
            ).where(TableChecksum.table_name == table)
            query.execute()

