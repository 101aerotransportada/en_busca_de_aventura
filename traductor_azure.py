#!/usr/bin/env python3
import argparse
import os
import sys

import requests

# Número máximo de caracteres por encima del cual se envía la petición de traducción.
LONGITUD_MAXIMA = 5000


def traduce_texto(texto):
    """ Envía una petición a Azure con el texto en cuestión. """

    # If you encounter any issues with the base_url or path, make sure
    # that you are using the latest endpoint:
    # https://docs.microsoft.com/azure/cognitive-services/translator/reference/v3-0-translate
    path = "/translate"
    constructed_url = endpoint + path

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-type": "application/json",
        # "X-ClientTraceId": str(uuid.uuid4())
    }

    # You can pass more than one object in body, but we'll do just one.
    body = [{"text": texto}]
    params = {
        "api-version": "3.0",
        "from": "en",
        "to": "es",
    }

    # Llamada a Cognitive Services para la traducción.
    request = requests.post(constructed_url, params=params, headers=headers, json=body)

    traduccion = request.json()[0]["translations"][0]["text"]
    print(
        f"Traducción recibida: {len(texto)} bytes enviados, {len(traduccion)} bytes recibidos.",
        file=sys.stderr,
    )

    if args.verbose > 0:
        # Muestra el texto original y el traducido.
        print(f"Texto original:\n{texto}\n")
        print(f"Texto traducido:\n{traduccion}")

    if args.destino:
        fichero_destino = open(args.destino, "a")
    else:
        fichero_destino = open(sys.stdout)

    try:
        fichero_destino.write(traduccion)
        fichero_destino.close()

    except (OSError, IOError):
        print(f"Error al acceder al fichero {args.destino}")
        sys.exit(1)


parser = argparse.ArgumentParser()
parser.add_argument(
    "-o",
    "--origen",
    help="Ruta del fichero que contiene el texto original. Si se omite, se utilizará "
    "la entrada estándar (stdin).",
)
parser.add_argument(
    "-d",
    "--destino",
    help="Ruta del fichero donde escribir el texto traducido. Si se omite, se utilizará "
    "la salida estándar (stdout). Si el fichero existe, se añadirá el texto al final.",
)
parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="Imprime el texto original y el traducido por pantalla, de forma adicional.",
)
args = parser.parse_args()

key_var_name = "TRANSLATOR_TEXT_SUBSCRIPTION_KEY"
if not key_var_name in os.environ:
    raise Exception(
        "Please set/export the environment variable: {}".format(key_var_name)
    )
subscription_key = os.environ[key_var_name]

endpoint_var_name = "TRANSLATOR_TEXT_ENDPOINT"
if not endpoint_var_name in os.environ:
    raise Exception(
        "Please set/export the environment variable: {}".format(endpoint_var_name)
    )
endpoint = os.environ[endpoint_var_name]

if args.origen:
    fichero_origen = open(args.origen, "r")
else:
    fichero_origen = open(sys.stdin)

try:
    texto = ""
    while True:
        linea = fichero_origen.readline()
        texto += linea

        if len(texto) > LONGITUD_MAXIMA:
            traduce_texto(texto)
            texto = ""

        if linea == "":
            traduce_texto(texto)
            break

except (OSError, IOError):
    print(f"Error al acceder al fichero {args.origen}")
    sys.exit(1)

fichero_origen.close()
