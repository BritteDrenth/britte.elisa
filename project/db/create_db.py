import sqlite3 as db

conn = db.connect('registrants.db')

create_registrants_table_query = (''' CREATE TABLE IF NOT EXISTS REGISTRANTS
                                    (ID         INTEGER         PRIMARY KEY,
                                    NAME        TEXT            NOT NULL,
                                    EMAIL       TEXT            NOT NULL UNIQUE,
                                    PASSWORD    TEXT            NOT NULL
                                    );''')

conn.execute(create_registrants_table_query)