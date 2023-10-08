import sqlite3


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def _execute_commands(self, statements: [(str, tuple)]):
        if self.conn is not None:
            for command, params in statements:
                self.conn.execute(command, params)
                self.conn.commit()
        else:
            raise ConnectionError("You need to create connection to database!")

    def _execute_commands_select(self, commands: [str]):
        if self.conn is not None:
            cur = self.conn.cursor()
            data = []
            for command in commands:
                cur.execute(command)
                data.append([list(elem) for elem in cur.fetchall()])
            return data
        else:
            raise ConnectionError("You need to create connection to database!")

    def start(self):
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self._execute_commands([
            ('CREATE TABLE IF NOT EXISTS "offices" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, "number" TEXT NOT NULL);', ()),
            ('CREATE TABLE IF NOT EXISTS "streets" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, "name" TEXT NOT NULL, "office_id" INTEGER NOT NULL, FOREIGN KEY(office_id) REFERENCES offices(id));', ()),
            ('CREATE TABLE IF NOT EXISTS "parcels" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, "office_id" INTEGER NOT NULL, "street_id" INTEGER NOT NULL, "type" INTEGER, FOREIGN KEY(office_id) REFERENCES offices(id), FOREIGN KEY(street_id) REFERENCES streets(id));', ()),
            ('CREATE TABLE IF NOT EXISTS "users" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, "username" TEXT NOT NULL UNIQUE, "password" TEXT NOT NULL, permissions INTEGER NOT NULL);', ()),
        ])

    def stop(self):
        self.conn.close()

    def get_data(self):
        data = self._execute_commands_select([
            'SELECT * FROM offices;',
            'SELECT * FROM streets;',
            'SELECT * FROM parcels;',
            'SELECT * FROM users;',
        ])
        return data

    def insert_data(self, offices_data: [tuple], streets_data: [tuple], parcels_data: [tuple], users_data: [tuple]):
        self._execute_commands(
            [("INSERT INTO offices (id, number) VALUES (?, ?);", (id_, number)) for id_, number in offices_data] +
            [("INSERT INTO streets (id, name, office_id) VALUES (?, ?, ?);", (id_, name, office_id)) for id_, name, office_id in streets_data] +
            [("INSERT INTO parcels (id, office_id, street_id, type) VALUES (?, ?, ?, ?);", (id_, office_id, street_id, type_)) for id_, office_id, street_id, type_ in parcels_data] +
            [("INSERT INTO users (id, username, password, permissions) VALUES (?, ?, ?, ?);", (id_, username, password, permissions)) for id_, username, password, permissions in users_data]
        )
        return True

    def clear_data(self):
        """
        Clear all data in all tables.
        """
        self._execute_commands([
            ("DELETE FROM offices;", ()),
            ("DELETE FROM streets;", ()),
            ("DELETE FROM parcels;", ()),
            ("DELETE FROM users;", ()),
        ])
        return True
