from shared.config import load_db_config
import psycopg2
from datetime import datetime

# helper function to set up connection 
def _load() -> psycopg2.extensions.connection:
    return psycopg2.connect(**load_db_config())


# add consultant - returnes id
def add_consultant(name: str, email: str) -> int:

    try:
        # connect to database
        with _load() as con:
            with con.cursor() as cursor:
                # execute query
                cursor.execute(
                    '''
                    INSERT INTO consultants (name, email) 
                    VALUES (%s, %s) RETURNING id
                    ''',
                    (name, email),
                )
                 # fetch & return the new id
                consultant_id = cursor.fetchone()[0]
                return consultant_id  
    except (Exception, psycopg2.DatabaseError) as e:
        print('Database error: ', e)


# add customer - returnes id
def add_customer(name: str) -> int:

    try:
        # connect to database
        with _load() as con:
            with con.cursor() as cursor:
                # execute query
                cursor.execute(
                    '''
                    INSERT INTO customers (name)
                    VALUES (%s) RETURNING id
                    ''',
                    (name, ),
                )
                # fetch & return the new id
                customer_id = cursor.fetchone()[0]
                return customer_id
    except (Exception, psycopg2.DatabaseError) as e:
        print('Database error: ', e)


# find consultant by email - return the id 
def find_consultant(email: str) -> int | None:
     
    try:
        # connect to database
        with _load() as con:
            with con.cursor() as cursor:
                # execute query
                cursor.execute(
                    '''
                    SELECT id
                    FROM consultants
                    WHERE email = %s
                    ''',
                    (email, ),
                )
                # fetch id return id or None
                result = cursor.fetchone()
                if result is None:
                    return None
                else:
                    return result[0]
    except (Exception, psycopg2.DatabaseError) as e:
        print('Database error: ', e)


# find customer return id
def find_customer(name: str) -> int | None:
    try:
        # connect to database
        with _load() as con:
            with con.cursor() as cursor:
                # execute query
                cursor.execute(
                    '''
                    SELECT id
                    FROM customers
                    WHERE name = %s
                    ''',
                    (name, ),
                )
                # fetch id - return id / None
                result = cursor.fetchone()
                if result is None:
                    return None
                else:
                    return result[0]
    except (Exception, psycopg2.DatabaseError) as e:
        print('Database error: ', e)


# add time_entrie
def add_time_entry(
        consultant_id: int, customer_id: int,
        start_time: datetime, end_time: datetime, lunch_break: int
) -> tuple | None:

    try:
        # connect to database
        with _load() as con:
            with con.cursor() as cursor:
                # execute query
                cursor.execute(
                    '''
                    INSERT INTO time_entries
                    (consultant_id, customer_id, start_time, end_time, lunch_break)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id, consultant_id, customer_id
                    ''',
                    (consultant_id, customer_id, start_time, end_time, lunch_break),
                )
                # fetch (id, consultant_id, customer_id) - return tuple
                time_created = cursor.fetchone()
                return time_created
    except (Exception, psycopg2.DatabaseError) as e:
        print('Database error: ', e)