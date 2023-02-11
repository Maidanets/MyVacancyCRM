import sqlite3


class Database:
    def __enter__(self):
        self.conn = sqlite3.connect('vacancy.db')
        self.c = self.conn.cursor()
        return self

    def query(self, qry):
        self.c.execute(qry)
        result = self.c.fetchall()
        return result

    def insert(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholder = ':' + ', :'.join(data.keys())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholder})"
        self.c.execute(query, data)
        self.conn.commit()

    def update(self, table_name, data, conditions):
        line = ", ".join([f"{i}=:{i}" for i in data.keys()])
        query = f"UPDATE {table_name} SET {line} WHERE {conditions}"
        self.c.execute(query, data)
        self.conn.commit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.c.close()
        self.conn.close()

