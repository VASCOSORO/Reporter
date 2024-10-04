# =================================================
# ======== VERSION DOBLE  2.o.3 ===================
# =================================================


import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import base64
from io import BytesIO

# Credenciales de BrowserStack
BROWSERSTACK_USERNAME = 'vascorepo_7EFbsI'
BROWSERSTACK_ACCESS_KEY = 'keVzqBxcjsyMJxYzUG9V'

# Credenciales de EasyBuild
EMAIL = "SomosMundo"
PASSWORD = "74108520!Ii"  # Contraseña para EasyBuild

# URL del sitio
LOGIN_URL = "https://auth.easybuild.website/login?destroyedSession=true&host=app.easybuild.website"

def login_selenium(email, password):
    """
    Función para iniciar sesión utilizando Selenium a través de BrowserStack.
    """
    try:
        # Configuración de BrowserStack con 'options'
        options = webdriver.ChromeOptions()
        options.set_capability('bstack:options', {
            'os': 'Windows',
            'osVersion': '10',
            'buildName': 'Build 1.0',
            'sessionName': 'EasyBuild Login Test',
            'userName': BROWSERSTACK_USERNAME,
            'accessKey': BROWSERSTACK_ACCESS_KEY
        })
        options.set_capability('browserName', 'Chrome')
        options.set_capability('browserVersion', 'latest')

        # URL de BrowserStack
        browserstack_url = f"http://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

        # Conectarse a BrowserStack con 'options'
        driver = webdriver.Remote(command_executor=browserstack_url, options=options)

        # Navegar a la página de inicio de sesión
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
            # Tomar la captura de pantalla
            screenshot = driver.get_screenshot_as_png()

            return driver, screenshot
        else:
            st.error("Error al iniciar sesión. Verifica tus credenciales.")
            driver.quit()
            return None, None
    except Exception as e:
        st.error(f"Error durante el inicio de sesión con Selenium: {e}")
        return None, None

def display_screenshot(screenshot):
    """
    Función para mostrar la captura de pantalla en Streamlit.
    """
    st.image(screenshot, caption='Captura de pantalla después del inicio de sesión', use_column_width=True)

def main():
    st.set_page_config(page_title="Automatización de Reportes - EasyBuild", layout="wide")
    st.title("Automatización de Reportes - EasyBuild")

    st.write("""
    Este aplicativo permite iniciar sesión en [EasyBuild](https://auth.easybuild.website/login) utilizando Selenium.
    """)

    # Primer intento de iniciar sesión
    if st.button("Iniciar Sesión en EasyBuild - Opción 1"):
        driver, screenshot = login_selenium(EMAIL, PASSWORD)
        if driver:
            st.success("Inicio de sesión exitoso en Opción 1.")
            if screenshot:
                display_screenshot(screenshot)
            driver.quit()

    # Segundo intento de iniciar sesión (duplicado)
    if st.button("Iniciar Sesión en EasyBuild - Opción 2"):
        driver, screenshot = login_selenium(EMAIL, PASSWORD)
        if driver:
            st.success("Inicio de sesión exitoso en Opción 2.")
            if screenshot:
                display_screenshot(screenshot)
            driver.quit()

if __name__ == "__main__":
    main()
