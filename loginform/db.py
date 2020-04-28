# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, redirect, session, render_template
from flask_wtf import FlaskForm


class DB:
    def __init__(self):
        conn = sqlite3.connect('news.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class NewsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(100),
                             breakfast VARCHAR(1000),
                             user_id INTEGER,
                             dinner VARCHAR(1000),
                             lunch VARCHAR(1000),
                             BKal INTEGER,
                             DKal INTEGER,
                             LKal INTEGER,
                             health VARCHAR(1000),
                             weight INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, breakfast, user_id, dinner, lunch, BKal, DKal, LKal, health, weight):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO news 
                          (title, breakfast, user_id, dinner, lunch, BKal, DKal, LKal, health, weight) 
                          VALUES (?,?,?,?,?,?,?,?,?,?)''',
                       (title, breakfast, str(user_id), dinner, lunch, BKal, DKal, LKal, health, weight))
        cursor.close()
        self.connection.commit()

    def get(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE id = ?", (str(news_id)))
        row = cursor.fetchone()
        return row

    def get_all(self, user_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM news WHERE user_id = ?",
                           (str(user_id),))
        else:
            cursor.execute("SELECT * FROM news")
        rows = cursor.fetchall()
        return rows

    def delete(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM news WHERE id = ?''', (str(news_id),))
        cursor.close()
        self.connection.commit()


class CrimeModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS crimes 
                            (crime_name VARCHAR(100),
                             crime_text TEXT,
                             crime_likes INTEGER,
                             username VARCHAR(100),
                             id	INTEGER PRIMARY KEY AUTOINCREMENT
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, crime_name, crime_text, crime_likes, username):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO crimes 
                          (crime_name, crime_text, crime_likes, username) 
                          VALUES (?,?,?,?)''',
                       (crime_name, crime_text, crime_likes, username))
        cursor.close()
        self.connection.commit()

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM crimes")
        rows = cursor.fetchall()
        return rows

    def delete(self, crime_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM crimes WHERE id = ?''', (str(crime_id),))
        cursor.close()
        self.connection.commit()

    def like(self, crime_id):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE crimes SET crime_likes = crime_likes + 1 WHERE id = ?''', (str(crime_id),))
        cursor.close()
        self.connection.commit()


class UsersModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             password_hash VARCHAR(128),
                             age INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash, age):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, age) 
                          VALUES (?,?,?)''', (user_name, password_hash, age))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, user_name, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password, ))
        row = cursor.fetchone()
        return (True, row[0], row[2]) if row else (False,)
