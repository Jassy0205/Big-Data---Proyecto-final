from tkinter import *
from tkinter import ttk 
#import numpy as np
from tkinter.font import Font
import matplotlib.pyplot as plt
#from matplotlib.figure import Figure
import unidecode 
import unicodedata
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

#Se extrae el nombre del archivo de las opciones que están en el combobox
def obtener_Doc():
    Doc_elegido = combo.get()
    print(Doc_elegido)
    importarinfo_Json(Doc_elegido)

#Se verifica que el json sea de un PDF o de un TXT, pues cada archivo 
#tiene el nombre de las palabras con sus lineas en una clave diferente
def tipo_texto():
    Doc_elegido = combo.get()

    if ("PDF" in Doc_elegido):
        busqueda = 'Diccionario'
    else: 
        busqueda = 'PalabraLineas'

    return busqueda

#Se extrae el texto copiado en el input
def busqueda_palabra(): 
    texto = entrada.get()
    print("El texto ingresado es:", texto)

    busqueda = tipo_texto()
    palabras_lineas(texto, busqueda)

#Se crea la ventana
ventana = Tk()
#Se configuran los parametros como titulo, tamaño y color de la ventana
xV = 900
ventana.title("FWP Asc")
ventana.geometry("900x350")
ventana['bg'] = '#FCFAFA'

#Cuadro para el titulo
def cuadro_titulo():
    # Crear el lienzo para dibujar
    lienzo = Canvas(ventana, width=811, height=43, background='#FCFAFA')

    # Coordenadas del cuadrado
    x2 = 810
    y2 = 43

    # Dibujar el cuadrado en el lienzo
    lienzo.create_rectangle(3, 3, x2, y2, fill="#FCFAFA", outline="black")
    lienzo.create_text((x2/2)-7, 25, text="FWP Asc", font=lbl_font2)

    #Lugar donde se dibuja el cuadrado
    lienzo.place(x=45, y=30)

#Se establece un formato de texto
lbl_font2 = Font(family="sans_serif", size=15) 
cuadro_titulo()

'''fontdict2 = {'fontweight': 'bold', 'fontsize': 15, 'fontfamily': 'script'}
lbl_font = Font(family="sans_serif", size=20, ) 
label = Label(ventana, font=lbl_font ,text="FWP Asc", background='#FCFAFA')
label.config(fg="#0056B1")
label.place(x=(xV/2)-50, y = 8)'''

#Se crea el combobox, cuya utilidad es elegir el archivo al que se desea procesar
combo = ttk.Combobox(ventana, font=lbl_font2)
combo.place(x=46, y=100)
combo['values'] = ('archivoPDF1.txt', 'archivoPDF2.txt', 'archivoPDF3.txt', "archivoTXT1.txt", "", "archivoTXT2.txt", "archivoTXT3.txt")
combo.current(2) #con esta línea se elige por defecto al que esté en esa posición
#Se crea el botón para seleccionar el archivo del combobox
Button(ventana, command=obtener_Doc, text="Seleccionar", font=lbl_font2, background='#83BDFA').place(x=300, y=95)

#Entrada de la palabra a buscar
entrada = Entry(ventana, font=lbl_font2, width=21)
entrada.place(x=484, y=100)
Button(ventana, command=busqueda_palabra, text="    Buscar    ", font=lbl_font2, background='#83BDFA').place(x=730, y=95)

#Se crea un metodo para importar la información que esté en el archivo escogido
def importarinfo_Json(Doc_elegido):

    with open(Doc_elegido, 'r', encoding="utf-8") as archivo:
    # Carga el contenido del archivo JSON en una variable
        datos_json = json.load(archivo)

    # Ahora se accede a los datos del archivo JSON llamandolos por la clave 
    nombre = datos_json['15palabras']
    Npalabras = datos_json['Npalabras']
    Nlineas = datos_json['Nlineas']
    
    #Se llaman a las funciones que crean los recuadros para mostrar la cantidad de palabras, la cantidad de líneas,
    #y hacer un grafico de barras con la información de las 15 palabras que más aparecen en el texto y el número de veces que lo hacen
    cantidad_palabras(Npalabras)
    cantidad_Lineas(Nlineas)
    dibujar_15palabras(nombre)

