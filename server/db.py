import pymysql
from dotenv import load_dotenv
import os



load_dotenv()

class Database:

    def __init__(self):
        self.host = os.getenv('host')
        self.user = os.getenv('user')
        self.password = os.getenv('password')
        self.db = os.getenv('db')


    def connectDB(self):
        conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db   
        )

        return conn


    def readDB(self,nombre,password):

        conn = self.connectDB()

        cursor = conn.cursor()

        sql = "SELECT nombre,password_user FROM user where nombre = '{}' AND password_user = '{}' ".format(nombre,password)

        cursor.execute(sql)

        return cursor.fetchall()
    

    def availableName(self,nombre):
        conn = self.connectDB()

        cursor = conn.cursor()

        sql = "SELECT nombre FROM user WHERE nombre = '{}'".format(nombre)

        cursor.execute(sql)

        return cursor.fetchall()