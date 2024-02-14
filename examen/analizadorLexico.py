from tkinter import *
from tkinter import ttk
import ply.lex as lex

rlexema = list()
valor = ""
reservada = ('FOR', 'DO', 'WHILE', 'IF', 'ELSE', 'STATIC', 'INT', 'FLOAT', 'VOID', 'CHAR', 'PUBLIC')
palabra_reservada = ('AREA', 'ALTURA','BASE',)

tokens = reservada + ('VARIABLE', 'NUMEROE', 'NUMEROD', 'DELIMITADOR', 'OPERADOR','PUNTOCOM',)

def t_OPERADOR(t):
    r'[\+\*-/=]'
    global valor
    valor = "OPERADOR"
    return t

def t_DELIMITADOR(t):
    r'[\(\)\[\]\{\}]'
    global valor
    valor = "DELIMITADOR"
    return t

def t_VARIABLE(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    global valor
    if t.value.upper() in reservada:
        valor = "IDENTIFICADOR"
    elif t.value.upper() in palabra_reservada:
        valor = "Palabra_reservada"
    else:
        valor = "IDENTIFICADOR"
    return t

def t_NUMEROD(t):
    r'[0-9]+\.[0-9]+'
    global valor
    valor = "Decimal"
    return t

def t_NUMEROE(t):
    r'[0-9]+'
    global valor
    valor = "numero"
    return t

def t_PUNTOCOM(t):
    r';'
    global valor
    valor ="PuntoCom"
    return t

t_ignore =" \t "

def t_error(t):
    global rlexema
    estado = {"token":"No Identificado","lexico":str(t.value),"linea":str(t.lineno)}
    rlexema.append(estado)
    t.lexer.skip(1)

def analizar(data):
    global rlexema
    global valor
    global num_linea
    rlexema.clear()
    analizador = lex.lex() 
    salto = data.split("\n")
    num_linea = 1  # Inicializar el número de línea
    for valoresAux in salto:
        analizador.input(valoresAux)
        while True:
            token = analizador.token()
            if not token:
                break
            estado = {"token":valor,"lexico":str(token.value),"linea":str(num_linea)}  # Asignar número de línea
            rlexema.append(estado)
        num_linea += 1  # Incrementar el número de línea después de analizar cada línea

def run():
    global rlexema
    index = 0
    entrada = text1.get("1.0", END)
    analizar(entrada)
    for resultado in rlexema:
        tabla.insert(parent="",index="end",iid=index, text="", values=(
            resultado.get("token"),resultado.get("lexico"),resultado.get("linea")    
        ))
        index = index +1
# Limpiar tabla
def limpiar():
    text1.delete("1.0", END)
    for valor in tabla.get_children():
        tabla.delete(valor)

ventana = Tk()
ventana.geometry("1020x800")
ventana.config(bg="#F5C9DD")
text1 = Text(ventana, bg="#999798")
tabla = ttk.Treeview(ventana)
#colores y texto
boton1 = Button(ventana, text='Run', command=run, bg="green")
boton2 = Button(ventana, text='Limpiar', command=limpiar, bg="red")
###################################################################
text1.place(x=10, y=50, height=300, width=1000)
tabla['columns'] = ('token', 'lexema', 'linea')
#tamaño y colocacion de los botones
boton1.place(x=10, y=10, width=90, height=30)
boton2.place(x=10, y=360, width=90, height=30)
##############################################
tabla.column("#0", width=0, stretch=NO)
tabla.column("token", anchor=CENTER)
tabla.column("lexema", anchor=CENTER)
tabla.column("linea", anchor=CENTER)
tabla.heading("#0", text="", anchor=CENTER)
tabla.heading("token", text="Token", anchor=CENTER)
tabla.heading("lexema", text="Lexema", anchor=CENTER)
tabla.heading("linea", text="Linea", anchor=CENTER)
tabla.place(x=10, y=400, height=350, width=1000)
ventana.mainloop()