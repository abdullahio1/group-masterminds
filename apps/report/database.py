# database.py
import psycopg2
from shared.credentials import get_database_credentials
from datetime import datetime


def get_connection() -> psycopg2.extensions.connection:
    try:
        host, database, user, password, port = get_database_credentials()
        return psycopg2.connect(
            host=host,
            dbname=database,
            user=user,
            password=password,
            port=port,
            sslmode="require",
        )
    except psycopg2.OperationalError as e:
        raise ConnectionError(f"Failed to connect to the database: {e}")


def get_time_entries(start_date: datetime, end_date: datetime) -> list[tuple]:
    try:
        with get_connection() as con:
            with con.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 
                        c.id AS consultant_id,
                        cust.id AS customer_id,
                        c.name AS consultant_name,
                        cust.name AS customer_name,
                        CAST(ROUND(SUM(EXTRACT(EPOCH FROM (te.end_time - te.start_time)) / 3600.0 - (te.lunch_break / 60.0)), 2) AS FLOAT) AS net_hours,
                        count(*) as days_worked
                    FROM time_entries te
                    JOIN consultants c ON c.id = te.consultant_id
                    JOIN customers cust ON cust.id = te.customer_id
                    WHERE te.start_time >= %s AND te.end_time <= %s
                    GROUP BY c.id, cust.name, cust.id, cust.name
                    ORDER BY c.id;
                    """,
                    (start_date, end_date),
                )
                return cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as e:
        raise RuntimeError(f"Failed to fetch time entries: {e}")
