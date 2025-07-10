import os
import datetime
import sys
from lex import lexer  # importas lexer de lex.py
from yacc import errores as errores_sintacticos

# -------------------------------
# Análisis semántico personalizado
# -------------------------------

# Variables semánticas
variables_declaradas = set()
errores_semanticos = []

# Ejecutar lexer y guardar identificadores y asignaciones
tokens_extraidos = list(lexer)

for i, token in enumerate(tokens_extraidos):
    if token.type == "IDENTIFICADOR":
        prev = tokens_extraidos[i - 1] if i > 0 else None
        next_ = tokens_extraidos[i + 1] if i < len(tokens_extraidos) - 1 else None

        if prev and prev.type in {"INT", "FLOAT", "STRING", "CHAR", "BOOL"}:
            if token.value in variables_declaradas:
                errores_semanticos.append(
                    f"[ERROR SEMÁNTICO] Línea {token.lineno}: Variable '{token.value}' ya fue declarada."
                )
            else:
                variables_declaradas.add(token.value)
        elif next_ and next_.type == "ASIGNACION":
            if token.value not in variables_declaradas:
                errores_semanticos.append(
                    f"[ERROR SEMÁNTICO] Línea {token.lineno}: Variable '{token.value}' usada sin ser declarada."
                )