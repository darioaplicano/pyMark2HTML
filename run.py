# -*- encoding: utf-8 -*-
"""
    pyTraslate v0.1.2015.02.06
    Este programa esta dedicado a convertir código escrito en el lenguaje MarkDown a HTML

"""

# Se importa todos los elementos de plex
from plex import *

class Analizador(Scanner):

    def __init__(self):

        """
        Se definen las expresiones regulares para analizar el archivo .md
        """

        #cursiva: Busca expresiones que inicien con * y terminen con *
        cursiva = Str("*") + Rep1(AnyBut("*")) + Str("*")

        #negrita: Busca expresiones que inicien con ** y terminen con **
        negrita = Str("**") + Rep1(AnyBut("**")) + Str("**")

        #negritaCursiva: Busca expresiones cuyo inicio sea ** y contenga cursivas, terminando en **
        negritaCursiva = Str("**") + Rep1(AnyBut("**") | Alt(cursiva)) + Str("**")

        #cursivaNegrita: Busca expresiones cuyo inicio sea * y contenga negritas, terminando en *
        cursivaNegrita = Str("*") + Rep1(AnyBut("*") | Alt(negrita)) + Str("*")

        #lista: Expresiones cuyo comienzo sea un -
        lista = Str("-") + Rep(AnyBut("\n"))

        #cita: Expresiones cuyo comienzo sea un >
        cita = Str(">") + Rep(AnyBut("\n"))

        #URL: Expresiones con el formato [texto](url)
        URL = Str("[") + Rep(AnyBut("]")) + Str("](") + Rep(AnyBut(")")) + Str(")")

        #imagen: Expresiones con el formato ![texto](url)
        imagen = Str("![") + Rep(AnyBut("]")) + Str("](") + Rep(AnyBut(")")) + Str(")")

        #linea: Identifica la secuencia de tres o mas *
        linea = Str("***") + Rep(Any("*")) + Str("\n")

        #letra: Todo aquello perteneciente en el rango a-z o A-Z
        letra = Range("azAZ")

        #digito: Todo aquello perteneciente en el rango 0-9
        digito = Range("09")

        #simbolo: Todo aquel que coincida con alguno de los siguientes
        simbolo = Str("#", "$", "%", "'", "(", ")", "+", ",", ".", "/", ":", ";", "<", "=", "?", "@", "\\", "]", "^",
                      "_", "`", "{", "|", "}", "~")

        #casoEspecial: Representa una forma especial al usar los asteriscos (*)
        casoEspecial = Rep1(Str("*")) + Rep(Str(" ")) + Rep(Str("*"))

        #parrafo: Comienza con alguna letra, digito
        parrafo = (letra | digito | Str(" ")) + Rep(AnyBut("\n")) + Str("\n")

        #ignorar: Para poder obviar los saltos de lineas
        ignorar = Any("\n")

        #lexicon: Es el que realiza el análisis del documento, con las expresiones anteriores
        self.lexicon = Lexicon([
            (linea, 'linea'),
            (URL, 'URL'),
            (imagen, 'imagen'),
            (lista, 'lista'),
            (cita, 'cita'),
            (cursiva, 'cursiva'),
            (negrita, 'negrita'),
            (cursivaNegrita, 'cursivaNegrita'),
            (negritaCursiva, 'negritaCursiva'),
            (parrafo, 'parrafo'),
            (ignorar, IGNORE)
            ])

        #analizador: Guarda la información del scanner del documento
        self.analizador = ""

        #html: Permite la comunicación con el archivo html
        self.html = ""

        #muestra: Almacena cada una de las tuplas encontradas por el lexicon
        self.muestra = []

    '''
    Este método hace una lectura al documento con el lenguaje fuente

    Variables:
        filename: Contiene el nombre del archivo a leer
        f: es el archivo leido
    '''
    def leerMarkDown(self):
        filename = "markDown.md"
        f = open(filename, "r")
        self.analizador = Scanner(self.lexicon, f, filename)

    '''
    Este método llenar un archivo CSS creado por este programa con identificadores, clases, entre otros...
    '''
    def llenarCSS(self):
        self.html = open('css.css', 'a')
        self.html.write("#imagen{\n"
                        "       height: 300px;\n"
                        "       width: 300px;\n"
                        "}")
        self.html.write("\n#parrafo{\n"
                        "       background-color: Grey;\n"
                        "}")
        self.html.write("\nbody{\n"
                        "   background-color: #cccccc;\n"
                        "}")
        self.html.write("\n.btn-ttc,\n"
                        ".btn-ttc:hover,\n"
                        ".btn-ttc:active{\n"
                        "   color: white;\n"
                        "   text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.25);\n"
                        "   background-color: #007da7;\n"
                        "}")
        self.html.write("\n.btn-ttc{"
                        "   background-repeat: repeat-x;\n"
                        "   background-image: linear-gradient(top, #009ED2 0%, #007DA7 100%);\n"
                        "}")
        self.html.write("\n.btn-ttc:hover{\n"
                        "   background-position: 0 -15px;\n"
                        "}")
        self.html.write("\nblockquote{\n"
                        "   background: #f9f9f9;\n"
                        "   border-left: 10px solid #ccc;\n"
                        "   margin: 1.5em 10px;\n"
                        "   padding: 0.5em 10px;\n"
                        "   quotes: \"\\201C\"\"\\201D\"\"\\2018\"\"\\2019\";\n"
                        "}")
        self.html.write("\nblockquote:before {\n"
                        "   color: #ccc;\n"
                        "   content: open-quote;\n"
                        "   font-size: 4em;\n"
                        "   line-height: 0.1em;\n"
                        "   margin-right: 0.25em;\n"
                        "   vertical-align: -0.4em;\n"
                        "}")
        self.html.write("\nblockquote p {\n"
                        "   display: inline;\n"
                        "}")
        self.html.close()

    '''
    Crea un archivo con extensión .css el cual contendrá estilos propios para personalizar el documento
    convertido
    '''
    def crearCSS(self):
        self.html = open('css.css', 'w')
        self.html.close()
        self.llenarCSS()

    '''
    Crea un archivo con extensión .html en donde se almacenará el lenguaje fuente convertido
    '''
    def crearHTML(self):
        self.html = open('html.html', 'w')
        self.html.close()
        self.crearCSS()

    '''
    En este método se almacena en la variable muestra, todas las tuplas encontradas por el lexicon
    '''
    def llenarMuestra(self):
        while 1:
            elemento = self.analizador.read()
            self.muestra.append(elemento)
            if elemento[0] is None:
                break

    '''
    Este método, escribe dentro del documento html la estructura básico de
    html5 y además de eso, los links redireccionando a componentes de bootstrap
    para personalizar el documento creado
    '''
    def llenarEncabezado(self):
        self.html = open('html.html', 'a')
        self.html.write("<!DOCTYPE html>\n")
        self.html.write("<html>\n")
        self.html.write("   <head>\n")
        self.html.write("       <meta charset=\"UTF-8\">\n")
        self.html.write("       <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n")
        self.html.write("       <title>pyTranslater</title>\n")
        self.html.write("       <link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/boo"
                        "tstrap.min.css\">\n")
        self.html.write("       <link href=\"css.css\" rel=\"stylesheet\" type=\"text/css\"/>\n")
        self.html.write("   </head>\n")
        self.html.write("   <body>\n")
        self.html.write("       <div class=\"container\">\n")
        self.html.close()

    '''
    Este método complementa el metodo llenarHTML con la parte terminal del documento HTML
    '''
    def llenarFinal(self):
        self.html = open('html.html', 'a')
        self.html.write("        <footer>\n"
                        "           <hr>\n"
                        "           <p>Elaborado por: Alex Dario Flores Aplicano - 20112300146</p>\n"
                        "           <p>Información de contacto: <a href=\"www.facebook.com/darioaplicano\">\n"
                        "               aplicano0921@gmail.com</a>.</p>\n"
                        "        </footer>\n")
        self.html.write("       </div>\n")
        self.html.write("       <script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js\"></scr"
                        "ipt>\n")
        self.html.write("       <script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js\"></s"
                        "cript>\n")
        self.html.write("   </body>\n")
        self.html.write("</html>\n")
        self.html.close()

    '''
    Este método toma la tupla con el representante parrafo y concatena etiquetas html
    '''
    def validarParrafo(self, elemento, estado):
        ingresar = "        <p class=\"lead\" id=\"parrafo\">" + elemento + "        </p>"
        if estado == 1:
            ingresar += "<br>"
        return ingresar

    '''
    Mediante este método, se validan aquellas tuplas que tienen como representante el termino cursiva
    Variables:
        elemento: Este contienen el valor de la tupla representada
        estado: Permite o no agregar la etiqueta <br> en el caso de ser necesario
    '''
    def validarCursiva(self, elemento, estado):
        ingresar = ""
        for letra in range(1, len(elemento)-1):
            ingresar += elemento[letra]
        ingresar += "\n"
        ingresar = self.validar(ingresar)
        ingresar = "        <p><i>" + ingresar + "</i></p>"
        if estado == 1:
            ingresar += "<br>"
        return ingresar

    '''
    Mediante este método, se valian aquellas tuplas que tienen como representante el termino linea
    '''
    def validarLinea(self, elemento, estado):
        ingresar = ""
        ingresar = "        <hr>"
        return ingresar

    '''
    Mediante este método, se puede retornar la validacion encontrada
    Variable:
        ayuda: Es el nuevo escaner al documento de ayuda
    '''
    def crearValidacion(self, ayuda):
        retornar = ""
        while 1:
            print "llego aqui"
            ayudaLectura = ayuda.read()
            print "paso esto"
            print "esta en lista", ayudaLectura
            if ayudaLectura[0] is None:
                break
            if ayudaLectura[0] == 'URL':
                retornar += self.validarURL(ayudaLectura[1], 2)
            if ayudaLectura[0] == 'cursiva':
                retornar += self.validarCursiva(ayudaLectura[1], 2)
            if ayudaLectura[0] == 'negrita':
                retornar += self.validarNegrita(ayudaLectura[1], 2)
            if ayudaLectura[0] == 'imagen':
                retornar += self.validarImagen(ayudaLectura[1], 2)
            if ayudaLectura[0] == 'cita':
                retornar += self.validarCita(ayudaLectura[1], 2)
            if ayudaLectura[0] == 'negritaCursiva':
                retornar += self.validarNegritaCursiva(ayudaLectura[1], 2)
            if ayudaLectura[0] == 'cursivaNegrita':
                retornar += self.validarCursivaNegrita(ayudaLectura[1], 2)
            if ayudaLectura[0] == 'linea':
                retornar += self.validarLinea(ayudaLectura[1], 2)
            if ayudaLectura[0] == 'parrafo':
                retornar += ayudaLectura[1]
        return retornar

    '''
    Este método verifica dentro de cada una de las muestras, para encontrar otras y ser representadas
    en HTML

    variable:
        ingresar: Representa la muestra a evaluar
    '''
    def validar(self, ingresar):
        ayudaName = 'ayuda.md'
        ayuda = open(ayudaName, 'w')
        ayuda.close()
        ayuda = open(ayudaName, 'a')
        ayuda.write(ingresar)
        ayuda.close()
        ayuda = open(ayudaName, 'r')
        ayuda = Scanner(self.lexicon, ayuda, ayudaName)
        retornar = self.crearValidacion(ayuda)
        return retornar

    '''
    Este método valida las listas, verificando si además del primer elemento de la lista
    se encuentran más de estos de forma continua

    variables:
        posicion: Contiene el número de la tupla encontrada por el lexicon

    Retorna la información a ser escrito en el archivo HTML, además de la posicion segun el numero de
    elementos consecutivos encontrados
    '''
    def validarLista(self, posicion, estado):
        print "posicion: ", posicion
        ingresar = ""
        for letra in range(1, len(self.muestra[posicion][1])):
            if letra == 1 and self.muestra[posicion][1][letra] == ' ':
                ''''''
            else:
                ingresar += self.muestra[posicion][1][letra]
        ingresar += "\n"
        ingresar = self.validar(ingresar)
        print "Se retorno: ", ingresar
        ingresar = "        <ul class=\"list-group\">\n            <li class=\"list-group-item\">" + ingresar + "</li>\n"
        while self.muestra[posicion+1][0] == 'lista':
            ingresar += self.ingresarEnLista(self.muestra[posicion+1][1])
            posicion += 1
        ingresar += "        </ul>"
        if estado == 1:
            ingresar += "<br>"
        print "ultima posicion: ", posicion
        return ingresar, posicion

    '''
    En el caso de que se encuentren elementos de listas seguidos, se llama a este método
    permitiendo concatenarlos en una sola etiqueta <ul>
    '''
    def ingresarEnLista(self, elemento):
        sinGuion = ""
        ingresar = ""
        for letra in range(1, len(elemento)):
            sinGuion += elemento[letra]
        contador = 0
        while sinGuion[contador] == ' ':
            contador += 1
        for letra in range(contador, len(sinGuion)):
            ingresar += sinGuion[letra]
        ingresar += "\n"
        ingresar = self.validar(ingresar)
        ingresar = "            <li class=\"list-group-item\">" + ingresar + "</li>\n"
        return ingresar

    '''
    Este método es llamado al encontrarse un representante cita dentro de las tuplas de muestra
    '''
    def validarCita(self, elemento, estado):
        ingresar = ""
        for letra in range(1, len(elemento)):
            ingresar += elemento[letra]
        ingresar += "\n"
        ingresar = self.validar(ingresar)
        ingresar = "        <blockquote>\n          <p>" + ingresar + "</p>\n        </blockquote>"
        if estado == 1:
            ingresar += "<br>"
        return ingresar

    '''
    Mediante este método de clase, se convierten las expresiones de URL en markDown
    a expresiones URL de HTML con la etiqueta <a>
    '''
    def validarURL(self, elemento, estado):
        ingresar = ""
        contador = 1
        for letra in range(1, len(elemento)):
            if elemento[letra] != ']':
                ingresar += elemento[letra]
                contador += 1
            else:
                break
        ingresar += "\n"
        ingresar = self.validar(ingresar)
        href = ""
        for letra in range(contador+2, len(elemento)-1):
            href += elemento[letra]
        ingresar = "        <a href=\"" + href + "\" class=\"btn btn-ttc\" role=\"button\">" + ingresar + "</a>"
        if estado == 1:
            ingresar += "<br>"
        return ingresar

    '''
    Mediante este método de clase, se convierten las expresiones de imagen en markDown
    a expresiones imagen de HTML con la etiqueta <img>
    '''
    def validarImagen(self, elemento, estado):
        ingresar = ""
        contador = 2
        for letra in range(2, len(elemento)):
            if elemento[letra] != ']':
                ingresar += elemento[letra]
                contador += 1
            else:
                break
        ingresar += "\n"
        ingresar = self.validar(ingresar)
        href = ""
        for letra in range(contador+2, len(elemento)-1):
            href += elemento[letra]
        ingresar = "        <img src=\"" + href + "\" alt=\"" + ingresar + "\" id = \"imagen\" class = \"img-thumbnail img-responsive\">"
        if estado == 1:
            ingresar += "<br>"
        return ingresar

    '''
    A través de este método, se agrega la etiqueta <b> al valor de la tupla encontrada
    con representante negrita, previamente eliminando los asteriscos al principio y al final de la misma
    '''
    def validarNegrita(self, elemento, estado):
        ingresar = ""
        for letra in range(2, len(elemento)-2):
            ingresar += elemento[letra]
        ingresar += "\n"
        ingresar = self.validar(ingresar)
        ingresar = "        <p><b>" + ingresar + "</b></p>"
        if estado == 1:
            ingresar += "<br>"
        return ingresar

    '''
    A través de este método, se agrega la etiqueta <i> al valor de la tupla encontrada
    con representante cursivaNegrita, previamente eliminando los asteriscos al principio y al final de la misma y
    además de eso verificar los elementos negrita dentro del mismo
    '''
    def validarCursivaNegrita(self, elemento, estado):
        ingresar = ""
        for letra in range(1, len(elemento)-1):
            ingresar += elemento[letra]
        ingresar += "\n"
        ingresar = self.validar(ingresar)
        ingresar = "        <p><i>" + ingresar + "</i></p>"
        if estado == 1:
            ingresar += "<br>"
        return ingresar

    '''
    A través de este método, se agrega la etiqueta <b> al valor de la tupla encontrada
    con representante negritaCursiva, previamente eliminando los asteriscos al principio y al final de la misma y
    además de eso verificar los elementos cursiva dentro del mismo
    '''
    def validarNegritaCursiva(self, elemento, estado):
        ingresar = ""
        for letra in range(2, len(elemento)-2):
            ingresar += elemento[letra]
        ingresar += "\n"
        ingresar = self.validar(ingresar)
        ingresar = "        <p><b>" + ingresar + "</b></p>"
        if estado == 1:
            ingresar += "<br>"
        return ingresar

    '''
    Este método es el corazón de la función completa del programa
    mediante este, se gestionan cada una de las tuplas encontradas con el lexicon,
    permitiendo agregarle las etiquetas y escribirlas en el archivo html
    '''
    def llenarHTML(self):
        self.llenarEncabezado()
        self.html = open('html.html', 'a')

        #posicion: Permite manejar que tupla es la que se esta leyendo
        posicion = -1

        #ignorar: Mediante una diferencia de posiciones, permite obviar elementos de lista consecutivos
        ignorar = 0
        for elemento in self.muestra:
            posicion += 1
            print "\n", elemento[0], "\n", elemento[1]
            ingresar = ""
            if ignorar == 0:
                if elemento[0] == 'lista':
                    ingresar, ignorar = self.validarLista(posicion, 2)
                    ingresar += "\n"
                    ignorar -= posicion
                if elemento[0] == 'cursiva':
                    ingresar = self.validarCursiva(elemento[1], 1) + "\n"
                if elemento[0] == 'negrita':
                    ingresar = self.validarNegrita(elemento[1], 1) + "\n"
                if elemento[0] == 'URL':
                    ingresar = self.validarURL(elemento[1], 1) + "\n"
                if elemento[0] == 'imagen':
                    ingresar = self.validarImagen(elemento[1], 1) + "\n"
                if elemento[0] == 'cita':
                    ingresar = self.validarCita(elemento[1], 1) + "\n"
                if elemento[0] == 'negritaCursiva':
                    ingresar = self.validarNegritaCursiva(elemento[1], 1) + "\n"
                if elemento[0] == 'cursivaNegrita':
                    ingresar = self.validarCursivaNegrita(elemento[1], 1) + "\n"
                if elemento[0] == 'linea':
                    ingresar = self.validarLinea(elemento[1], 1) + "\n"
                if elemento[0] == 'parrafo':
                    ingresar = self.validarParrafo(elemento[1], 1) + "\n"
                self.html.write(ingresar)
            else:
                ignorar -= 1
            if elemento[0] is None:
                break
        self.html.close()
        self.llenarFinal()

    '''
    A través de iniciar(), se comienza el programa y se muestra la secuenta que realiza el mismo
    '''
    def iniciar(self):
        self.leerMarkDown()
        self.crearHTML()
        self.llenarMuestra()
        self.llenarHTML()

'''
Elementos inicializadores del programa en general
'''
analizador = Analizador()
analizador.iniciar()