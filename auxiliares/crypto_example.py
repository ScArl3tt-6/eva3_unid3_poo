"""Ejemplos de uso para `auxiliares.crypto`.

Uso:
  - Generar una clave y exportarla a `ENCRYPTION_KEY`:
      from auxiliares import crypto
      print(crypto.generate_key())

  - Ajustar la variable de entorno y ejecutar los ejemplos.
"""
import os
from auxiliares import crypto


def main():
    print("--- Crypto example ---")

    # Mostrar cómo generar una nueva clave
    print("Generar nueva clave (guardar en ENCRYPTION_KEY):")
    new_key = crypto.generate_key()
    print(new_key)

    # Para la demo, usar la nueva clave en memoria
    os.environ["ENCRYPTION_KEY"] = new_key

    secret = "mi texto secreto"
    token = crypto.encrypt_str(secret)
    print("Token:", token)

    recovered = crypto.decrypt_str(token)
    print("Recuperado:", recovered)


if __name__ == "__main__":
    main()
