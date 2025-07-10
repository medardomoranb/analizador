# analizador.py
from lex import lexer, tokens
from yacc import parser, errores as errores_sintacticos
import datetime
import os
import ply.lex as lex
import ply.yacc as yacc

def analisis_lexico(codigo):
    lexer.input(codigo)
    resultado = []
    for tok in lexer:
        resultado.append(f"{tok.type:15} -> {tok.value}")
    return "\n".join(resultado)

def analisis_sintactico(codigo):
    errores_sintacticos.clear()
    parser.parse(codigo)
    if errores_sintacticos:
        return "\n".join(errores_sintacticos)
    return "Análisis sintáctico sin errores."

def analisis_semantico(codigo):
    lexer.input(codigo)
    tokens_extraidos = list(lexer)

    variables_declaradas = set()
    errores_semanticos = []

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

    if errores_semanticos:
        return "\n".join(errores_semanticos)
    return "Análisis semántico sin errores."
