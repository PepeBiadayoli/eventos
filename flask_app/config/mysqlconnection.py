import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        self.connection = connection

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                if data:
                    print("Running Query:", query % data)  # Mensaje de depuración
                    cursor.execute(query, data)
                else:
                    print("Running Query:", query)  # Mensaje de depuración
                    cursor.execute(query)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong", e)  # Mensaje de error
                return False
            finally:
                cursor.close()

def connectToMySQL(db):
    return MySQLConnection(db)
