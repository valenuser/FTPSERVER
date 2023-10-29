import socket
import datetime as datetime

HOST = '127.0.0.1'
PORT = 65432



socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


socket_client.connect((HOST,PORT))

data = socket_client.recv(4096)

print(data.decode())

connection = True

session = False

count = 0

pasos = 1

register = 0

wait = 0

while connection:

    if wait == 1:
        print('cargando...')
        wait = 0
    elif session == True and count == 0 and pasos == 1:
        print('cargando...\n')
        pasos+=1
    elif session == True and count == 0 and pasos == 2:
        dato = input('Cliente ------> ')
    elif session == True and count == 0 and pasos == 3:
        print('cargando...')
        dato = 'pass'
        pasos+=1
    elif session == False and count == 0 and pasos == 1 and register == 1:
        dato = 'pass'
        register = 0
    elif session == True and count == 1:
        print('cargando...\n')
        count+=1
    else:
        session = False
        count = 0
        pasos = 1
        register = 0
        dato = input('Cliente -----> ')

    if len(dato) == 0:
        while True:
            print('Por favor envia un mensaje de respuesta')
            dato = input('Cliente -----> ')

            if len(dato) > 0:
                break

    if dato == 'fin' and session == False and count == 0 or dato == 'fin' and session == True and count == 1:
        socket_client.sendall(dato.encode())

        respServer = socket_client.recv(4096).decode()

        connection = False
        socket_client.close()
    else:
        socket_client.sendall(dato.encode())

        respServer = socket_client.recv(4096).decode()


        if ':True' in respServer:
            state = respServer.split(':')

            session = bool(state[1])

            print(state[0])
        elif ':False' in respServer:
            state = respServer.split(':')

            print(state[0])

            pasos+=1

        elif ':pass' in respServer:
            state = respServer.split(':')

            print(state[0])

            wait+=1

        elif 'Usuario registrado' in respServer:

            register+=1

        else:
            print(respServer)


print('Cliente cerrado')
