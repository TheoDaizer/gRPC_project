from psycopg2.extensions import connection
from grps_project_postgres_connection import create_connection, insert, select, update
from string import ascii_lowercase as letters
from random import sample, randint
import unittest


connection_data = {"database": "store", "user": "postgres", "password": "qwe", "host": "127.0.0.1", "port": "5433"}
columns = ["id", "name", "quantity"]
table_name = "products"
test_connection = None


class Test_postgres_commands(unittest.TestCase):

    def test_create_connection(self):
        test_connection = create_connection(*connection_data.values())
        self.assertIsInstance(test_connection, connection)

    def test_select(self):
        test_connection = create_connection(*connection_data.values())
        self.assertIsInstance(select(columns, ["id"], [1], table_name, test_connection), list)

    # def test_insert(self):
    #     self.assertIsNone(insert(columns[1:], [''.join(sample(letters, 3)), randint(1, 100)],
    #                              table_name, test_connection))

    def test_update(self):
        test_connection = create_connection(*connection_data.values())
        data1 = select(columns, ["id"], [10], table_name, test_connection)
        update(columns[1:], [''.join(sample(letters, 3)), randint(1, 100)],
               ["id"], [1], table_name, test_connection)

        test_connection = create_connection(*connection_data.values())
        data2 = select(columns, ["id"], [10], table_name, test_connection)

        self.assertNotEqual(data1, data2)


if __name__ == '__main__':
    unittest.main()