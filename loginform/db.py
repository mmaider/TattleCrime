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
                             pub_time DATETIME,
                             title TEXT(500),
                             news_text TEXT(2000),
                             comments TEXT(1000),
                             status VARCHAR(1000),
                             user_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, pub_time, title, news_text, comments, status, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO news 
                          (pub_time, title, news_text, comments, status, user_id) 
                          VALUES (?,?,?,?,?,?)''',
                       (pub_time, title, news_text, comments, status, str(user_id)))
        cursor.close()
        self.connection.commit()

    def update(self, news_id, pub_time, title, news_text, comments, status, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE news 
                        SET pub_time = ?, title = ?, news_text = ?, comments = ?, 
                        status = ?, user_id = ? WHERE id = ?''',
                       (pub_time, title, news_text, comments, status, str(user_id), str(news_id)))
        cursor.close()
        self.connection.commit()

    def get(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE id = ?", [str(news_id)])
        row = cursor.fetchone()
        return row

    def get_all(self, user_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM news WHERE user_id = ? ORDER BY pub_time DESC",
                           (str(user_id),))
        else:
            cursor.execute("SELECT * FROM news")
        rows = cursor.fetchall()
        return rows

    def delete(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM news WHERE id = ?''', [str(news_id)])
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
                             pub_time DATETIME,
                             crime_likes INTEGER,
                             photo VARCHAR(100),
                             username VARCHAR(100),
                             id	INTEGER PRIMARY KEY AUTOINCREMENT
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, crime_name, crime_text, pub_time, crime_likes, photo, username):
        cursor = self.connection.cursor()
        print(crime_name, crime_text, pub_time, crime_likes, photo, username)
        cursor.execute('''INSERT INTO crimes 
                          (crime_name, crime_text, pub_time, crime_likes, photo, username) 
                          VALUES (?,?,?,?,?,?)''',
                       (crime_name, crime_text, pub_time, crime_likes, photo, username))
        cursor.close()
        self.connection.commit()

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM crimes")
        rows = cursor.fetchall()
        return rows

    def get_lasts(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM crimes ORDER BY pub_time DESC LIMIT 10")
        rows = cursor.fetchall()
        return rows

    def delete(self, crime_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM crimes WHERE id = ?''', [str(crime_id)])
        cursor.close()
        self.connection.commit()

    def like(self, crime_id):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE crimes SET crime_likes = crime_likes + 1 WHERE id = ?''', [str(crime_id)])
        cursor.close()
        self.connection.commit()

    def findcrime(self, searchtext):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM crimes WHERE crime_name LIKE '%"+searchtext+"%'")
        rows = cursor.fetchall()
        return rows

    def sort_newest(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM crimes ORDER BY pub_time")
        rows = cursor.fetchall()
        return rows

    def sort_oldest(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM crimes ORDER BY pub_time DESC")
        rows = cursor.fetchall()
        return rows

    def sort_likes(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM crimes ORDER BY crime_likes")
        rows = cursor.fetchall()
        return rows

    def sort_likes_desc(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM crimes ORDER BY crime_likes DESC")
        rows = cursor.fetchall()
        return rows


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
        cursor.execute("SELECT * FROM users WHERE id = ?", [str(user_id)])
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
                       (user_name, password,))
        row = cursor.fetchone()
        return (True, row[0], row[2]) if row else (False,)
