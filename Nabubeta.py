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

# Credenciales de Smarty
SMARTY_USERNAME = "Soop"
SMARTY_PASSWORD = "74108520"

# URL de Smarty
SMARTY_LOGIN_URL = "https://smartycart.com.ar/users/login"

def login_selenium_smart_local(username, password):
    """
    Función para iniciar sesión en Smarty usando un navegador local.
    Dejará que el usuario resuelva el reCAPTCHA manualmente y continuará después.
    """
    try:
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

    # Iniciar sesión en Smarty usando el navegador local
    if st.button("Iniciar Sesión en Smarty"):
        login_selenium_smart_local(SMARTY_USERNAME, SMARTY_PASSWORD)

if __name__ == "__main__":
    main()

