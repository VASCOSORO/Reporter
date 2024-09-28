import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Función para iniciar sesión en Smarti
def login_smarti(username, password):
    # Configurar opciones de Chrome para que el navegador sea visible
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    # Eliminar el modo headless para que puedas interactuar con el navegador
    # chrome_options.add_argument("--headless")  # No usar headless para poder ver el navegador

    # Inicializar el controlador de Selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Navegar a la página de inicio de sesión
        driver.get("https://smartycart.com.ar/users/login")
        time.sleep(3)  # Esperar a que la página cargue

        # Encontrar los campos de usuario y contraseña e ingresar las credenciales
        user_field = driver.find_element(By.NAME, "username")  # Ajusta el selector según la página
        pass_field = driver.find_element(By.NAME, "password")  # Ajusta el selector según la página

        user_field.send_keys(username)
        pass_field.send_keys(password)

        # Mostrar una advertencia en Streamlit para que el usuario resuelva el reCAPTCHA
        st.warning("Por favor, completa el reCAPTCHA manualmente en el navegador que se abrió.")
        
        # Esperar hasta que completes el reCAPTCHA manualmente (espera 60 segundos)
        st.info("Esperando 60 segundos para que completes el reCAPTCHA...")
        time.sleep(60)

        # Intentar hacer clic en el botón de "Ingresar" después del reCAPTCHA
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

        time.sleep(5)  # Esperar a que el inicio de sesión se procese

        # Verificar si el inicio de sesión fue exitoso
        if "dashboard" in driver.current_url.lower():
            return True, "Inicio de sesión exitoso."
        else:
            return False, "Fallo al iniciar sesión. Verifica tus credenciales o el reCAPTCHA."

    except Exception as e:
        return False, f"Ocurrió un error: {str(e)}"
    finally:
        driver.quit()

# Interfaz de usuario con Streamlit
def main():
    st.title("Automatización de Inicio de Sesión en Smarti")

    st.write("Este script utiliza Selenium para automatizar el inicio de sesión en Smarti.")

    with st.form("login_form"):
        username = st.text_input("Usuario", value="Soop")
        password = st.text_input("Contraseña", type="password", value="74108520")
        submit_button = st.form_submit_button("Iniciar Sesión")

    if submit_button:
        with st.spinner("Procesando..."):
            success, message = login_smarti(username, password)
            if success:
                st.success(message)
            else:
                st.error(message)

if __name__ == "__main__":
    main()
