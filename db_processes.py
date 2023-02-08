import sqlite3


def select_info(query):
    conn = sqlite3.connect('vacancy.db')
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    conn.close()
    return result


def insert_info(table_name, data):
    columns = ', '.join(data.keys())
    placeholder = ':' + ', :'.join(data.keys())
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholder})"
    conn = sqlite3.connect('vacancy.db')
    c = conn.cursor()
    c.execute(query, data)
    conn.commit()
    conn.close()

