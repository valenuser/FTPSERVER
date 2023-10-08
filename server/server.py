import socket
import datetime as datetime

from funcionesServer.login import validateLogin
from funcionesServer.register import registerUser, checkNameAvailable, checkSpaces
from funcionesServer.cifrado import cifrado

HOST = '127.0.0.1'
PORT = 65432

socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


socket_server.bind((HOST,PORT))

socket_server.listen()

conn, addr = socket_server.accept()


fechaDatos = [str(datetime.datetime.today().year),str(datetime.datetime.today().month),str(datetime.datetime.today().day)]
horaDatos = [str(datetime.datetime.today().hour),str(datetime.datetime.today().minute),str(datetime.datetime.today().second)]


fecha = '-'.join(fechaDatos)
hora = ':'.join(horaDatos)

inicio = '\n\n1 ---> Iniciar Sesion\n2 ---> Registrarse\n3 ---> Salir del sistema\n\n\n'.format(socket.gethostbyname(socket.gethostname()),fecha,hora)

# bienvenida = 'Bienvenido {}! \nTe has conectado el dia {} a las {}\nQue deseas hacer:\n1 ---> Iniciar Sesion\n2 ---> Registrarse\n3 ---> Salir del sistema\n\n\n'.format(socket.gethostbyname(socket.gethostname()),fecha,hora)

connection = True

while connection:

    conn.sendall(inicio.encode())   

    data = conn.recv(4096)

    if data.decode() == '3':
        conn.sendall('Fin'.encode())
        connection = False
    else:
        if data.decode() == '1':
            infoUser = 'Por favor escriba su nombre de usuario y su contraseña separado por una coma\nEJEMPLO = Benito,1234'
            conn.sendall(infoUser.encode())

            data = conn.recv(4096)

            infoRecibida = data.decode().split(',')

            print(infoRecibida)
            print(len(infoRecibida))

            datos = {}

            if len(infoRecibida) <= 1 or len(infoRecibida) > 2:
                while True:
                    aviso = 'Por favor escriba su nombre de usuario y su contraseña separado por una coma \nEJEMPLO = Benito,1234'
                    conn.sendall(aviso.encode())

                    data = conn.recv(4096)

                    infoRecibida = data.decode().split(',')

                    if len(infoRecibida) == 2:
                         break



            datos['name'] = infoRecibida[0]
            datos['password'] = infoRecibida[1]


            verifyuser = validateLogin(datos)

            if verifyuser['status'] == False:
                    conn.sendall(verifyuser['info'].encode())

            elif verifyuser['status'] == True:     
                    conn.sendall(verifyuser['info'].encode())



        elif data.decode() == '2':

            datos = {}

            nombre = '\n\nRegistro de usuario:\n\nNombre de usuario:\n'

            conn.sendall(nombre.encode())

            nombreUser = conn.recv(4096)

            spaces = checkSpaces(nombreUser.decode())

            if spaces == False:
                while True:
                      
                    nombre = '\n\nPor favor escriba su nombre correctamente, sin espacios, para crear el usuario.\n\nRegistro de usuario:\n\nNombre de usuario:\n'

                    conn.sendall(nombre.encode())

                    nombreUser = conn.recv(4096)

                    spaces = checkSpaces(nombreUser.decode())
                      
                    if spaces:
                         break
                    
            available = checkNameAvailable(nombreUser.decode())
            if available['status']:
                datos['nombre'] = nombreUser.decode()
            else:
                 while True:
                    info = available['info']  
                    conn.sendall(info.encode())

                    nombreUser = conn.recv(4096)

                    available = checkNameAvailable(nombreUser.decode())

                    if available['status']:
                        datos['nombre'] = nombreUser.decode()
                        break
                 


            password = '\n\nContraseña de usuario:\n\n'

            conn.sendall(password.encode())

            passUser = conn.recv(4096)

            spaces = checkSpaces(passUser.decode())

            if spaces == False:
                 while True:
                      
                    password = '\n\nPor favor escriba una contraseña para crear el usuario. \n\nContraseña de usuario:\n'

                    conn.sendall(password.encode())

                    passUser = conn.recv(4096)

                    spaces = checkSpaces(passUser.decode())
                      
                    if spaces == True:
                         break
                    
            infoCifrado = {}

            infoCifrado['nombre'] = nombreUser.decode()
            infoCifrado['password'] = passUser.decode()

                
            passCifrada = cifrado(infoCifrado)
                    
            datos['password'] = passCifrada
            datos['directorio'] = nombreUser.decode().upper()
            datos['rol'] = 'client'

            registerUser(datos)


print('Servidor cerrado')
socket_server.close()