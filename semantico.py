import os
import datetime
from lex import lexer
from yacc import parser  # Usa el parser sin modificar yacc.py
from yacc import errores as errores_sintacticos  # para evitar repetir errores

# -------------------------------
# Selección de usuario
# -------------------------------
print("¿Quién está probando el análisis semántico?")
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
# Leer archivo fuente
# -------------------------------
archivo_codigo = f"algoritmo-{usuario_git}.cs"

try:
    with open(archivo_codigo, "r", encoding="utf-8") as f:
        data = f.read()
except FileNotFoundError:
    print(f"El archivo '{archivo_codigo}' no fue encontrado.")
    exit()

# -------------------------------
# Análisis semántico personalizado
# -------------------------------

# Variables semánticas
variables_declaradas = set()
errores_semanticos = []

# Ejecutar lexer y guardar identificadores y asignaciones
lexer.input(data)
tokens_extraidos = list(lexer)

for i, token in enumerate(tokens_extraidos):
    if token.type == "ID":
        prev = tokens_extraidos[i - 1] if i > 0 else None
        next_ = tokens_extraidos[i + 1] if i < len(tokens_extraidos) - 1 else None

        if prev and prev.type in {"INT", "FLOAT", "STRING", "CHAR", "BOOL"}:
            if token.value in variables_declaradas:
                errores_semanticos.append(
                    f"Línea {token.lineno}: Variable '{token.value}' ya fue declarada."
                )
            else:
                variables_declaradas.add(token.value)
        elif next_ and next_.type == "ASSIGN":
            if token.value not in variables_declaradas:
                errores_semanticos.append(
                    f"Línea {token.lineno}: Variable '{token.value}' usada sin ser declarada."
                )

# -------------------------------
# Guardar log semántico
# -------------------------------
now = datetime.datetime.now()
fecha_hora = now.strftime("%d%m%Y-%Hh%M")
log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)
log_file = f"semantico-{usuario_git}-{fecha_hora}.txt"
log_path = os.path.join(log_folder, log_file)

with open(log_path, "w", encoding="utf-8") as f:
    if errores_semanticos:
        f.write("Errores semánticos encontrados:\n")
        f.write("\n".join(errores_semanticos))
    else:
        f.write("Análisis semántico sin errores.")

print(f" Análisis semántico completado. Log guardado en '{log_path}'")