import psycopg2
from psycopg2 import sql

# Параметры подключения к PostgreSQL
dbname = 'bot'
user = 'aslanpapa'
password = 'aslhack'
host = 'localhost'  # Укажите ваш хост, на котором работает PostgreSQL



async def insert_token_into_database(user_id, token):
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        cursor = conn.cursor()


        query = sql.SQL("INSERT INTO tokens (user_id, token_no) VALUES (%s, %s)")
        cursor.execute(query, (user_id, token))

        conn.commit()
        cursor.close()
        conn.close()

        return True
    except Exception as e:
        print(e)
        return False


async def get_token_from_database(user_id):
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        cursor = conn.cursor()

        query = sql.SQL("SELECT token_no FROM tokens WHERE user_id = %s LIMIT 1")
        cursor.execute(query, (user_id,))

        row = cursor.fetchone()
        token = row[0] if row else None

        cursor.close()
        conn.close()

        return token
    except Exception as e:
        print("Произошла ошибка при извлечении токена из базы данных:", e)
        return None


async def delete_token_from_database(user_id):
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        cursor = conn.cursor()

        query = sql.SQL("DELETE FROM tokens WHERE user_id = %s")
        cursor.execute(query, (user_id,))

        conn.commit()
        cursor.close()
        conn.close()

        return True
    except Exception as e:
        print("Произошла ошибка при удаление токена из базы данных:", e)
        return None
#
#



























# import pyodbc
#
#
#
# server = 'WIN-3T4UAQMUTGD\\SQLEXPRESS'
# database = 'bot'
# username = 'AslanPAPA'
# password = 'Aslan_2006'
#
#
# async def insert_token_into_database(user_id, token):
#     try:
#
#         conn = pyodbc.connect(
#             f'DRIVER=SQL Server;'
#             f'SERVER={server};'
#             f'DATABASE={database};'
#             f'UID={username};'
#             f'PWD={password};'
#         )
#
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO Tokens (user_id, token) VALUES (?,?)", (user_id, token))
#         conn.commit()
#         cursor.close()
#         conn.close()
#
#         return True
#     except Exception as e:
#         print(e)
#         return False
#
# async def get_token_from_database(user_id):
#     try:
#         conn = pyodbc.connect(
#             f'DRIVER=SQL Server;'
#             f'SERVER={server};'
#             f'DATABASE={database};'
#             f'UID={username};'
#             f'PWD={password};'
#         )
#
#         cursor = conn.cursor()
#         cursor.execute("SELECT TOP 1 token FROM Tokens WHERE user_id = ? ", user_id)
#         row = cursor.fetchone()
#         token = row[0] if row else None
#         cursor.close()
#         conn.close()
#
#         return user_id
#     except Exception as e:
#         print("Произошла ошибка при извлечении токена из базы данных:", e)
#         return None