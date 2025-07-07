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
    'using : USING IDENTIFICADOR PUNTO_COMA'
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
    '''clase : modificador CLASS NOMBRE_CLASE LLAVE_IZQ cuerpo_clase LLAVE_DER
             | XML_COMMENT modificador CLASS NOMBRE_CLASE LLAVE_IZQ cuerpo_clase LLAVE_DER'''
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
    '''propiedad : modificador tipo IDENTIFICADOR ASIGNACION expresion PUNTO_COMA
                 | modificador tipo IDENTIFICADOR PUNTO_COMA
                 | tipo IDENTIFICADOR ASIGNACION expresion PUNTO_COMA
                 | tipo IDENTIFICADOR PUNTO_COMA
                 | XML_COMMENT tipo IDENTIFICADOR ASIGNACION expresion PUNTO_COMA
                 | XML_COMMENT tipo IDENTIFICADOR PUNTO_COMA'''
    pass

def p_metodo_main(p):
    '''metodo : modificador tipo_main IDENTIFICADOR PARENTESIS_IZQ parametros_main PARENTESIS_DER LLAVE_IZQ instrucciones LLAVE_DER'''
    pass

def p_tipo_main(p):
    '''tipo_main : VOID'''
    pass

def p_parametros_main(p):
    '''parametros_main : tipo CORCHETE_IZQ CORCHETE_DER IDENTIFICADOR'''

def p_metodo(p):
    '''metodo : modificador tipo IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER LLAVE_IZQ instrucciones LLAVE_DER
              | modificador tipo IDENTIFICADOR PARENTESIS_IZQ tipo CORCHETE_IZQ CORCHETE_DER IDENTIFICADOR PARENTESIS_DER LLAVE_IZQ instrucciones LLAVE_DER
              | XML_COMMENT modificador tipo IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER LLAVE_IZQ instrucciones LLAVE_DER
              | XML_COMMENT modificador tipo IDENTIFICADOR PARENTESIS_IZQ tipo CORCHETE_IZQ CORCHETE_DER IDENTIFICADOR PARENTESIS_DER LLAVE_IZQ instrucciones LLAVE_DER'''
    pass

def p_parametros(p):
    '''parametros : parametro
                  | parametros COMA parametro
                  | XML_COMMENT parametros
                  | empty'''
    print("DEBUG parámetros:", [str(t) for t in p.slice])  # <-- Añade esto
    pass


def p_parametro(p):
    '''parametro : tipo IDENTIFICADOR
                 | tipo CORCHETE_IZQ CORCHETE_DER IDENTIFICADOR
                 | tipo IDENTIFICADOR ASIGNACION expresion
                 | tipo CORCHETE_IZQ CORCHETE_DER IDENTIFICADOR ASIGNACION expresion
                 | XML_COMMENT tipo IDENTIFICADOR
                 | XML_COMMENT tipo IDENTIFICADOR ASIGNACION expresion'''
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
    '''impresion : IDENTIFICADOR PUNTO IDENTIFICADOR PARENTESIS_IZQ expresion PARENTESIS_DER PUNTO_COMA
                 | IDENTIFICADOR PUNTO IDENTIFICADOR PARENTESIS_IZQ lista_expresiones PARENTESIS_DER PUNTO_COMA'''
    pass    

def p_lista_expresiones(p):
    '''lista_expresiones : expresion
                         | lista_expresiones COMA expresion'''
    pass



def p_lectura(p):
    'lectura : IDENTIFICADOR PUNTO IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA'
    pass

def p_asignacion(p):
    '''asignacion : tipo IDENTIFICADOR ASIGNACION expresion PUNTO_COMA
                  | tipo IDENTIFICADOR ASIGNACION NEW IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA'''
    pass


def p_instruccion_return(p):
    '''instruccion_return : RETURN expresion PUNTO_COMA'''
    pass

