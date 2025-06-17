import ply.yacc as yacc

from lex import tokens



def p_body(p):
    '''body : programa
            | programa body'''


def p_programa(p):
    ''' programa : sentencia
              | sentencia programa'''

# Definición de la gramática

def p_sentencia(p):
    '''sentencia : declaracion
                | asignacion
                '''

# Definición de la gramática para declaraciones y asignaciones
def p_declaracion(p):
    '''declaracion : tipo ID PUNTO_Y_COMA
                   | tipo ID ASIGNACION expresion PUNTO_Y_COMA'''
    
def p_char(p):
    'char: CHAR_LITERAL'

def p_string(p):
    'string: STRING_LITERAL'

def p_number(p):
    'number: NUMBER'


def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' (línea {p.lineno})")
    else:
        print("Error de sintaxis al final del archivo.")

# Construir el parser
parser = yacc.yacc()

# Leer el archivo como en lex.py
import os
nombre_archivo = f"algoritmo-{input('Nombre de usuario git (sin .cs): ')}.cs"

try:
    with open(nombre_archivo, "r", encoding="utf-8") as file:
        data = file.read()
except FileNotFoundError:
    print(f" El archivo '{nombre_archivo}' no fue encontrado.")
    exit()

# Parsear
result = parser.parse(data)
print("\nÁrbol de análisis sintáctico:")
print(result)