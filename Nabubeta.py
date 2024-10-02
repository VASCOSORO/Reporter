import streamlit as st
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import pandas as pd

# Cargar variables de entorno
load_dotenv()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

# URLs del sitio
LOGIN_URL = "https://leadsales.services/login"
ANALYTICS_URL = "https://leadsales.services/workspace/analytics"

def login(session, email, password):
    """
    Función para iniciar sesión en el sitio web.
    """
    # Obtener la página de login para obtener cualquier token necesario (como CSRF)
    response = session.get(LOGIN_URL)
    if response.status_code != 200:
        st.error("No se pudo acceder a la página de login.")
        return False

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraer tokens o campos necesarios si es aplicable
    # Por ejemplo:
    # csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

    payload = {
        'email': email,
        'password': password,
        # 'csrf_token': csrf_token  # Incluir si es necesario
    }

    # Enviar solicitud POST para iniciar sesión
    post_response = session.post(LOGIN_URL, data=payload)

    # Verificar si el login fue exitoso
    if post_response.url != LOGIN_URL:
        return True
    else:
        return False

def obtener_datos_analytics(session):
    """
    Función para obtener datos de la página de analytics.
    """
    response = session.get(ANALYTICS_URL)
    if response.status_code != 200:
        st.error("No se pudo acceder a la página de analytics.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Aquí debes adaptar el código para extraer los datos específicos que necesitas.
    # Esto dependerá de la estructura HTML de la página de analytics.

    # Ejemplo: Supongamos que hay una tabla con id 'tabla-analytics'
    tabla = soup.find('table', {'id': 'tabla-analytics'})
    if not tabla:
        st.error("No se encontró la tabla de analytics.")
        return None

    # Extraer encabezados
    headers = [th.text.strip() for th in tabla.find('thead').find_all('th')]

    # Extraer filas
    filas = []
    for tr in tabla.find('tbody').find_all('tr'):
        celdas = [td.text.strip() for td in tr.find_all('td')]
        filas.append(celdas)

    # Crear DataFrame de pandas
    df = pd.DataFrame(filas, columns=headers)
    return df

def main():
    st.title("Automatización de Reportes - Analytics")

    if st.button("Iniciar Sesión y Obtener Datos de Analytics"):
        with requests.Session() as session:
            if login(session, EMAIL, PASSWORD):
                st.success("Inicio de sesión exitoso.")
                datos = obtener_datos_analytics(session)
                if datos is not None:
                    st.dataframe(datos)
                    # Opcional: Permitir descargar los datos como CSV
                    csv = datos.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Descargar CSV",
                        data=csv,
                        file_name='datos_analytics.csv',
                        mime='text/csv',
                    )
            else:
                st.error("Error al iniciar sesión. Verifica tus credenciales.")

if __name__ == "__main__":
    main()
