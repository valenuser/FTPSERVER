from db import Database
from funcionesServer.cifrado import decifrado

def validateLogin(datosUser):
    user = Database()



    dato = user.readDB(datosUser['name'])



    statusData = {}

    if len(dato) == 0:

        statusData['status'] = 404
        statusData['info'] = '\n\nUsuario introducido no existente\n\n'

        return statusData
        
    else:

        pass_decifrado = decifrado(datosUser,dato[0][0])

        if pass_decifrado == True:
            statusData['status'] = 200
            statusData['info'] = '\n\nBienvenido {}!\n\n'.format(datosUser['name'])

            return statusData
        else:
            statusData['status'] = 406
            statusData['info'] = '\n\nContraseña incorrecta, por favor intentelo de nuevo.\n\n'    

            return statusData