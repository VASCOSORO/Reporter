import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Credenciales
EMAIL = "SomosMundo"
PASSWORD = "74108520!Ii"

# URL del sitio
LOGIN_URL = "https://auth.easybuild.website/login?destroyedSession=true&host=app.easybuild.website"

def login_selenium(email, password):
    """
    Función para iniciar sesión utilizando Selenium.
    """
    try:
        logging.info("Configurando opciones de Chrome.")
        # Configurar el driver de Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Ejecutar en modo headless (sin interfaz)
        options.add_argument('--no-sandbox')  # Evitar problemas de permisos
        options.add_argument('--disable-dev-shm-usage')  # Evitar problemas de memoria compartida
        options.add_argument('--disable-gpu')  # Desactivar uso de GPU
        options.add_argument('--window-size=1920,1080')  # Definir tamaño de ventana

        logging.info("Instalando chromedriver.")
        # Instalar y configurar el driver
        driver_path = ChromeDriverManager().install()
        os.chmod(driver_path, 0o755)  # Asegurar permisos de ejecución

        logging.info("Iniciando el navegador.")
        driver = webdriver.Chrome(service=ChromeService(driver_path), options=options)
        driver.get(LOGIN_URL)

        logging.info("Esperando a que la página cargue.")
        # Esperar a que la página cargue
        time.sleep(10)  # Considera usar WebDriverWait para una espera más robusta

        logging.info("Localizando campos de usuario y contraseña.")
        # Encontrar y rellenar los campos de usuario y contraseña
        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')

        username_field.send_keys(email)
        password_field.send_keys(password)

        logging.info("Enviando formulario de inicio de sesión.")
        # Enviar el formulario
        password_field.send_keys(Keys.RETURN)

        logging.info("Esperando a que se procese el inicio de sesión.")
        # Esperar a que se procese el inicio de sesión
        time.sleep(10)  # Considera usar WebDriverWait para una espera más robusta

        logging.info("Verificando si el inicio de sesión fue exitoso.")
        # Verificar si el inicio de sesión fue exitoso
        if driver.current_url != LOGIN_URL:
            logging.info("Inicio de sesión exitoso.")
            return driver
        else:
            logging.error("Error al iniciar sesión. Verifica tus credenciales.")
            st.error("Error al iniciar sesión. Verifica tus credenciales.")
            driver.quit()
            return None
    except Exception as e:
        logging.error(f"Error durante el inicio de sesión con Selenium: {e}")
        st.error(f"Error durante el inicio de sesión con Selenium: {e}")
        return None

def main():
    st.set_page_config(page_title="Automatización de Reportes - EasyBuild", layout="wide")
    st.title("Automatización de Reportes - EasyBuild")

    st.write("""
    Este aplicativo permite iniciar sesión en [EasyBuild](https://auth.easybuild.website/login) utilizando Selenium.
    """)

    if st.button("Iniciar Sesión en EasyBuild"):
        driver = login_selenium(EMAIL, PASSWORD)
        if driver:
            st.success("Inicio de sesión exitoso.")
            # Aquí puedes continuar con la automatización para obtener datos del sitio
            # Por ejemplo, navegar a una página específica, extraer información, etc.
            # Al finalizar, cierra el navegador
            driver.quit()

if __name__ == "__main__":
    main()
