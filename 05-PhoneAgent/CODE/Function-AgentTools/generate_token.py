#!/usr/bin/env python3
"""
Script para generar el token de autenticación para Google APIs.
Este script solicitará autorización para acceder a Google Calendar y Google Sheets.
"""

import os
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Ruta del directorio actual
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_PATH, "client_secret.json")
TOKEN_FILE = os.path.join(BASE_PATH, "token.json")

# Permisos requeridos
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
]

def main():
    """Genera un token de autenticación para Google APIs."""
    creds = None
    
    # Verificar si ya existe un token
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # Si no hay credenciales válidas, solicitar autorización
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"ERROR: No se encontró el archivo de credenciales '{CREDENTIALS_FILE}'")
                print("Por favor, descarga el archivo 'client_secret.json' desde la consola de desarrolladores de Google")
                print("y colócalo en el directorio actual.")
                return
            
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Guardar las credenciales para la próxima ejecución
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
        
        print(f"Token generado exitosamente y guardado en {TOKEN_FILE}")
        print("Ahora puedes ejecutar la aplicación principal.")
    else:
        print("El token ya existe y es válido.")

if __name__ == "__main__":
    main() 