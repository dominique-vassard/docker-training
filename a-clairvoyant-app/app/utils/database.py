import mysql.connector
# from app.irma_api import app


class IrmaDb(object):
    """MYSQL Kwanko Database Connection Object"""
    def __init__(self, host, port, user, password, db_name):
        """IncirrinaDb Constructor

        Instantiate a Cursor
        """
        self._connect_infos = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": db_name
        }

    def execute(self, sql, params=[]):
        self._db = mysql.connector.connect(**self._connect_infos)
        cursor = self._db.cursor(dictionary=True)

        try:
            cursor.execute(sql, params)
            r = [row for row in cursor]
            self._db.commit()
            return r
        except Exception as e:
            self._db.rollback()
            raise e
        finally:
            cursor.close()
            self._db.close()
