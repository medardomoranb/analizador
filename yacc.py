import ply.yacc as yacc
import datetime
import os
import sys
from lex import tokens  

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
    '''program : using_list elementos_programa
               | using_list XML_COMMENT elementos_programa'''
    pass


def p_elementos_programa(p):
    '''elementos_programa : clase
                          | enum_decl
                          | struct_decl
                          | elementos_programa clase
                          | elementos_programa enum_decl
                          | elementos_programa struct_decl
                          | elementos_programa XML_COMMENT'''
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
    '''modificador : lista_modificadores
                   | empty'''
    pass

def p_lista_modificadores(p):
    '''lista_modificadores : modificador_simple
                           | lista_modificadores modificador_simple'''
    pass

def p_modificador_simple(p):
    '''modificador_simple : PUBLIC
                          | PRIVATE
                          | PROTECTED
                          | STATIC'''
    pass


def p_clase(p):
    '''clase : modificador CLASS CLASS_NAME LBRACE cuerpo_clase RBRACE
             | XML_COMMENT modificador CLASS CLASS_NAME LBRACE cuerpo_clase RBRACE'''
    pass



def p_cuerpo_clase(p):
    '''cuerpo_clase : propiedad
                    | metodo
                    | enum_decl
                    | struct_decl
                    | clase
                    | cuerpo_clase propiedad
                    | cuerpo_clase metodo
                    | cuerpo_clase enum_decl
                    | cuerpo_clase struct_decl
                    | cuerpo_clase clase
                    | cuerpo_clase XML_COMMENT
                    | XML_COMMENT'''
    pass


def p_propiedad(p):
    '''propiedad : modificador tipo ID ASSIGN expresion SEMICOLON
                 | modificador tipo ID SEMICOLON
                 | tipo ID ASSIGN expresion SEMICOLON
                 | tipo ID SEMICOLON
                 | XML_COMMENT tipo ID ASSIGN expresion SEMICOLON
                 | XML_COMMENT tipo ID SEMICOLON'''
    pass

def p_metodo_main(p):
    '''metodo : modificador tipo_main ID LPAREN parametros_main RPAREN LBRACE instrucciones RBRACE'''
    pass

def p_tipo_main(p):
    '''tipo_main : VOID'''
    pass

def p_parametros_main(p):
    '''parametros_main : tipo LBRACKET RBRACKET ID'''

def p_metodo(p):
    '''metodo : modificador tipo ID LPAREN parametros RPAREN LBRACE instrucciones RBRACE
              | modificador tipo ID LPAREN tipo LBRACKET RBRACKET ID RPAREN LBRACE instrucciones RBRACE
              | XML_COMMENT modificador tipo ID LPAREN parametros RPAREN LBRACE instrucciones RBRACE
              | XML_COMMENT modificador tipo ID LPAREN tipo LBRACKET RBRACKET ID RPAREN LBRACE instrucciones RBRACE'''
    pass

def p_parametros(p):
    '''parametros : parametro
                  | parametros COMMA parametro
                  | XML_COMMENT parametros
                  | empty'''
    print("DEBUG parámetros:", [str(t) for t in p.slice])  # <-- Añade esto
    pass


def p_parametro(p):
    '''parametro : tipo ID
                 | tipo LBRACKET RBRACKET ID
                 | tipo ID ASSIGN expresion
                 | tipo LBRACKET RBRACKET ID ASSIGN expresion
                 | XML_COMMENT tipo ID
                 | XML_COMMENT tipo ID ASSIGN expresion'''
    pass


# -------------------------------
# Instrucciones dentro de métodos
# -------------------------------
def p_instrucciones(p):
    '''instrucciones : instruccion
                     | instrucciones instruccion
                     | empty'''
    pass

def p_instruccion(p):
    '''instruccion : impresion  
                   | llamada
                   | lectura
                   | asignacion
                   | control
                   | instruccion_return
                   | XML_COMMENT
                   | propiedad'''
    pass

