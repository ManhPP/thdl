from configparser import ConfigParser
from pathlib import Path

import psycopg2


def config_db(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(f"{Path(__file__).parent}/{filename}")

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config_db()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = [
        """
        CREATE TABLE IF NOT EXISTS price (
            id SERIAL PRIMARY KEY,
            product_name VARCHAR NOT NULL,
            now_price int NOT NULL,
            old_price int NOT NULL,
            shop VARCHAR NOT NULL
        )
        """
    ]
    conn = None
    try:
        params = config_db()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def delete(table):
    """ delete part by part id """
    conn = None
    rows_deleted = 0
    try:
        params = config_db()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {table}")
        rows_deleted = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted


def insert(shop, product_name, now_price, old_price):
    """ insert a new vendor into the vendors table """
    sql = "INSERT INTO price (product_name, now_price, old_price, shop) VALUES(%s, %s, %s, %s);"
    conn = None
    try:
        params = config_db()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (product_name, now_price, old_price, shop,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_product(shop=None):
    sql = f"SELECT * FROM price"
    if shop:
        sql = f"{sql} WHERE shop like '%{shop}%';"
    conn = None
    rows = []
    try:
        params = config_db()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        print("The number of parts: ", cur.rowcount)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows


if __name__ == '__main__':
    get_product()
