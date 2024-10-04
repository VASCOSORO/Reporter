import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Credenciales
EMAIL = "SomosMundo"
PASSWORD = "74108520!Ii"

# URL del sitio
LOGIN_URL = "https://auth.easybuild.website/login?destroyedSession=true&host=app.easybuild.website"

def login_selenium(email, password):
    """
    Función para iniciar sesión utilizando Selenium en modo headless.
    """
    try:
        # Configurar el driver de Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Ejecutar en modo headless (sin interfaz)
        options.add_argument('--no-sandbox')  # Añadir no-sandbox para evitar problemas de permisos
        options.add_argument('--disable-dev-shm-usage')  # Evitar problemas de memoria compartida
        options.add_argument('--remote-debugging-port=9222')  # Para ejecutar Chrome en algunos entornos

        # Descargar e iniciar el ChromeDriver usando webdriver_manager
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(LOGIN_URL)

        # Esperar a que la página cargue
        wait = WebDriverWait(driver, 10)

        # Encontrar y rellenar los campos de usuario y contraseña
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))

        username_field.send_keys(email)
        password_field.send_keys(password)

        # Enviar el formulario
        password_field.send_keys(Keys.RETURN)

        # Esperar a que se procese el inicio de sesión y verificar si fue exitoso
        time.sleep(5)
        if driver.current_url != LOGIN_URL:
            return driver
        else:
            st.error("Error al iniciar sesión. Verifica tus credenciales.")
            driver.quit()
            return None
    except Exception as e:
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
            # En este punto, podemos continuar con la automatización para obtener datos del sitio
            driver.quit()

if __name__ == "__main__":
    main()
