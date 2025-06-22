import ply.lex as lex
import datetime
import os

# SELECCIÓN DEL INTEGRANTE
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
    'abstract': 'ABSTRACT',
    'as': 'AS',
    'base': 'BASE',
    'bool': 'BOOL',
    'break': 'BREAK',
    'byte': 'BYTE',
    'case': 'CASE',
    'catch': 'CATCH',
    'char': 'CHAR',
    'checked': 'CHECKED',
    'class': 'CLASS',
    'const': 'CONST',
    'continue': 'CONTINUE',
    'decimal': 'DECIMAL',
    'default': 'DEFAULT',
    'delegate': 'DELEGATE',
    'do': 'DO',
    'double': 'DOUBLE',
    'else': 'ELSE',
    'enum': 'ENUM',
    'event': 'EVENT',
    'explicit': 'EXPLICIT',
    'extern': 'EXTERN',
    'false': 'FALSE',
    'finally': 'FINALLY',
    'fixed': 'FIXED',
    'float': 'FLOAT',
    'for': 'FOR',
    'foreach': 'FOREACH',
    'goto': 'GOTO',
    'if': 'IF',
    'implicit': 'IMPLICIT',
    'in': 'IN',
    'int': 'INT',
    'interface': 'INTERFACE',
    'internal': 'INTERNAL',
    'is': 'IS',
    'lock': 'LOCK',
    'long': 'LONG',
    'namespace': 'NAMESPACE',
    'new': 'NEW',
    'null': 'NULL',
    'object': 'OBJECT',
    'operator': 'OPERATOR',
    'out': 'OUT',
    'override': 'OVERRIDE',
    'params': 'PARAMS',
    'private': 'PRIVATE',
    'protected': 'PROTECTED',
    'public': 'PUBLIC',
    'readonly': 'READONLY',
    'ref': 'REF',
    'return': 'RETURN',
    'sbyte': 'SBYTE',
    'sealed': 'SEALED',
    'short': 'SHORT',
    'sizeof': 'SIZEOF',
    'stackalloc': 'STACKALLOC',
    'static': 'STATIC',
    'string': 'STRING',
    'struct': 'STRUCT',
    'switch': 'SWITCH',
    'this': 'THIS',
    'throw': 'THROW',
    'true': 'TRUE',
    'try': 'TRY',
    'typeof': 'TYPEOF',
    'uint': 'UINT',
    'ulong': 'ULONG',
    'unchecked': 'UNCHECKED',
    'unsafe': 'UNSAFE',
    'ushort': 'USHORT',
    'using': 'USING',
    'virtual': 'VIRTUAL',
    'void': 'VOID',
    'volatile': 'VOLATILE',
    'while': 'WHILE'
}

# Lista de tokens

tokens = [
    'ID',
    'NUMBER',
    'CLASS_NAME',
    'STRING_LITERAL',
    'CHAR_LITERAL',

    # Operadores
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'MOD', 'INCREMENT', 'DECREMENT',
    'ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN',
    'TIMES_ASSIGN', 'DIVIDE_ASSIGN', 'MOD_ASSIGN',
    'EQUALS', 'NOTEQUAL', 'GT', 'LT', 'GE', 'LE',
    'AND', 'OR', 'NOT', 'BITAND', 'BITOR', 'BITXOR', 'BITNOT',
    'LSHIFT', 'RSHIFT',

    # Delimitadores
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'COMMA', 'DOT', 'SEMICOLON', 'COLON', 'QUESTION', 'ARROW',

    # --- INICIO tokens adicionales de Andres Layedra ---
    'FLOAT_LITERAL',     # Ej: 36.6f
    'TRUE_LITERAL',      # true como literal
    'FALSE_LITERAL',     # false como literal
    'XML_COMMENT',       # Comentarios de documentación ///
    'DATE_LITERAL',      # Ej: "2025-06-14"
    'HEX_NUMBER',        # Ej: 0x1F4
    'BIN_NUMBER',        # Ej: 0b1010
    # --- FIN tokens adicionales de Andres Layedra ---



] + list(reserved.values())

# Expresiones regulares para tokens simples

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'

t_ASSIGN = r'='
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_TIMES_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = r'/='
t_MOD_ASSIGN = r'%='

# --- INICIO tokens de Mario Alvarado ---
t_EQUALS = r'=='
t_NOTEQUAL = r'!='
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='

t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
# --- FIN tokens de Mario Alvarado ---

t_BITAND = r'&'
t_BITOR = r'\|'
t_BITXOR = r'\^'
t_BITNOT = r'~'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_COMMA = r','
t_DOT = r'\.'
t_SEMICOLON = r';'
t_COLON = r':'
t_QUESTION = r'\?'
t_ARROW = r'=>'


# Reglas con acciones
expecting_class_name = False
clases_declaradas = set()

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    global expecting_class_name

    if expecting_class_name:
        t.type = 'CLASS_NAME'
        clases_declaradas.add(t.value) # Añadir a conjunto de clases declaradas
        expecting_class_name = False
    else:
        t.type = reserved.get(t.value, 'ID')

    if t.value == 'class':
        expecting_class_name = True

    return t

# --- INICIO 1 definiciones de tokens de Andres Layedra ---

def t_FLOAT_LITERAL(t):
    r'\d+\.\d+f'
    t.value = float(t.value[:-1])  # Quita la 'f'
    return t

def t_DATE_LITERAL(t):
    r'"\d{4}-\d{2}-\d{2}"'
    t.value = t.value.strip('"')
    return t

def t_HEX_NUMBER(t):
    r'0x[0-9A-Fa-f]+'
    t.value = int(t.value, 16)
    return t

def t_BIN_NUMBER(t):
    r'0b[01]+'
    t.value = int(t.value, 2)
    return t


# --- FIN 1 definiciones de tokens de Andres Layedra ---

def t_NUMBER(t):
    r'\d+(\.\d+)?([eE][+-]?\d+)?'
    t.value = float(t.value) if '.' in t.value or 'e' in t.value.lower() else int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]  # Remover comillas
    return t

def t_CHAR_LITERAL(t):
    r"'([^'\\]|\\.)'"
    t.value = t.value[1:-1]
    return t



# --- INICIO 2 definiciones de tokens de Andres Layedra ---

def t_TRUE_LITERAL(t):
    r'\btrue\b'
    t.type = reserved.get(t.value, 'TRUE_LITERAL')
    t.value = True
    return t

def t_FALSE_LITERAL(t):
    r'\bfalse\b'
    t.type = reserved.get(t.value, 'FALSE_LITERAL')
    t.value = False
    return t

def t_XML_COMMENT(t):
    r'///[^\n]*'
    t.type = 'XML_COMMENT'
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
