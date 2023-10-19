from db import Database

def checkNameAvailable(nombre):

    user = Database()

    datos = user.availableName(nombre)

    status = {}

    if len(datos) == 0:

        status['status'] = True
        status['info'] = 'Nombre no existente'
        return status
    else:
        status['status'] = False
        status['info'] = 'El nombre que has introducido ya existe, por favor vuelva a intentarlo.'

        return status


def checkSpaces(nombre):
    state = True
    for i in nombre:
        if ord(i) == 32:
            state = False
            break

    return state


def registerUser(datos):
    user = Database()

    state = user.addUser(datos)

    return state


def availableMail(mail):

    user = Database()

    datos = user.mailCheck(mail)

    if len(datos) == 0:
        return True
    else:
        return False
