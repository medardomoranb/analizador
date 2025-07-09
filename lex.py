import ply.lex as lex
import datetime
import os
import sys


if len(sys.argv) > 1:
    usuario_git = sys.argv[1]
else:
    print("¿Quién está probando el programa?")
    print("1. Medardo Moran")
    print("2. Mario Alvarado")
    print("3. Andres Layedra")

    opciones = {
        "1": "medardomoran",
        "2": "marioalvarado",
        "3": "andreslayedra"
    }

    opcion = input("Ingrese el número correspondiente (1-3): ").strip()
    usuario_git = opciones.get(opcion)

    if not usuario_git:
        print("Opción no válida. Terminando el programa.")
        exit()


# Palabras reservadas

reserved = {
    'bool': 'BOOL',
    'break': 'BREAK',
    'case': 'CASE',
    'char': 'CHAR',
    'class': 'CLASS',
    'continue': 'CONTINUE',
    'default': 'DEFAULT',
    'else': 'ELSE',
    'enum': 'ENUM',
    'float': 'FLOAT',
    'for': 'FOR',
    'if': 'IF',
    'in': 'IN',
    'int': 'INT',
    'is': 'IS',
    'new': 'NEW',
    'null': 'NULL',
    'private': 'PRIVATE',
    'protected': 'PROTECTED',
    'public': 'PUBLIC',
    'return': 'RETURN',
    'static': 'STATIC',
    'string': 'STRING',
    'struct': 'STRUCT',
    'switch': 'SWITCH',
    'this': 'THIS',
    'unchecked': 'UNCHECKED',
    'unsafe': 'UNSAFE',
    'void': 'VOID',
    'while': 'WHILE'
}

# Lista de tokens

tokens = [
    'IDENTIFICADOR',
    'NUMERO',
    'NOMBRE_CLASE',
    'STRING_LITERAL',
    'CHAR_LITERAL',

    # Operadores
    'MAS', 'MENOS', 'MULTIPLICACION', 'DIVISION',
    'MODULO', 'INCREMENTO', 'DECREMENTO',
    'ASIGNACION', 'MAS_ASIGNACION', 'MENOS_ASIGNACION',
    'MULTIPLICACION_ASIGNACION', 'DIVISION_ASIGNACION', 'MODULO_ASIGNACION',
    'IGUAL', 'NO_IGUAL', 'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL',
    'AND', 'OR', 'NOT', 'BITAND', 'BITOR', 'BITXOR', 'BITNOT',
    'COMILLAS_ANGULARES_IZQ', 'COMILLAS_ANGULARES_DER',

    # Delimitadores
    'PARENTESIS_IZQ', 'PARENTESIS_DER', 'LLAVE_IZQ', 'LLAVE_DER', 'CORCHETE_IZQ', 'CORCHETE_DER',
    'COMA', 'PUNTO', 'PUNTO_COMA', 'DOS_PUNTOS', 'PREGUNTA', 'FLECHA',

    # --- INICIO tokens adicionales de Andres Layedra ---
    'FLOAT_LITERAL',     # Ej: 36.6f
    'TRUE_LITERAL',      # true como literal
    'FALSE_LITERAL',     # false como literal
    'XML_COMMENT',       # Comentarios de documentación ///
    'DATE_LITERAL',      # Ej: "2025-06-14"
    'HEX_LITERAL',       # Ej: 0x1F4
    'BIN_LITERAL',      # Ej: 0b1010
    'DECIMAL_LITERAL',
    # --- FIN tokens adicionales de Andres Layedra ---



] + list(reserved.values())

# Expresiones regulares para tokens simples

t_MAS = r'\+'
t_MENOS = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_MODULO = r'%'
t_INCREMENTO = r'\+\+'
t_DECREMENTO = r'--'

t_ASIGNACION = r'='
t_MAS_ASIGNACION = r'\+='
t_MENOS_ASIGNACION = r'-='
t_MULTIPLICACION_ASIGNACION = r'\*='
t_DIVISION_ASIGNACION = r'/='
t_MODULO_ASIGNACION = r'%='

