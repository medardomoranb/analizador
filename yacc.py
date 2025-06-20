import ply.yacc as yacc
import datetime
import os

# Importar los tokens desde el lexer
from lex import tokens

# -------------------------------
# Variables para logs y errores
# -------------------------------
errores = []

# -------------------------------
# Reglas sintácticas principales
# -------------------------------

# Programa principal
def p_program(p):
    '''program : using_list clase_list'''
    pass

def p_using_list(p):
    '''using_list : using
                  | using_list using
                  | empty'''
    pass

def p_using(p):
    'using : USING ID SEMICOLON'
    pass

def p_clase_list(p):
    '''clase_list : clase
                  | clase_list clase'''
    pass

def p_modificador(p):
    '''modificador : PUBLIC
                   | PRIVATE
                   | PROTECTED
                   | empty'''
    pass

def p_clase(p):
    'clase : modificador CLASS CLASS_NAME LBRACE cuerpo_clase RBRACE'
    pass

def p_cuerpo_clase(p):
    '''cuerpo_clase : propiedad
                    | metodo
                    | cuerpo_clase propiedad
                    | cuerpo_clase metodo'''
    pass

def p_propiedad(p):
    'propiedad : tipo ID ASSIGN expresion SEMICOLON'
    pass

def p_metodo(p):
    'metodo : tipo ID LPAREN parametros RPAREN LBRACE instrucciones RBRACE'
    pass

def p_parametros(p):
    '''parametros : tipo ID
                  | parametros COMMA tipo ID
                  | empty'''
    pass

# -------------------------------
# Instrucciones dentro de métodos
# -------------------------------
def p_instrucciones(p):
    '''instrucciones : instruccion
                     | instrucciones instruccion'''
    pass

def p_instruccion(p):
    '''instruccion : impresion
                   | lectura
                   | asignacion
                   | control
                   | instruccion_return'''
    pass

def p_imprimir(p):
    'impresion : ID DOT ID LPAREN STRING_LITERAL RPAREN SEMICOLON'
    pass

def p_lectura(p):
    'lectura : ID DOT ID LPAREN RPAREN SEMICOLON'
    pass

def p_asignacion(p):
    '''asignacion : tipo ID ASSIGN expresion SEMICOLON'''
    pass

def p_asignacion_objeto(p):
    'asignacion : tipo ID ASSIGN NEW ID LPAREN RPAREN SEMICOLON'
    pass

def p_instruccion_return(p):
    '''instruccion_return : RETURN expresion SEMICOLON'''
    pass

# -------------------------------
# Expresiones y condiciones
# -------------------------------
def p_expresion_aritmetica(p):
    '''expresion : expresion PLUS expresion
                 | expresion MINUS expresion
                 | expresion TIMES expresion
                 | expresion DIVIDE expresion
                 | NUMBER
                 | ID
                 | STRING_LITERAL
                 | TRUE
                 | FALSE'''
    pass

def p_condicion_logica(p):
    '''condicion : expresion GT expresion
                 | expresion LT expresion
                 | expresion GE expresion
                 | expresion LE expresion
                 | expresion EQUALS expresion
                 | expresion NOTEQUAL expresion
                 | condicion AND condicion
                 | condicion OR condicion'''
    pass

def p_control_if(p):
    '''control : IF LPAREN condicion RPAREN LBRACE instrucciones RBRACE
               | IF LPAREN condicion RPAREN LBRACE instrucciones RBRACE ELSE LBRACE instrucciones RBRACE'''
    pass

# -------------------------------
# Tipos de datos
# -------------------------------
def p_tipo(p):
    '''tipo : INT
            | FLOAT
            | STRING
            | CHAR
            | BOOL
            | ID'''
    pass

def p_empty(p):
    'empty :'
    pass

# -------------------------------
# Manejo de errores sintácticos
# -------------------------------
def p_error(p):
    if p:
        errores.append(f"Error sintáctico en línea {p.lineno}: Token inesperado '{p.value}'")
    else:
        errores.append("Error sintáctico: Fin de archivo inesperado.")

# -------------------------------
# Construcción del parser
# -------------------------------
parser = yacc.yacc()

# -------------------------------
# Selección de usuario
# -------------------------------
print("¿Quién está probando el parser?")
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
    print("Opción inválida.")
    exit()

# -------------------------------
# Leer archivo personalizado
# -------------------------------
archivo_codigo = f"algoritmo-{usuario_git}.cs"

try:
    with open(archivo_codigo, "r", encoding="utf-8") as f:
        data = f.read()
except FileNotFoundError:
    print(f" El archivo '{archivo_codigo}' no fue encontrado.")
    exit()

# -------------------------------
# Ejecutar el parser
# -------------------------------
parser.parse(data)

# -------------------------------
# Crear log de errores sintácticos
# -------------------------------
now = datetime.datetime.now()
fecha_hora = now.strftime("%d%m%Y-%Hh%M")
log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)
log_file = f"sintactico-{usuario_git}-{fecha_hora}.txt"
log_path = os.path.join(log_folder, log_file)

with open(log_path, "w", encoding="utf-8") as f:
    if errores:
        f.write("\n".join(errores))
    else:
        f.write("Análisis sintáctico sin errores.")

print(f" Análisis completado. Log guardado en '{log_path}'")
