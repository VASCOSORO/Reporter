import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

# URLs del sitio
LOGIN_URL = "https://leadsales.services/login"
ANALYTICS_URL = "https://leadsales.services/workspace/analytics"

def login_selenium(email, password):
    """
    Función para iniciar sesión utilizando Selenium.
    """
    try:
        # Configurar el driver de Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Ejecutar en modo headless (sin interfaz)
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(LOGIN_URL)

        # Esperar a que la página cargue
        time.sleep(3)

        # Encontrar y rellenar los campos de email y contraseña
        email_field = driver.find_element(By.NAME, 'email')
        password_field = driver.find_element(By.NAME, 'password')

        email_field.send_keys(email)
        password_field.send_keys(password)

        # Enviar el formulario
        password_field.send_keys(Keys.RETURN)

        # Esperar a que se procese el inicio de sesión
        time.sleep(5)

        # Verificar si el inicio de sesión fue exitoso
        if driver.current_url != LOGIN_URL:
            return driver
        else:
            st.error("Error al iniciar sesión. Verifica tus credenciales.")
            driver.quit()
            return None
    except Exception as e:
        st.error(f"Error durante el inicio de sesión con Selenium: {e}")
        return None

def obtener_datos_selenium(driver):
    """
    Función para obtener datos de la página de analytics utilizando Selenium.
    """
    try:
        driver.get(ANALYTICS_URL)
        time.sleep(5)  # Esperar a que la página cargue completamente

        # Extraer el contenido de la página
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Adaptar según la estructura HTML de la página de analytics
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
    except Exception as e:
        st.error(f"Error al obtener los datos de analytics con Selenium: {e}")
        return None
    finally:
        driver.quit()

def main():
    st.set_page_config(page_title="Automatización de Reportes - Analytics", layout="wide")
    st.title("Automatización de Reportes - Analytics")

    st.write("""
    Este aplicativo permite iniciar sesión en [LeadSales](https://leadsales.services/login) y extraer datos de la sección de Analytics utilizando Selenium.
    """)

    if st.button("Iniciar Sesión y Obtener Datos de Analytics"):
        driver = login_selenium(EMAIL, PASSWORD)
        if driver:
            st.success("Inicio de sesión exitoso.")
            datos = obtener_datos_selenium(driver)
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

if __name__ == "__main__":
    main()
