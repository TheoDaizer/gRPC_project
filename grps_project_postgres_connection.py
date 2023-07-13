import psycopg2
from psycopg2 import OperationalError

connection_data = {"database": "store", "user": "postgres", "password": "qwe", "host": "127.0.0.1", "port": "5433"}


def create_connection(db_name: str, db_user: str, db_password: str,
                      db_host: str, db_port: str, echo: bool = False):

    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        if echo:
            print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def insert(columns: list, data: list, table_name: str,
           connection, echo: bool = False) -> None:

    data_records = ", ".join(["%s"] * len(data))

    insert_query = (
        f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({data_records})"
    )
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query, data)
        connection.commit()
        if echo:
            print("Data inserted successfully:")
            print(*data)
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def select(columns: list, condition_columns: list, condition_data: list,
           table_name: str, connection, echo: bool = False) -> list:

    condition_records = " AND ".join([f"{condition_column} = %s" for condition_column in condition_columns ])

    select_query = (
        f"SELECT {', '.join(columns)} FROM {table_name} WHERE {condition_records}"
    )
    cursor = connection.cursor()
    try:
        cursor.execute(select_query, condition_data)
        if echo:
            print("Data selected successfully")
        return cursor.fetchall()
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def update(update_columns: list, update_data: list,
           condition_columns: list, condition_data: list,
           table_name: str, connection, echo: bool = False) -> None:

    update_records = ", ".join([f"{update_column} = %s" for update_column in update_columns])
    condition_records = " AND ".join([f"{condition_column} = %s" for condition_column in condition_columns])
    insert_query = (
        f"UPDATE {table_name} SET {update_records} WHERE {condition_records}"
    )
    cursor = connection.cursor()
    try:
        data = update_data + condition_data
        cursor.execute(insert_query, data)
        connection.commit()
        if echo:
            print("Data updated successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


if __name__ == '__main__':
    pass
