import socket
import datetime as datetime
import os

from funcionesServer.login import validateLogin
from funcionesServer.register import registerUser, checkNameAvailable, checkSpaces, availableMail
from funcionesServer.cifrado import cifrado
from funcionesServer.mails import checkMail

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
            datos = {}

            infoUser = '\nNombre de usuario:\n'
            conn.sendall(infoUser.encode())

            nombre = conn.recv(4096)

            datos['name'] = nombre.decode()

            passUser = '\nContraseña de usuario:\n' 
            conn.sendall(passUser.encode())

            passwd = conn.recv(4096)

            datos['password'] = passwd.decode()

            verifyuser = validateLogin(datos)

            if verifyuser['status'] == 404:
                    conn.sendall(verifyuser['info'].encode())

            elif verifyuser['status'] == 406:
                    conn.sendall(verifyuser['info'].encode())

                    intentos = 0

                    while True:
                        data = conn.recv(4096)

                        datos['password'] = data.decode()

                        verifyuser = validateLogin(datos)

                        if verifyuser['status'] == 200:
                            conn.sendall(verifyuser['info'].encode())
                            break

                        elif intentos == 3:
                            conn.sendall('Cantidad de intentos alcanzados, intentelo de nuevo mas tarde'.encode())
                            break
                        else:
                            intentos+=1
                            conn.sendall(verifyuser['info'].encode())




            elif verifyuser['status'] == 200:     
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


            email ='\n\nEmail del usuario:\n\n'

            conn.sendall(email.encode())

            emailUser = conn.recv(4096)

            if availableMail(emailUser.decode()) == False:
                 while True:
                        email = 'Este mail ya ha sido registrado.Por favor introduzca otro.\n\nEmail del usuario:\n\n'

                        conn.sendall(email.encode())

                        emailUser = conn.recv(4096)
                      
                        if availableMail(emailUser.decode()) == True:
                            break                      

            verifyEmail = checkMail(emailUser.decode())

            if verifyEmail == False:
                 
                 while True:
                        email = 'Por favor escribe un correo electrónico valido.\n\nEmail del usuario:\n\n'

                        conn.sendall(email.encode())

                        emailUser = conn.recv(4096)

                        verifyEmail = checkMail(emailUser.decode())
                      
                        if verifyEmail == True:
                            break                      


            datos['email'] = emailUser.decode()
            datos['directorio'] = nombreUser.decode().upper()
            datos['rol'] = 'client'

            if registerUser(datos) == False:
                     while True:
                          
                        advise = 'Algo ha salido mal al finalizar el registro, por favor vuelva a intentarlo\n\nEscriba "finalizar" para volver al menú\n\n'

                        conn.sendall(advise.encode())

                        respuesta = conn.recv(4096)    

                        if respuesta.decode() == 'finalizar':
                             break         
                        

            elif registerUser(datos) == True:

                os.system('mkdir directorios/{}'.format(datos['directorio']))
                os.system('mkdir ../cliente/directorios/{}'.format(datos['directorio']))
                


print('Servidor cerrado')
socket_server.close()