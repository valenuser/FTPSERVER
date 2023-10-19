import os


def crearFichero(fichero):
    nombre = fichero['nombre']+'.txt'
    with open(nombre,'w') as crear:
        crear.write(fichero['texto'])

    os.system('cp {} ../cliente/directorios/{}'.format(nombre,fichero['user'].upper()))
    os.system('mv {} directorios/{}'.format(nombre,fichero['user'].upper()))