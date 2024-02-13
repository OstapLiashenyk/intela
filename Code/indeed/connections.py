from decouple import config
from playhouse.mysql_ext import MySQLConnectorDatabase
from peewee import *

draft_database = MySQLConnectorDatabase(config('DB_NAME'),
                                    user=config('DB_USER'),
                                    host=config('DB_HOST'),
                                    password=config('DB_PASSWORD'),
                                    port=config('DB_PORT', default=5432),
                                    collation = 'utf8mb4_unicode_ci',
                                    charset = 'utf8mb4' )





