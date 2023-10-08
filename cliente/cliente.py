import socket
import datetime as datetime

HOST = '127.0.0.1'
PORT = 65432

socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


socket_client.connect((HOST,PORT))

data = socket_client.recv(4096)

print(data.decode())

connection = True

while connection:
    dato = input('Cliente -----> ')

    if len(dato) == 0:
        while True:
            print('Por favor envia un mensaje de respuesta')
            dato = input('Cliente -----> ')

            if len(dato) > 0:
                break

    socket_client.sendall(dato.encode())

    respServer = socket_client.recv(4096)

    if respServer.decode() == 'Fin':
        connection = False
    else:

        print(respServer.decode())


print('Cliente cerrado')

socket_client.close()