import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

class PG:
    con = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    cur = con.cursor()

    query = """
    Create table if not exists Users(
    id serial primary key,
    user_id bigint unique,
    lastname varchar(255),
    firstname varchar(255),
    created_dat timestamp default CURRENT_TIMESTAMP
    );"""
    cur.execute(query)
    con.commit()
    def add (self, user_id, lastname, firstname):
        query = """
        insert into Users(user_id, lastname, firstname) values (%s, %s, %s)"""
        prams = (user_id, lastname, firstname)
        self.cur.execute(query, prams)
        self.con.commit()
    def select_user(self,user_id):
        query = """
        select * from Users where user_id = %s"""
        prams =(user_id,)
        self.cur.execute(query, prams)
        return self.cur.fetchall()
    def update_data(self,user_id,lastname,firstname):
        query = """
        update Users set lastname = %s, firstname = %s where user_id = %s"""
        prams =(lastname, firstname, user_id)
        self.cur.execute(query, prams)
        self.con.commit()

    def select_users(self,user_id):
        query = """
        select * from Users where user_id = %s"""
        prams =(user_id,)
        self.cur.execute(query, prams)
        return self.cur.fetchall()

    def select_all_users(self,):
        query = """
        select user_id from Users"""
        self.cur.execute(query,)
        self.con.commit()
        data =  self.cur.fetchall()
        return data