# -------------------------------
# Expresiones y condiciones
# -------------------------------
def p_expresion_aritmetica(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion MULTIPLICACION expresion
                 | expresion DIVISION expresion
                 | DATE_LITERAL
                 | DECIMAL_LITERAL
                 | HEX_LITERAL
                 | BIN_LITERAL
                 | NUMERO
                 | FLOAT_LITERAL
                 | IDENTIFICADOR
                 | STRING_LITERAL
                 | TRUE_LITERAL
                 | FALSE_LITERAL
                 | CHAR_LITERAL'''
    pass
#---Expresiones adicionales de Andrés Layedra---
def p_expresion_incremento(p):
    '''expresion : IDENTIFICADOR INCREMENTO
                 | IDENTIFICADOR DECREMENTO'''
    pass


def p_condicion_logica(p):
    '''condicion : expresion MAYOR expresion
                 | expresion MENOR expresion
                 | expresion MAYOR_IGUAL expresion
                 | expresion MENOR_IGUAL expresion
                 | expresion IGUAL expresion
                 | expresion NO_IGUAL expresion
                 | condicion AND condicion
                 | condicion OR condicion'''
    pass

def p_control_if(p):
    '''control : IF PARENTESIS_IZQ condicion PARENTESIS_DER LLAVE_IZQ instrucciones LLAVE_DER
               | IF PARENTESIS_IZQ condicion PARENTESIS_DER LLAVE_IZQ instrucciones LLAVE_DER ELSE LLAVE_IZQ instrucciones LLAVE_DER'''
    pass

# ========================
# Reglas aportadas por Mario Alvarado
# ========================

# === 1. ESTRUCTURA DE DATOS ===
# -------- Arreglo Simple ----------

def p_arreglo_asignacion(p):
    '''asignacion : tipo CORCHETE_IZQ CORCHETE_DER IDENTIFICADOR ASIGNACION LLAVE_IZQ lista_expresiones LLAVE_DER PUNTO_COMA'''
    pass
# int [] notas = {10,9,8};

# === 2. ESTRUCTURA DE CONTROL ===
# -------- CICLO WHILE ----------

def p_control_while(p):
    '''control : WHILE PARENTESIS_IZQ condicion PARENTESIS_DER LLAVE_IZQ instrucciones LLAVE_DER'''
    pass

# === 3. TIPO DE FUNCION ===

def p_funcion_void_sin_parametros(p):
    '''metodo : modificador VOID IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER LLAVE_IZQ instrucciones LLAVE_DER'''
    pass
# ejemplo: public void metodo() { ... }


# ========================
# Reglas aportadas por Andrés Layedra
# ========================

# === 1. ESTRUCTURA DE DATOS ===
# -------- enum ----------
def p_enum_decl(p):
    'enum_decl : modificador ENUM IDENTIFICADOR LLAVE_IZQ lista_identificadores LLAVE_DER'
    pass


def p_lista_identificadores(p):
    '''lista_identificadores : IDENTIFICADOR
                             | lista_identificadores COMA IDENTIFICADOR'''
    pass

# -------- struct ----------
def p_struct_decl(p):
    'struct_decl : modificador STRUCT IDENTIFICADOR LLAVE_IZQ cuerpo_clase LLAVE_DER'
    pass

def p_llamada(p):
    '''llamada : IDENTIFICADOR PUNTO IDENTIFICADOR PARENTESIS_IZQ lista_expresiones PARENTESIS_DER PUNTO_COMA
               | IDENTIFICADOR PUNTO IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA'''
    pass


# === 2. ESTRUCTURA DE CONTROL ===
# -------- switch-case ----------
def p_switch(p):
    '''control : SWITCH PARENTESIS_IZQ expresion PARENTESIS_DER LLAVE_IZQ lista_casos default_case LLAVE_DER'''
    pass

def p_lista_casos(p):
    '''lista_casos : lista_casos caso
                   | caso'''
    pass

def p_caso(p):
    'caso : CASE expresion DOS_PUNTOS instrucciones BREAK PUNTO_COMA'
    pass

def p_default_case(p):
    '''default_case : DEFAULT DOS_PUNTOS instrucciones BREAK PUNTO_COMA
                    | empty'''
    pass

# -------- ciclo for ----------
def p_for(p):
    '''control : FOR PARENTESIS_IZQ tipo IDENTIFICADOR ASIGNACION expresion PUNTO_COMA condicion PUNTO_COMA expresion PARENTESIS_DER LLAVE_IZQ instrucciones LLAVE_DER'''
    pass

# -------- continue ----------
def p_instruccion_continue(p):
    'instruccion : CONTINUE PUNTO_COMA'
    pass

# -------- break ----------
def p_instruccion_break(p):
    'instruccion : BREAK PUNTO_COMA'
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
            | IDENTIFICADOR'''
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
