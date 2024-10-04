# ====== VERSION 1.o ==========
# ====== Funcando ============= bien bien
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
EMAIL = "SomosMundo"
PASSWORD = "74108520!Ii"  # Contraseña para EasyBuild

# URLs del sitio
LOGIN_URL = "https://auth.easybuild.website/login?destroyedSession=true&host=app.easybuild.website"
SALES_URL = "https://app.easybuild.website/admin/e-commerce/sales"
PRODUCTS_URL = "https://app.easybuild.website/admin/e-commerce/products"
STATS_SALES_URL = "https://app.easybuild.website/admin/statistics/sales"

def login_and_navigate_selenium(email, password, target_url):
    """
    Función para iniciar sesión en EasyBuild y navegar a la página seleccionada.
    """
    try:
        # Configuración de BrowserStack con 'options'
        options = webdriver.ChromeOptions()
        options.set_capability('bstack:options', {
            'os': 'Windows',
            'osVersion': '10',
            'buildName': 'Build 1.0',
            'sessionName': 'EasyBuild Login and Navigation',
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

        # Esperar a que el inicio de sesión sea exitoso
        time.sleep(5)

        # Navegar a la página seleccionada (ventas, productos o estadísticas)
        driver.get(target_url)

        # Esperar a que la página cargue
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        st.success(f"Navegaste a la página: {target_url} exitosamente.")

        # Aquí podrías agregar código para extraer o manipular datos de la página

        return driver

    except Exception as e:
        st.error(f"Error durante el inicio de sesión o la navegación: {e}")
        return None

def main():
    st.set_page_config(page_title="Automatización - EasyBuild", layout="wide")
    st.title("Automatización - EasyBuild")

    st.write("""
    Este aplicativo permite iniciar sesión en EasyBuild y navegar a la página seleccionada:
    - Ventas
    - Productos
    - Estadísticas de Ventas Online
    """)

    # Selección de la página a la que navegar
    opcion = st.selectbox("Selecciona la página a la que deseas navegar:", 
                          ["Gestor de Ventas", "Productos", "Estadísticas de Ventas Online"])

    # Mapeo de la opción seleccionada a la URL correspondiente
    target_url = SALES_URL if opcion == "Gestor de Ventas" else PRODUCTS_URL if opcion == "Productos" else STATS_SALES_URL

    if st.button("Iniciar Sesión y Navegar"):
        driver = login_and_navigate_selenium(EMAIL, PASSWORD, target_url)
        if driver:
            st.success("Proceso completado.")
            driver.quit()

if __name__ == "__main__":
    main()
