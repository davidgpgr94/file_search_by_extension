#!C:\Python27 python
# -*- coding: utf-8 -*-
import sys
import argparse
from os import walk, makedirs
from os.path import join, dirname, exists
import binascii
import shutil
import errno
from Tkinter import *

def copy_files(files, src ,dst):
    for archivo in files:
        path_archivo = archivo[len(src):]
        if archivo[len(src):][0] == '\\' or archivo[len(src):][0] == '/':
            path_archivo = path_archivo[1:]
        destino = join(dst, path_archivo)
        if not exists(dirname(destino)):
            try:
                makedirs(dirname(destino))
                shutil.copy2(archivo, destino)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        else:
            shutil.copy2(archivo, destino)
    if len(files) == 0:
        print "None files copied into " + dst
    else:
        print "Files copied into " + dst

PROGRAM_NAME = 'search_by_extension'
PROGRAM_VERSION = '0.1'

parser = argparse.ArgumentParser(prog=PROGRAM_NAME,description='%(prog)s is a file search by extension using the "magic numbers". Tested on Windows 10 with Python 2.7.15. customsigs_GCK.txt is required to be in the same folder than %(prog)s. You can download it from https://www.garykessler.net/software/FileSigs_20151213a.zip')

#mandatory_options = parser.add_argument_group('Mandatory options', '')
#mandatory_options.add_argument("-e", "--ext", help="Set the file format to search without the point (.)", type=str, required=True)

exclusion = parser.add_argument_group("Mutually exclusive arguments. It's mandatory to choose one").add_mutually_exclusive_group(required=True)
exclusion.add_argument("-i", "--inf", help="See the extensions that can be recognized", action="store_true")
exclusion.add_argument("-e", "--ext", help="Set the file format to search without the point (.)", type=str)

parser._optionals.title = 'Optional arguments'

parser.add_argument("-s", "--start", help="Set the directory where start to search - By default, it will start in the same directory as %(prog)s", type=str)
parser.add_argument("-t", "--to", help="Set the directory where to copy the found files - By default, found files will be copied into "+PROGRAM_NAME+"_copy", type=str)
parser.add_argument("-f", "--few", help="Use this option to select which files do you want to copy - Without this option, it will copy all found files", action="store_true")

#parser.add_argument("-i", "--inf", help="See the extensions that can be recognized", action="store_true")
parser.add_argument('-v', '--version', action='version', version='%(prog)s v{}'.format(PROGRAM_VERSION), help="Show program's version number and exit")
parser.add_argument("-d", "--dev", action="store_true", help="See the magic number(s) of the indicated extension. Will not copy anything and will not search any file with the indicated extension")
args = parser.parse_args()

# Cargamos el diccionario a partir del fichero customsigs_GCK.txt que nos relaciona la extension con su numero magico
extensiones = {} #clave: extension , valor: lista con el/los numero(s) magico(s)
f = open("customsigs_GCK.txt", "r")
while True:
    linea = f.readline()
    if not linea:
        break
    formato = linea.split(",") # in formato[0] will be a extension's description
    formato[1] = formato[1].replace(' ', '').upper() # the extension's magic_number
    formato[2] = formato[2].replace('\n', '') # the extension
    if '|' in formato[2]:
        same = formato[2].split("|")
        for s in same:
            #extensiones[s].append(formato[1])
            if extensiones.has_key(s):
                extensiones[s].append(formato[1])
            else:
                extensiones[s] = [formato[1]]
    else:
        if extensiones.has_key(formato[2]):
            extensiones[formato[2]].append(formato[1])
        else:
            extensiones[formato[2]] = [formato[1]]
f.close()

# Si introducen la opcion -i, mostramos las extensions reconocidas y finalizamos el programa
if args.inf:
    inf = ''
    for item in extensiones:
        if inf == '':
            inf = item
        else:
            inf = inf + ", " + item
    print inf
    sys.exit()

# Vemos si la extension que quiere buscar el usuario esta en el diccionario que hemos cargado para poder dar soporte para esa extension
ext = args.ext.upper()
if not extensiones.has_key(ext):
    sys.exit("Extension not supported")

# Development option
if args.dev:
    print "Extension:", ext
    print "Magic number:", extensiones[ext]
    sys.exit()


# Seteamos el directorio donde empezar a buscar. Por defecto sera el directorio donde se encuentre el script
start_directory = "."
if args.start:
    start_directory = args.start

# Seteamos el directorio donde se copiaran los ficheros encontrados. Por defecto sera [nombreScript]_copy
dir_to_copy = PROGRAM_NAME + "_copy" 
if args.to:
    dir_to_copy = args.to

# Nos quedamos con la lista de numeros magicos correspondiente a la extension indicada
magic_numbers = extensiones[ext]

# Metemos en archivos_encontrados la ruta relativa a start_directory de los archivos encontrados con la extension indicada por el usuario
archivos_encontrados = []
for (path, carpetas, archivos) in walk(start_directory):
    for archivo in archivos:
        #print(path)
        ruta_relativa_archivo = join(path, archivo)
        f = open(ruta_relativa_archivo, "rb")
        content = f.read()
        f.close()
        hex_file = binascii.hexlify(content).upper()
        for magic_number in magic_numbers:
            if magic_number in hex_file:
                archivos_encontrados.append(ruta_relativa_archivo)
                break
            

# Si nos indica que quiere copiar algunos ficheros (-f) mostramos los archivos encontrados mediante una interfaz grafica
# para que seleccione aquellos mediante checkbox
if args.few:
    check_boxes = {}
    master = Tk()
    master.title("Select files")
    Label(master, text="Select the files that you want to copy").pack()
    for archivo in archivos_encontrados:
        aux = BooleanVar()
        check_boxes[archivo] = aux
        Checkbutton(master, text=archivo[len(start_directory):], variable=check_boxes[archivo]).pack()
    
    selected = []

    def copySelectedFiles():
        for key in check_boxes:
            if check_boxes[key].get():
                selected.append(key)
        copy_files(selected, start_directory, dir_to_copy)
        master.quit()

    Button(master, text="Select", command=copySelectedFiles).pack()
    master.mainloop()
else:
    copy_files(archivos_encontrados, start_directory, dir_to_copy)