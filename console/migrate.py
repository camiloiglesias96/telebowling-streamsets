from database.mysql import *

"""
Migrate script

Create on MySQL Database the basic checksum system tables to sync and migrate all bowling
data system on change to TLB Cloud Data Lake BI System.

"""
mysql.connect()
mysql.create_tables([TableChecksum, FailedRequest, ServiceSettings])