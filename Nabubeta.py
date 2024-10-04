import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Credenciales de BrowserStack
BROWSERSTACK_USERNAME = 'vascorepo_7EFbsI'
BROWSERSTACK_ACCESS_KEY = 'keVzqBxcjsyMJxYzUG9V'

# Credenciales de EasyBuild
EASYBUILD_EMAIL = "SomosMundo"
EASYBUILD_PASSWORD = "74108520!Ii"  # Contraseña para EasyBuild

# Credenciales de LeadSales
LEADSALES_EMAIL = "jsanovsky@gmail.com"
LEADSALES_PASSWORD = "Pasteur39"

# URLs de los sitios
EASYBUILD_LOGIN_URL = "https://auth.easybuild.website/login?destroyedSession=true&host=app.easybuild.website"
LEADSALES_LOGIN_URL = "https://leadsales.services/login"

def login_selenium(email, password, login_url):
    """
    Función para iniciar sesión utilizando Selenium a través de BrowserStack.
    """
    try:
        # Configuración de BrowserStack con 'options' básicas
        options = webdriver.ChromeOptions()
        options.set_capability('browserName', 'Chrome')
        options.set_capability('browserVersion', 'latest')
        options.set_capability('bstack:options', {
            'os': 'Windows',
            'osVersion': '10',
            'userName': BROWSERSTACK_USERNAME,
            'accessKey': BROWSERSTACK_ACCESS_KEY
        })

        # URL de BrowserStack
        browserstack_url = f"http://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

        # Conectarse a BrowserStack con 'options'
        driver = webdriver.Remote(command_executor=browserstack_url, options=options)

        # Navegar a la página de inicio de sesión
        driver.get(login_url)

        # Esperar a que la página cargue
        wait = WebDriverWait(driver, 10)

        # Encontrar y rellenar los campos de usuario y contraseña
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'email')))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))

        username_field.send_keys(email)
        password_field.send_keys(password)

        # Enviar el formulario
        password_field.send_keys(Keys.RETURN)

        # Esperar a que se procese el inicio de sesión y verificar si fue exitoso
        time.sleep(5)
        if driver.current_url != login_url:
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
    st.set_page_config(page_title="Automatización de Reportes", layout="wide")
    st.title("Automatización de Reportes - EasyBuild y LeadSales")

    st.write("""
    Este aplicativo permite iniciar sesión en diferentes sitios utilizando Selenium.
    """)

    # Seleccionar el sitio al que queremos ingresar
    opcion = st.selectbox("Selecciona el sitio al que deseas ingresar:", 
                          ["EasyBuild", "LeadSales"])

    if st.button("Iniciar Sesión y Tomar Captura"):
        if opcion == "EasyBuild":
            driver, screenshot = login_selenium(EASYBUILD_EMAIL, EASYBUILD_PASSWORD, EASYBUILD_LOGIN_URL)
        else:
            driver, screenshot = login_selenium(LEADSALES_EMAIL, LEADSALES_PASSWORD, LEADSALES_LOGIN_URL)

        if driver:
            st.success(f"Inicio de sesión exitoso en {opcion}.")
            if screenshot:
                display_screenshot(screenshot)
            driver.quit()

if __name__ == "__main__":
    main()
