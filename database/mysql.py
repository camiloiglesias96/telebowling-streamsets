import json
from os import getenv
from datetime import datetime
from peewee import *

mysql = MySQLDatabase(getenv('MYSQL_DATABASE'), user=getenv('MYSQL_USER'), 
                        password=getenv('MYSQL_PASSWORD'), host=getenv('MYSQL_HOST'), 
                        port=int(getenv('MYSQL_PORT')))

""" BaseModel Class """
class BaseModel(Model):
    class Meta:
        database = mysql


""" The JSON Custom Field for peewee """
class JSONField(TextField):
        
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


""" Table: Tablechecksum """
class TableChecksum(BaseModel):
    table_name = CharField(primary_key=True, unique=True, index=True)
    checksum = BigIntegerField(null=True, default=None)
    last_inserted_id = BigIntegerField(null=True)
    last_update = DateTimeField()

    @property
    def last_inserted(self):
        if self.last_inserted_id is not None:
            return self.last_inserted_id
        else:
            return 0

    class Meta:
        table_name = 'table_checksums'
        primary_key= False


""" Table: FailedRequest """
class FailedRequest(BaseModel):
    id = UUIDField(primary_key=True)
    url = CharField(null=False)
    data = JSONField(null=True)
    persisted = BooleanField(default=False)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'failed_requests'
        primary_key = False