import logging

import pyodbc
from odd_contract.models import DataEntity
from oddrn_generator import MssqlGenerator
from pyodbc import Connection, Cursor

from .mappers import _column_metadata, _column_table, _column_order_by, _table_metadata, _table_table, _table_order_by
from .mappers.tables import map_table


class MssqlAdapter:
    __connection: Connection = None
    __cursor: Cursor = None

    def __init__(self, config) -> None:
        # https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15
        # https://github.com/mkleehammer/pyodbc/wiki/Install
        # https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Linux
        # cat /etc/odbcinst.ini
        self.__driver: str = config['ODD_DRIVER']
        self.__host: str = config['ODD_HOST']
        self.__port: str = config['ODD_PORT']
        self.__database: str = config['ODD_DATABASE']
        self.__user: str = config['ODD_USER']
        self.__password: str = config['ODD_PASSWORD']
        self.__data_source: str = f"DRIVER={self.__driver};SERVER={self.__host};DATABASE={self.__database};" \
                                  f"UID={self.__user};PWD={self.__password}"
        self.__oddrn_generator = MssqlGenerator(host_settings=f"{self.__host}", databases=self.__database)

    def get_data_source_oddrn(self) -> str:
        return self.__oddrn_generator.get_data_source_oddrn()

    def get_datasets(self) -> list[DataEntity]:
        try:
            self.__connect()

            tables = self.__query(_table_metadata, _table_table, _table_order_by)
            columns = self.__query(_column_metadata, _column_table, _column_order_by)

            return map_table(self.__oddrn_generator, tables, columns)
        except Exception as e:
            logging.error("Failed to load metadata for tables")
            logging.exception(e)
        finally:
            self.__disconnect()
        return []

    def __query(self, columns: str, table: str, order_by: str) -> list[tuple]:
        return self.__execute(f"select {columns} from {table} order by {order_by}")

    def __execute(self, query: str) -> list[tuple]:
        self.__cursor.execute(query)
        records = self.__cursor.fetchall()
        return records

    # replace
    def __connect(self):
        try:
            self.__connection = pyodbc.connect(self.__data_source)
            self.__cursor = self.__connection.cursor()
        except Exception as e:
            logging.error(e)
            raise DBException("Database error")
        return

    # replace
    def __disconnect(self):
        try:
            if self.__cursor:
                self.__cursor.close()
        except Exception:
            pass
        try:
            if self.__connection:
                self.__connection.close()
        except Exception:
            pass
        return


class DBException(Exception):
    pass
