import json
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Función para cargar cookies de sesión desde un archivo
def load_cookies(driver, cookie_file):
    with open(cookie_file, 'r') as f:
        cookies = json.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)

# Función para acceder a Smarty con cookies de sesión
def access_smarti_with_cookies():
    # Configurar opciones de Chrome para que el navegador sea visible
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    # Inicializar el controlador de Selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Navegar a la página de Smarty
        driver.get("https://smartycart.com.ar")
        time.sleep(3)  # Esperar a que la página cargue

        # Cargar las cookies de sesión desde un archivo JSON
        load_cookies(driver, 'cookies.json')

        # Refrescar la página para aplicar las cookies y acceder como usuario autenticado
        driver.refresh()
        time.sleep(3)

        # Verificar si el acceso fue exitoso
        if "dashboard" in driver.current_url.lower():
            st.success("Inicio de sesión exitoso con cookies. Ahora puedes automatizar acciones.")
        else:
            st.error("No se pudo iniciar sesión. Verifica las cookies.")

        # Aquí puedes agregar acciones automatizadas (ejemplo: búsqueda, scraping, etc.)
        # ...

    except Exception as e:
        st.error(f"Ocurrió un error: {str(e)}")
    
    finally:
        driver.quit()  # Cerrar el navegador siempre, incluso si ocurre un error

# Interfaz de usuario con Streamlit
def main():
    st.title("Automatización en Smarty usando cookies de sesión")

    st.write("Este script utiliza Selenium y cookies para acceder automáticamente a Smarty.")

    if st.button("Acceder a Smarty con cookies"):
        with st.spinner("Accediendo..."):
            access_smarti_with_cookies()

if __name__ == "__main__":
    main()
