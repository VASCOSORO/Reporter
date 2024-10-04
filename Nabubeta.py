import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# URL del sitio de inicio de sesión
LOGIN_URL = "https://auth.easybuild.website/login?destroyedSession=true&host=app.easybuild.website"

def login_selenium(email, password):
    """
    Función para iniciar sesión utilizando Selenium.
    """
    try:
        # Configurar el driver de Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Ejecutar en modo headless (sin interfaz)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Instalar y configurar el driver
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(LOGIN_URL)

        # Esperar a que la página cargue
        time.sleep(5)

        # Encontrar y rellenar los campos de usuario y contraseña
        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')

        username_field.send_keys(email)
        password_field.send_keys(password)

        # Enviar el formulario
        password_field.send_keys(Keys.RETURN)

        # Esperar a que se procese el inicio de sesión
        time.sleep(5)

        # Verificar si el inicio de sesión fue exitoso
        if driver.current_url != LOGIN_URL:
            return True
        else:
            return False

    except Exception as e:
        st.error(f"Error durante el inicio de sesión con Selenium: {e}")
        return False
    finally:
        driver.quit()

def main():
    st.set_page_config(page_title="Login EasyBuild", layout="centered")
    st.title("Ingreso a EasyBuild")

    st.write("Por favor, ingresa tus credenciales para iniciar sesión en EasyBuild.")

    # Campos de entrada para Email y Contraseña
    email = st.text_input("Email")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        if not email or not password:
            st.error("Por favor, completa ambos campos.")
        else:
            with st.spinner("Iniciando sesión..."):
                success = login_selenium(email, password)
                if success:
                    st.success("Inicio de sesión exitoso.")
                else:
                    st.error("Error al iniciar sesión. Verifica tus credenciales.")

if __name__ == "__main__":
    main()
