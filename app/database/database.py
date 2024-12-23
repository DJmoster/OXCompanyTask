from psycopg2 import pool
from psycopg2.extras import RealDictCursor

from app.config import settings


class DataBaseHelper:
    def __init__(self, host, name, user, password):
        self._db_pool = pool.SimpleConnectionPool(
            minconn=1, maxconn=10, host=host, dbname=name, user=user, password=password
        )

    @property
    def pool(self):
        return self._db_pool

    @property
    def cursor(self) -> RealDictCursor:
        connection = self.pool.getconn()

        return connection.cursor(cursor_factory=RealDictCursor)

    def cursor_dependency(self) -> RealDictCursor:
        cursor = self.cursor

        try:
            yield cursor
        finally:
            cursor.close()
            self.pool.putconn(cursor.connection)


db_helper = DataBaseHelper(
    host=settings.db.host,
    name=settings.db.name,
    user=settings.db.user,
    password=settings.db.password,
)
