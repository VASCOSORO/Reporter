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

# Credenciales de Smarty
SMARTY_USERNAME = "Soop"
SMARTY_PASSWORD = "74108520"

# URL de Smarty
SMARTY_LOGIN_URL = "https://smartycart.com.ar/users/login"

def login_selenium_smart(username, password, use_browserstack=True):
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

        # Captura de pantalla después de cargar la página
        screenshot1 = driver.get_screenshot_as_png()
        st.image(screenshot1, caption='Página de inicio de sesión de Smarty cargada', use_column_width=True)

        # Esperar a que la página cargue
        wait = WebDriverWait(driver, 15)

        # Encontrar y rellenar los campos de usuario y contraseña
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'data[User][username]')))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, 'data[User][password]')))

        username_field.send_keys(username)
        password_field.send_keys(password)

        # Captura de pantalla después de ingresar credenciales
        screenshot2 = driver.get_screenshot_as_png()
        st.image(screenshot2, caption='Credenciales ingresadas en Smarty', use_column_width=True)

        # Marcar la casilla del reCAPTCHA (esperar hasta que esté disponible)
        captcha_checkbox = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border")))
        captcha_checkbox.click()
        
        # Captura de pantalla después de seleccionar el reCAPTCHA
        screenshot3 = driver.get_screenshot_as_png()
        st.image(screenshot3, caption='reCAPTCHA seleccionado', use_column_width=True)

        # Esperar un poco más después de hacer clic (para que Google verifique el reCAPTCHA)
        time.sleep(3)

        # Enviar el formulario
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        # Esperar un poco para que procese el inicio de sesión
        time.sleep(5)

        # Captura de pantalla después de intentar iniciar sesión
        screenshot4 = driver.get_screenshot_as_png()
        st.image(screenshot4, caption='Después de intentar iniciar sesión en Smarty', use_column_width=True)

        # Verificar si el inicio de sesión fue exitoso
        if driver.current_url != SMARTY_LOGIN_URL:
            st.success("Inicio de sesión exitoso en Smarty.")
            return driver, screenshot4
        else:
            st.error("Error al iniciar sesión en Smarty. Verifica tus credenciales o el reCAPTCHA.")
            driver.quit()
            return None, None
    except Exception as e:
        st.error(f"Error durante el inicio de sesión en Smarty: {e}")
        return None, None

def main():
    st.set_page_config(page_title="Automatización de Reportes", layout="wide")
    st.title("Automatización de Reportes - Smarty")

    st.write("""
    Este aplicativo permite iniciar sesión en [Smarty](https://smartycart.com.ar/users/login) utilizando Selenium.
    """)

    # Seleccionar si usar BrowserStack o un controlador local
    use_browserstack = st.checkbox("Usar BrowserStack", value=True)

    # Iniciar sesión en Smarty
    if st.button("Iniciar Sesión en Smarty"):
        driver, screenshot = login_selenium_smart(SMARTY_USERNAME, SMARTY_PASSWORD, use_browserstack=use_browserstack)
        if driver:
            st.success("Inicio de sesión exitoso en Smarty.")
            if screenshot:
                display_screenshot(screenshot)
            driver.quit()

if __name__ == "__main__":
    main()


