import os


def crearFichero(fichero):
    if '.txt' not in fichero['nombre']:
        nombre = fichero['nombre']+'.txt'

        with open(nombre,'w') as crear:
            crear.write(fichero['texto'])

        os.system('cp {} ../cliente/directorios/{}'.format(nombre,fichero['user'].upper()))
        os.system('mv {} directorios/{}'.format(nombre,fichero['user'].upper()))
    else:
        with open(fichero['nombre'],'w') as crear:
            crear.write(fichero['texto'])

        os.system('cp {} ../cliente/directorios/{}'.format(fichero['nombre'],fichero['user'].upper()))
        os.system('mv {} directorios/{}'.format(fichero['nombre'],fichero['user'].upper()))




def borrarFichero(fichero):
    os.system('')


def verifyFileName(fichero,nombre):

    if '.txt' not in fichero:
        fichero = fichero+'.txt'

    datos = os.listdir("./directorios/{}/".format(nombre.upper()))

    print(fichero)
    print(datos)

    datosFichero = {}

    if fichero in datos:
        datosFichero['status'] =  True
        datosFichero['nombre'] =  fichero
        return datosFichero 
    else:
        datosFichero['status'] =  False
        datosFichero['mensaje'] =  'El archivo que deseas eliminar no existe.'
        return datosFichero 