#Se importa el diccionario que contiene las palabras del texto como clave y las lineas en las que aparece como valor
def palabras_lineas(texto, busqueda):

    Doc_elegido = combo.get()
    with open(Doc_elegido, 'r', encoding="utf-8") as archivo:
    # Carga el contenido del archivo JSON en una variable
        datos_json = json.load(archivo)

    Plineas = datos_json[busqueda]

    texto = entrada.get()
    #Se llama al metodo que quita las tildes, mayusculas y espacios del texto
    texto = convertir_texto(texto)
    #Se llama al metodo que compara a la palabra que se desea buscar por todas las palabras en el diccionario importado
    lineas = comparar_palabras(Plineas, texto)

    #Se llama al metodo que crea el cuadro donde se muestran las líneas donde aparece la palabra buscada
    Lineas_busqueda(texto, lineas)

#Se crea el metodo que compara a la palabra que se desea buscar con todas las del diccionario
def comparar_palabras(diccionario, palabra):
    bandera = 0
    lineas = 0

    #Se extraen la clave y el valor del diccionario
    for clave, valor in diccionario.items():
        nuevo = convertir_texto(clave)
        #Se define si la palabra a buscar es igual a las del diccionario
        if palabra == nuevo:
            bandera = 1
            lineas = valor
    
    #En caso de que la compatibilidad nunca se de con ninguna de las palabras, se imprime este mensaje
    if bandera == 0: 
        print('palabra no se encuentra en el texto')

    #Se retorna el vector que contiene a las lineas donde aparece la palabra
    return lineas

#En este metodo se ingresa un texto y se retorna el mismo, pero sin mayusculas, tildes o espacios
def convertir_texto(texto):
    # Convertir a minúsculas
    texto = texto.lower()
    # Remover tildes
    texto = unidecode.unidecode(unicodedata.normalize("NFD", texto))
    #Remover espacios
    texto = texto.replace(" ", "")

    return texto

#Crear fondo para items
def cantidad_palabras(nombre):
    # Crear el lienzo para dibujar
    lienzo = Canvas(ventana, width=377, height=43, background='#FCFAFA')
    texto = "Cantidad de palabras: "+str(nombre)

    # Coordenadas del cuadrado
    x2 = 376
    y2 = 43

    # Dibujar el cuadrado en el lienzo
    lienzo.create_rectangle(3, 3, x2, y2, fill="#FCFAFA", outline="black")
    lienzo.create_text(190, 25, text=texto, font=lbl_font2)

    lienzo.place(x=43, y=150)

#Crear fondo para items
def Lineas_busqueda(nombre, lineas):
    # Crear el lienzo para dibujar
    lienzo = Canvas(ventana, width=377, height=43, background='#FCFAFA')

    if lineas == 0:  
        texto = str(nombre)+': NULL'
    else: 
        texto = str(nombre)+': '+str(lineas)

    # Coordenadas del cuadrado
    x2 = 376
    y2 = 43

    # Dibujar el cuadrado en el lienzo
    lienzo.create_rectangle(3, 3, x2, y2, fill="#FCFAFA", outline="black")
    lienzo.create_text(190, 25, text=texto, font=lbl_font2)

    lienzo.place(x=480, y=152)

#Crear fondo para items
def cantidad_Lineas(nombre):
    # Crear el lienzo para dibujar
    lienzo = Canvas(ventana, width=377, height=43, background='#FCFAFA')
    texto = "Cantidad de lineas: "+str(nombre)

    # Coordenadas del cuadrado
    x2 = 376
    y2 = 43

    # Dibujar el cuadrado en el lienzo
    lienzo.create_rectangle(3, 3, x2, y2, fill="white", outline="black")
    lienzo.create_text(195, 25, text=texto, font=lbl_font2)

    lienzo.place(x=43, y=200)

#Proceso de sibujo de la figura
def dibujar_15palabras(nombre):
    datos = nombre
    fontdict = {'fontweight': 'bold', 'fontsize': 10, 'fontfamily': 'serif'}

    figura, ejes = plt.subplots(facecolor='white')
    ejes.set_xticks([])
    ejes.set_yticks([])

    # Crear ejes del diagrama de barras
    ejes = figura.add_subplot(111)

    # Dibujar barras en el diagrama
    ejes.bar(datos.keys(), datos.values(), color='#83BDFA')

    ejes.set_xticklabels(datos.keys(), fontdict=fontdict, rotation=45)

    # Personalizar el diagrama de barras
    ejes.set_xlabel('Palabras')
    ejes.set_ylabel('Cantidad')
    ejes.set_title('15 palabras más usadas en el texto')

    plt.show()

ventana.mainloop()