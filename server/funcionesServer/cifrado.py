def cifrado(mensaje):
    
    pass_codificado = ''

    lista = [ord(i) for i in str(mensaje['password'])]

    magic_number = 0

    for i in lista:
        magic_number += i


    for i in str(mensaje['password']):
        pass_codificado += chr(magic_number*ord(i))


    datosCifrados = []


    with open('cifrados.txt','r') as listCifrado:
        datosCifrados = listCifrado.readlines()


    with open('cifrados.txt','w') as cifrado:
        info = '{}-{}\n'.format(mensaje['nombre'],magic_number)

        datosCifrados.append(info)
        cifrado.writelines(datosCifrados)

    return pass_codificado


def decifrado(user,password):

    usuariosDatos = []

    with open('cifrados.txt','r') as usuarios:
        datos = usuarios.readlines()        

        for i in datos:
            usuariosDatos.append(i) 


    datoSplit = []

    print(datoSplit)

    for i in usuariosDatos:
        datoSplit.append(i.split('-'))

    print(datoSplit)
    for i in datoSplit:
        a = i[1].split('\n')
        i[1] = a[0]

    userLogin = []


    for i in datoSplit:
        if i[0] == user['name']:
            userLogin.append(i)

    print(userLogin)

    passLogin = ''

    for i in password:
        letra = chr(ord(i)//int(userLogin[0][1]))

        passLogin += letra


    print(user['password'])
    print(passLogin)

    if user['password'] == passLogin:
        return True
    else:
        return False

