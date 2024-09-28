import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from pyvirtualdisplay import Display

# Función para iniciar sesión en Smarti
def login_smarti(username, password):
    # Crear una pantalla virtual
    display = Display(visible=0, size=(1024, 768))
    display.start()

    # Configurar opciones de Chrome para modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    # Inicializar el controlador de Selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Navegar a la página de inicio de sesión
        driver.get("https://smartycart.com.ar/users/login")
        time.sleep(3)  # Esperar a que la página cargue

        # Encontrar los campos de usuario y contraseña e ingresar las credenciales
        user_field = driver.find_element(By.ID, "username")  # Ajusta el selector según la página
        pass_field = driver.find_element(By.ID, "password")  # Ajusta el selector según la página

        user_field.send_keys(username)
        pass_field.send_keys(password)

        # Enviar el formulario
        pass_field.submit()
        time.sleep(5)  # Esperar a que el inicio de sesión se procese

        # Verificar si el inicio de sesión fue exitoso
        if "dashboard" in driver.current_url.lower():
            return True, "Inicio de sesión exitoso."
        else:
            return False, "Fallo al iniciar sesión. Verifica tus credenciales."

    except Exception as e:
        return False, f"Ocurrió un error: {str(e)}"
    finally:
        driver.quit()
        display.stop()  # Detener la pantalla virtual

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
