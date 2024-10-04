# ===========================
# ======= DALEEEE DALEEEE ===== 2
# ====== paso el lead ========

import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager

# Credenciales de BrowserStack
BROWSERSTACK_USERNAME = 'vascorepo_7EFbsI'
BROWSERSTACK_ACCESS_KEY = 'keVzqBxcjsyMJxYzUG9V'

# Credenciales de EasyBuild
EASYBUILD_EMAIL = "SomosMundo"
EASYBUILD_PASSWORD = "74108520!Ii"

# Credenciales de LeadSales
LEADSALES_EMAIL = "jsanovsky@gmail.com"
LEADSALES_PASSWORD = "Pasteur39"

# URLs de los sitios
EASYBUILD_LOGIN_URL = "https://auth.easybuild.website/login?destroyedSession=true&host=app.easybuild.website"
LEADSALES_LOGIN_URL = "https://leadsales.services/login"
LEADSALES_DIRECTORY_URL = "https://leadsales.services/workspace/directory"  # URL de la página de Leadsales a visitar después de iniciar sesión

def login_selenium_easybuild(email, password, login_url, use_browserstack=True):
    """
    Función para iniciar sesión en EasyBuild con Selenium, con opción para usar BrowserStack o un controlador local.
    """
    try:
        if use_browserstack:
            # Configuración de BrowserStack con 'options'
            options = webdriver.ChromeOptions()
            options.set_capability('bstack:options', {
                'os': 'Windows',
                'osVersion': '10',
                'buildName': 'Build EasyBuild',
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
        else:
            # Usar controlador local (ChromeDriver)
            driver = webdriver.Chrome(ChromeDriverManager().install())

        # Navegar a la página de EasyBuild
        driver.get(login_url)

        # Esperar a que la página cargue
        wait = WebDriverWait(driver, 10)

        # Encontrar y rellenar los campos de usuario y contraseña
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))

        username_field.send_keys(email)
        password_field.send_keys(password)

        # Enviar el formulario
        password_field.send_keys(Keys.RETURN)

        # Esperar un poco para que procese el inicio de sesión
        time.sleep(5)

        # Tomar la captura de pantalla
        screenshot = driver.get_screenshot_as_png()

        if driver.current_url != login_url:
            st.success("Inicio de sesión exitoso en EasyBuild.")
            return driver, screenshot
        else:
            st.error("Error al iniciar sesión en EasyBuild. Verifica tus credenciales.")
            driver.quit()
            return None, None
    except Exception as e:
        st.error(f"Error durante el inicio de sesión en EasyBuild: {e}")
        return None, None

def login_selenium_leadsales(email, password, use_browserstack=True):
    """
    Función para iniciar sesión en LeadSales con Selenium, con opción para usar BrowserStack o un controlador local.
    """
    try:
        if use_browserstack:
            # Configuración de BrowserStack con 'options'
            options = webdriver.ChromeOptions()
            options.set_capability('bstack:options', {
                'os': 'Windows',
                'osVersion': '10',
                'buildName': 'Build LeadSales',
                'sessionName': 'LeadSales Login Test',
                'userName': BROWSERSTACK_USERNAME,
                'accessKey': BROWSERSTACK_ACCESS_KEY
            })
            options.set_capability('browserName', 'Chrome')
            options.set_capability('browserVersion', 'latest')

            # URL de BrowserStack
            browserstack_url = f"http://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

            # Conectarse a BrowserStack con 'options'
            driver = webdriver.Remote(command_executor=browserstack_url, options=options)
        else:
            # Usar controlador local (ChromeDriver)
            driver = webdriver.Chrome(ChromeDriverManager().install())

        # Navegar a la página de LeadSales
        driver.get(LEADSALES_LOGIN_URL)
        st.write("Página de LeadSales cargada.")

        # Esperar a que la página cargue
        wait = WebDriverWait(driver, 10)

        # Captura de pantalla después de cargar la página
        screenshot1 = driver.get_screenshot_as_png()
        st.image(screenshot1, caption='Página de LeadSales cargada', use_column_width=True)

        # Encontrar y rellenar los campos de usuario y contraseña
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'email')))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, 'Password')))

        username_field.send_keys(email)
        password_field.send_keys(password)

        # Captura de pantalla después de ingresar credenciales
        screenshot2 = driver.get_screenshot_as_png()
        st.image(screenshot2, caption='Credenciales ingresadas', use_column_width=True)

        # Enviar el formulario
        password_field.send_keys(Keys.RETURN)

        # Esperar un poco para que procese el inicio de sesión
        time.sleep(5)

        # Captura de pantalla después de intentar iniciar sesión
        screenshot3 = driver.get_screenshot_as_png()
        st.image(screenshot3, caption='Después de intentar iniciar sesión', use_column_width=True)

        if driver.current_url != LEADSALES_LOGIN_URL:
            st.success("Inicio de sesión exitoso en LeadSales.")
            return driver, screenshot3
        else:
            st.error("Error al iniciar sesión en LeadSales. Verifica tus credenciales.")
            driver.quit()
            return None, None
    except Exception as e:
        st.error(f"Error durante el inicio de sesión en LeadSales: {e}")
        return None, None

def display_screenshot(screenshot):
    """
    Función para mostrar la captura de pantalla en Streamlit.
    """
    st.image(screenshot, caption='Captura de pantalla después del inicio de sesión', use_column_width=True)

def main():
    st.set_page_config(page_title="Automatización de Reportes", layout="wide")
    st.title("Automatización de Reportes con Ingreso")

    st.write("""
    Comprobando ingresos positivos, lo logramos fue buena idea!👨‍🦼🕶️.
    """)

    # Seleccionar si usar BrowserStack o un controlador local
    use_browserstack = st.checkbox("Usar BrowserStack", value=True)

    # Iniciar sesión en EasyBuild
    if st.button("Iniciar Check de Catalogo"):
        driver, screenshot = login_selenium_easybuild(EASYBUILD_EMAIL, EASYBUILD_PASSWORD, EASYBUILD_LOGIN_URL, use_browserstack=use_browserstack)
        if driver:
            st.success("Inicio de sesión exitoso en EasyBuild.")
            if screenshot:
                display_screenshot(screenshot)
            driver.quit()

    # Línea divisoria gris
    st.markdown("<hr style='border:1px solid gray'>", unsafe_allow_html=True)

    # Iniciar sesión en LeadSales
    if st.button("Iniciar LeadSales"):
        driver, screenshot = login_selenium_leadsales(LEADSALES_EMAIL, LEADSALES_PASSWORD, use_browserstack=use_browserstack)
        if driver:
            st.success("Inicio de sesión exitoso en LeadSales.")
            if screenshot:
                display_screenshot(screenshot)
            driver.quit()

if __name__ == "__main__":
    main()
