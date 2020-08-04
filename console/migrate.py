from database.mysql import *

mysql.connect()
mysql.create_tables([TableChecksum, FailedRequest])