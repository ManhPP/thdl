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
        CREATE TABLE IF NOT EXISTS cellphones (
            id SERIAL PRIMARY KEY,
            device_id int NOT NULL,
            product_name VARCHAR(255) NOT NULL,
            special_price int NOT NULL,
            old_price int NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS hoang_ha (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            price int NOT NULL,
            listed_price int NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS nguyen_kim (
            id SERIAL PRIMARY KEY,
            device_id int NOT NULL,
            label VARCHAR(255) NOT NULL,
            now_price int NOT NULL,
            old_price int NOT NULL,
            brand VARCHAR(255) NOT NULL,
            currency VARCHAR(255) NOT NULL,
            description VARCHAR NOT NULL
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


def insert_cellphones_list(data_list: dict):
    """ insert multiple vendors into the vendors table  """

    sql = "INSERT INTO cellphones(device_id, product_name, special_price, old_price) VALUES(%s, %s, %s, %s)"
    conn = None
    try:
        # read database configuration
        params = config_db()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql, data_list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_cellphones(device_id, product_name, special_price, old_price):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO cellphones(device_id, product_name, special_price, old_price)
             VALUES(%s, %s, %s, %s) RETURNING id;"""
    conn = None
    vendor_id = None
    try:
        # read database configuration
        params = config_db()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (device_id, product_name, special_price, old_price,))
        # get the generated id back
        vendor_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return vendor_id


def insert_hoang_ha(title, price, listed_price):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO hoang_ha(title, price, listed_price)
             VALUES(%s, %s, %s) RETURNING id;"""
    conn = None
    vendor_id = None
    try:
        # read database configuration
        params = config_db()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (title, price, listed_price,))
        # get the generated id back
        vendor_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return vendor_id


def insert_nguyen_kim(device_id, label, now_price, old_price, brand, currency, des):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO nguyen_kim(device_id, label, now_price, old_price, brand, currency, description)
             VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
    conn = None
    vendor_id = None
    try:
        # read database configuration
        params = config_db()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (device_id, label, now_price, old_price, brand, currency, des,))
        # get the generated id back
        vendor_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return vendor_id


if __name__ == '__main__':
    create_tables()
