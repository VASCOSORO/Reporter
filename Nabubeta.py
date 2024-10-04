import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env (opcional)
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)

# URL del sitio de inicio de sesión
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
        # Usar WebDriverWait en lugar de time.sleep para una espera más robusta
        wait = WebDriverWait(driver, 20)
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))

        logging.info("Rellenando campos de usuario y contraseña.")
        # Rellenar los campos de usuario y contraseña
        username_field.send_keys(email)
        password_field.send_keys(password)

        logging.info("Enviando formulario de inicio de sesión.")
        # Enviar el formulario
        password_field.send_keys(Keys.RETURN)

        logging.info("Esperando a que se procese el inicio de sesión.")
        # Esperar a que la URL cambie indicando inicio de sesión exitoso
        wait.until(EC.url_changes(LOGIN_URL))

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

    st.header("Iniciar Sesión")

    # Crear campos de entrada para Email y Contraseña
    email = st.text_input("Email")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión en EasyBuild"):
        if not email or not password:
            st.error("Por favor, ingresa tanto el Email como la Contraseña.")
        else:
            driver = login_selenium(email, password)
            if driver:
                st.success("Inicio de sesión exitoso.")
                # Aquí puedes continuar con la automatización para obtener datos del sitio
                # Por ejemplo, navegar a una página específica, extraer información, etc.
                # Al finalizar, cierra el navegador
                driver.quit()

if __name__ == "__main__":
    main()
