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

# Credenciales de Smarty
SMARTY_EMAIL = "Soop"
SMARTY_PASSWORD = "74108520"

# URLs de los sitios
EASYBUILD_LOGIN_URL = "https://auth.easybuild.website/login?destroyedSession=true&host=app.easybuild.website"
LEADSALES_LOGIN_URL = "https://leadsales.services/login"
SMARTY_LOGIN_URL = "https://smartycart.com.ar/users/login"

def login_selenium_smart(email, password, use_browserstack=True):
    """
    Función para iniciar sesión en Smarty con Selenium y manejar el reCAPTCHA.
    """
    try:
        if use_browserstack:
            # Configuración de BrowserStack con 'options'
            options = webdriver.ChromeOptions()
            options.set_capability('bstack:options', {
                'os': 'Windows',
                'osVersion': '10',
                'buildName': 'Build Smarty',
                'sessionName': 'Smarty Login Test',
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

        # Navegar a la página de Smarty
        driver.get(SMARTY_LOGIN_URL)

        # Esperar a que la página cargue
        wait = WebDriverWait(driver, 10)

        # Encontrar y rellenar los campos de usuario y contraseña
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))

        username_field.send_keys(email)
        password_field.send_keys(password)

        # Marcar la casilla del reCAPTCHA (simulación de espera)
        captcha_checkbox = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border")))
        captcha_checkbox.click()
        
        # Esperar un segundo antes de continuar
        time.sleep(2)

        # Enviar el formulario
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        # Esperar un poco para que procese el inicio de sesión
        time.sleep(5)

        # Tomar la captura de pantalla
        screenshot = driver.get_screenshot_as_png()

        if driver.current_url != SMARTY_LOGIN_URL:
            st.success("Inicio de sesión exitoso en Smarty.")
            return driver, screenshot
        else:
            st.error("Error al iniciar sesión en Smarty. Verifica tus credenciales o el reCAPTCHA.")
            driver.quit()
            return None, None
    except Exception as e:
        st.error(f"Error durante el inicio de sesión en Smarty: {e}")
        return None, None

def display_screenshot(screenshot):
    """
    Función para mostrar la captura de pantalla en Streamlit.
    """
    st.image(screenshot, caption='Captura de pantalla después del inicio de sesión', use_column_width=True)

def main():
    st.set_page_config(page_title="Automatización de Reportes", layout="wide")
    st.title("Automatización de Reportes - EasyBuild, LeadSales y Smarty")

    st.write("""
    Este aplicativo permite iniciar sesión en [EasyBuild](https://auth.easybuild.website/login), 
    [LeadSales](https://leadsales.services/login) y [Smarty](https://smartycart.com.ar/users/login) utilizando Selenium.
    """)

    # Seleccionar si usar BrowserStack o un controlador local
    use_browserstack = st.checkbox("Usar BrowserStack", value=True)

    # Iniciar sesión en EasyBuild
    if st.button("Iniciar Sesión en EasyBuild"):
        driver, screenshot = login_selenium_easybuild(EASYBUILD_EMAIL, EASYBUILD_PASSWORD, EASYBUILD_LOGIN_URL, use_browserstack=use_browserstack)
        if driver:
            st.success("Inicio de sesión exitoso en EasyBuild.")
            if screenshot:
                display_screenshot(screenshot)
            driver.quit()

    # Línea divisoria gris
    st.markdown("<hr style='border:1px solid gray'>", unsafe_allow_html=True)

    # Iniciar sesión en LeadSales
    if st.button("Iniciar Sesión en LeadSales"):
        driver, screenshot = login_selenium_leadsales(LEADSALES_EMAIL, LEADSALES_PASSWORD, use_browserstack=use_browserstack)
        if driver:
            st.success("Inicio de sesión exitoso en LeadSales.")
            if screenshot:
                display_screenshot(screenshot)
            driver.quit()

    # Línea divisoria gris
    st.markdown("<hr style='border:1px solid gray'>", unsafe_allow_html=True)

    # Iniciar sesión en Smarty
    if st.button("Iniciar Sesión en Smarty"):
        driver, screenshot = login_selenium_smart(SMARTY_EMAIL, SMARTY_PASSWORD, use_browserstack=use_browserstack)
        if driver:
            st.success("Inicio de sesión exitoso en Smarty.")
            if screenshot:
                display_screenshot(screenshot)
            driver.quit()

if __name__ == "__main__":
    main()