# --- INICIO tokens de Mario Alvarado ---
t_IGUAL = r'=='
t_NO_IGUAL = r'!='
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYOR_IGUAL = r'>='
t_MENOR_IGUAL = r'<='

t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
# --- FIN tokens de Mario Alvarado ---

t_BITAND = r'&'
t_BITOR = r'\|'
t_BITXOR = r'\^'
t_BITNOT = r'~'
t_COMILLAS_ANGULARES_IZQ = r'<<'
t_COMILLAS_ANGULARES_DER = r'>>'

t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'

t_COMA = r','
t_PUNTO = r'\.'
t_PUNTO_COMA = r';'
t_DOS_PUNTOS = r':'
t_PREGUNTA = r'\?'
t_FLECHA = r'=>'


# Reglas con acciones
expecting_class_name = False
clases_declaradas = set()

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    global expecting_class_name

    if expecting_class_name:
        t.type = 'NOMBRE_CLASE'
        clases_declaradas.add(t.value) # Añadir a conjunto de clases declaradas
        expecting_class_name = False
    else:
        t.type = reserved.get(t.value, 'IDENTIFICADOR')

    if t.value == 'class':
        expecting_class_name = True

    return t

# --- INICIO 1 definiciones de tokens de Andres Layedra ---

def t_FLOAT_LITERAL(t):
    r'\d+\.\d+f'
    t.value = float(t.value[:-1])  # Quita la 'f'
    return t

def t_DECIMAL_LITERAL(t):
    r'\d+\.\d+([mM])'
    t.value = float(t.value[:-1])
    return t


def t_DATE_LITERAL(t):
    r'"\d{4}-\d{2}-\d{2}"'
    t.value = t.value.strip('"')
    return t

def t_HEX_LITERAL(t):
    r'0[xX][0-9A-Fa-f]+'
    t.value = int(t.value, 16)
    return t

def t_BIN_LITERAL(t):
    r'0[bB][01]+'
    t.value = int(t.value, 2)
    return t


# --- FIN 1 definiciones de tokens de Andres Layedra ---

def t_NUMERO(t):
    r'\d+(\.\d+)?([eE][+-]?\d+)?'
    t.value = float(t.value) if '.' in t.value or 'e' in t.value.lower() else int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t



def t_CHAR_LITERAL(t):
    r"\'(\\.|[^\\'])\'"
    t.value = t.value[1:-1]  # elimina las comillas
    return t

# --- INICIO 2 definiciones de tokens de Andres Layedra ---

def t_TRUE_LITERAL(t):
    r'\btrue\b'
    t.type = 'TRUE_LITERAL'
    t.value = True
    return t

def t_FALSE_LITERAL(t):
    r'\bfalse\b'
    t.type = 'FALSE_LITERAL'
    t.value = False
    return t

def t_XML_COMMENT(t):
    r'\/\/\/[^\n]*'
    return t



# --- FIN 2 definiciones de tokens de Andres Layedra ---

t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comment(t):
    r'//.*'
    pass  # Ignora comentarios

def t_multiline_comment(t):
    r'/\*[\s\S]*?\*/'
    pass  # Ignora comentarios multilínea

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()



nombre_archivo = f"algoritmo-{usuario_git}.cs"

try:
    with open(nombre_archivo, "r", encoding="utf-8") as file:
        data = file.read()
except FileNotFoundError:
    print(f" El archivo '{nombre_archivo}' no fue encontrado.")
    exit()


# Analizar y guardar logs
logs = []

# Prueba del lexer
lexer.input(data)

for tok in lexer:
    logs.append(f"{tok.type:15} -> {tok.value}")

# Guardar log
now = datetime.datetime.now()
fecha_hora = now.strftime("%d-%m-%Y-%Hh%M")
log_filename = f"lexico-{usuario_git}-{fecha_hora}.txt"

log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)

with open(os.path.join(log_folder, log_filename), "w", encoding="utf-8") as f:
    f.write("\n".join(logs))

print(f" Análisis completado. Log guardado en '{os.path.join(log_folder, log_filename)}'")
