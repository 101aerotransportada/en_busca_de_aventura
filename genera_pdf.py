#!/usr/bin/env python3
""" Programa para generar el PDF final mediante marko y Weasyprint a partir de un texto en Markdown.
Necesita ambos módulos instalados con pip u otra forma. """

import argparse
import os
import time

import marko
import weasyprint

PLANTILLA = "plantilla.html"
SALIDA = f"En busca de aventura - {time.strftime('%Y%m%d')}"
print(SALIDA)

parser = argparse.ArgumentParser(description="Generación del PDF a partir de Markdown.")
parser.add_argument(
    "-p",
    "--plantilla",
    help="Plantilla donde empotrar el HTML intermedio. Ha de contener la cadena '%%TEXTO%%'.",
    default=PLANTILLA,
)
parser.add_argument(
    "-d",
    "--dir",
    help="Directorio donde encontrar los ficheros en Markdown. Se leerán en orden alfabético.",
    default="español",
)
parser.add_argument(
    "-s",
    "--salida",
    help=f"Nombre del fichero HTML intermedio y el PDF final. Por omisión es '{SALIDA}'.",
    default=SALIDA,
)
args = parser.parse_args()

ficheros = os.listdir(args.dir)
# Los ordenamos por índice numérico. Tienen que tener la forma "numero_titulo_largo.txt".
ficheros.sort(key=lambda x: int(x.split("_")[0]))
print(f"Encontrados {len(ficheros)} ficheros:")
print("\n".join(ficheros))

html_salida = f"{SALIDA}.html"
pdf_salida = f"{SALIDA}.pdf"
print(f"Generando {html_salida}.")
t0 = time.time()
with open(PLANTILLA, "r") as f:
    html_intermedio = f.read()

texto = ""
for i in ficheros:
    with open(os.path.join(args.dir, i), "r") as f:
        texto += marko.convert(f.read())

with open(html_salida, "w") as f:
    f.write(html_intermedio.replace("%TEXTO%", texto))

print(f"{html_salida} generado en {time.time()-t0:.1f} segundos.")

print(f"Generando {pdf_salida}.")
weasyprint.HTML(filename=html_salida).write_pdf(pdf_salida)
print(f"{pdf_salida} generado en {time.time()-t0:.1f} segundos.")
