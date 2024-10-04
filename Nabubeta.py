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
    Función para iniciar sesión en Smarty usando BrowserStack.
    Dejará que el usuario resuelva el reCAPTCHA manualmente y continuará después.
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
        wait = WebDriverWait(driver, 15)

        # Encontrar y rellenar los campos de usuario y contraseña
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'data[User][username]')))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, 'data[User][password]')))

        username_field.send_keys(username)
        password_field.send_keys(password)

        # Mostrar una instrucción en Streamlit
        st.warning("Por favor, completa el CAPTCHA manualmente en el navegador y luego presiona continuar en Streamlit.")

        # Pausar el script esperando que el usuario presione el botón "Continuar" en Streamlit
        if st.button("Continuar"):
            # Después de que el usuario complete el CAPTCHA manualmente y presione continuar
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()

            # Esperar un poco para que procese el inicio de sesión
            time.sleep(5)

            # Captura de pantalla después de intentar iniciar sesión
            screenshot = driver.get_screenshot_as_png()
            st.image(screenshot, caption='Después de hacer clic en Ingresar en Smarty', use_column_width=True)

            # Verificar si el inicio de sesión fue exitoso
            if driver.current_url != SMARTY_LOGIN_URL:
                st.success("Inicio de sesión exitoso en Smarty.")
            else:
                st.error("Error al iniciar sesión en Smarty. Verifica tus credenciales o el reCAPTCHA.")
            driver.quit()
    except Exception as e:
        st.error(f"Error durante el inicio de sesión en Smarty: {e}")

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
        login_selenium_smart(SMARTY_USERNAME, SMARTY_PASSWORD, use_browserstack=use_browserstack)

if __name__ == "__main__":
    main()
