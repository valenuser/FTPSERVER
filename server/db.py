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


    def readDB(self,nombre):

        datos = ''

        conn = self.connectDB()

        cursor = conn.cursor()

        sql = "SELECT password_user FROM user where nombre = '{}'".format(nombre)

        cursor.execute(sql)

        datos = cursor.fetchall()

        conn.commit()

        print(datos)

        return datos
    

    def availableName(self,nombre):

        datos = ''
        conn = self.connectDB()

        cursor = conn.cursor()

        sql = "SELECT nombre FROM user WHERE nombre = '{}'".format(nombre)

        cursor.execute(sql)

        datos = cursor.fetchall()
    
        conn.commit()

        print(datos)

        return datos

    def addUser(self,datos):
        try:
            conn = self.connectDB()

            cursor = conn.cursor()


            print(datos)

            sql = "insert into user(nombre,password_user,mail_user,directorio,rol) values ('{}','{}','{}','{}','cliente')".format(datos['nombre'],datos['password'],datos['email'],datos['directorio'])

            cursor.execute(sql)

            conn.commit()

            return True
        
        except Exception as e:
            print(e)
            return False 
        


    def mailCheck(self,mail):

        datos = ''

        conn = self.connectDB()

        cursor = conn.cursor()

        sql = "select mail_user from user where mail_user = '{}'".format(mail)

        cursor.execute(sql)

        datos = cursor.fetchall()

        conn.commit()

        return datos