def p_imprimir(p):
    '''impresion : ID DOT ID LPAREN expresion RPAREN SEMICOLON
                 | ID DOT ID LPAREN lista_expresiones RPAREN SEMICOLON'''
    pass    

def p_lista_expresiones(p):
    '''lista_expresiones : expresion
                         | lista_expresiones COMMA expresion'''
    pass



def p_lectura(p):
    'lectura : ID DOT ID LPAREN RPAREN SEMICOLON'
    pass

def p_asignacion(p):
    '''asignacion : tipo ID ASSIGN expresion SEMICOLON
                  | tipo ID ASSIGN NEW ID LPAREN RPAREN SEMICOLON'''
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
                 | DATE_LITERAL
                 | DECIMAL_LITERAL
                 | HEX_LITERAL
                 | BIN_LITERAL
                 | NUMBER
                 | FLOAT_LITERAL
                 | ID
                 | STRING_LITERAL
                 | TRUE_LITERAL
                 | FALSE_LITERAL
                 | CHAR_LITERAL'''
    pass
#---Expresiones adicionales de Andrés Layedra---
def p_expresion_incremento(p):
    '''expresion : ID INCREMENT
                 | ID DECREMENT'''
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

# ========================
# Reglas aportadas por Mario Alvarado
# ========================

# === 1. ESTRUCTURA DE DATOS ===
# -------- Arreglo Simple ----------

def p_arreglo_asignacion(p):
    '''asignacion : tipo LBRACKET RBRACKET ID ASSIGN LBRACE lista_expresiones RBRACE SEMICOLON'''
    pass
# int [] notas = {10,9,8};

# === 2. ESTRUCTURA DE CONTROL ===
# -------- CICLO WHILE ----------

def p_control_while(p):
    '''control : WHILE LPAREN condicion RPAREN LBRACE instrucciones RBRACE'''
    pass

# === 3. TIPO DE FUNCION ===

def p_funcion_void_sin_parametros(p):
    '''metodo : modificador VOID ID LPAREN RPAREN LBRACE instrucciones RBRACE'''
    pass
# ejemplo: public void metodo() { ... }


# ========================
# Reglas aportadas por Andrés Layedra
# ========================

# === 1. ESTRUCTURA DE DATOS ===
# -------- enum ----------
def p_enum_decl(p):
    'enum_decl : modificador ENUM ID LBRACE lista_identificadores RBRACE'
    pass


def p_lista_identificadores(p):
    '''lista_identificadores : ID
                             | lista_identificadores COMMA ID'''
    pass

# -------- struct ----------
def p_struct_decl(p):
    'struct_decl : modificador STRUCT ID LBRACE cuerpo_clase RBRACE'
    pass

def p_llamada(p):
    '''llamada : ID DOT ID LPAREN lista_expresiones RPAREN SEMICOLON
               | ID DOT ID LPAREN RPAREN SEMICOLON'''
    pass


# === 2. ESTRUCTURA DE CONTROL ===
# -------- switch-case ----------
def p_switch(p):
    '''control : SWITCH LPAREN expresion RPAREN LBRACE lista_casos default_case RBRACE'''
    pass

def p_lista_casos(p):
    '''lista_casos : lista_casos caso
                   | caso'''
    pass

def p_caso(p):
    'caso : CASE expresion COLON instrucciones BREAK SEMICOLON'
    pass

def p_default_case(p):
    '''default_case : DEFAULT COLON instrucciones BREAK SEMICOLON
                    | empty'''
    pass

# -------- ciclo for ----------
def p_for(p):
    '''control : FOR LPAREN tipo ID ASSIGN expresion SEMICOLON condicion SEMICOLON expresion RPAREN LBRACE instrucciones RBRACE'''
    pass

# -------- continue ----------
def p_instruccion_continue(p):
    'instruccion : CONTINUE SEMICOLON'
    pass

# -------- break ----------
def p_instruccion_break(p):
    'instruccion : BREAK SEMICOLON'
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
            | VOID
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

if len(sys.argv) > 1:
    usuario_git = sys.argv[1]
else:
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
