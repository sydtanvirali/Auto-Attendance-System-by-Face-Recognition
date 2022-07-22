from tkinter import messagebox
import sqlite3
import os


class Queries:
    def __init__(self):
        # Create Directory
        self.dir_name = './MyDatabase'
        if not os.path.exists(self.dir_name):
            os.makedirs(self.dir_name)
            print('Database Directory Successfully Created...')

        #  Establish Database Connection
        self.connection = None
        try:
            self.database = './MyDatabase/AttendanceDB.db'
            self.connection = sqlite3.connect(self.database)
        except sqlite3.Error as e:
            print(e)

    #  Creating Table
    def create_table(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as e:
            print(e)

    #  Inserting Values to Table
    def insert(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            messagebox.showinfo('Information', 'Record Inserted Successfully.')
        except sqlite3.Error as e:
            print(e)

    #  Inserting Values Without Showing Messagebox
    def insert_wsm(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            print('Record Inserted Successfully.')
        except sqlite3.Error as e:
            print(e)

    #  Selecting A Single Record & Return It
    def select_one(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.record = cursor.fetchone()
        except sqlite3.Error as e:
            print(e)
        return self.record

    #  Selecting An All Records & Return It
    def select_all(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.records = cursor.fetchall()
        except sqlite3.Error as e:
            print(e)
        return self.records

    #  Deleting A Record
    def delete(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            messagebox.showinfo('Information', 'Record Deleted Successfully.')
        except sqlite3.Error as e:
            print(e)


if __name__ == '__main__':
    obj = Queries()
