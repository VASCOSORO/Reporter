# ===== version 1.o.1 andando ....

import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager  # Para manejar el driver local

# Credenciales de EasyBuild
EMAIL = "SomosMundo"
PASSWORD = "74108520!Ii"  # Contraseña para EasyBuild

# URL del sitio
LOGIN_URL = "https://auth.easybuild.website/login?destroyedSession=true&host=app.easybuild.website"
SALES_URL = "https://app.easybuild.website/admin/e-commerce/sales"

def login_and_navigate_selenium(email, password, target_url):
    """
    Función para iniciar sesión en EasyBuild y navegar a la página seleccionada.
    """
    try:
        # Configuración del driver local
        driver = webdriver.Chrome(ChromeDriverManager().install())

        # Navegar a la página de inicio de sesión
        driver.get(LOGIN_URL)

        # Esperar a que la página cargue
        wait = WebDriverWait(driver, 10)
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))

        # Ingresar las credenciales
        username_field.send_keys(email)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        # Esperar a que el inicio de sesión sea exitoso
        time.sleep(5)

        # Navegar a la URL seleccionada (Ventas)
        driver.get(target_url)

        # Esperar a que la página cargue completamente
        time.sleep(5)

        # Devolver el driver para interactuar con él después
        return driver

    except Exception as e:
        st.error(f"Error durante el inicio de sesión o la navegación: {e}")
        return None

def analyze_clickable_elements(driver):
    """
    Función para analizar los elementos clickeables dentro de la página (links, botones).
    """
    try:
        # Obtener todos los enlaces clickeables
        clickable_elements = driver.find_elements(By.TAG_NAME, 'a')
        clickable_data = []

        for element in clickable_elements:
            href = element.get_attribute('href')
            text = element.text
            clickable_data.append({'Texto': text, 'Enlace': href})

        # Convertir los datos a un DataFrame para mostrar en Streamlit
        df = pd.DataFrame(clickable_data)
        return df

    except Exception as e:
        st.error(f"Error al analizar los elementos clickeables: {e}")
        return None

def main():
    st.set_page_config(page_title="Automatización de EasyBuild", layout="wide")
    st.title("Automatización de EasyBuild - Análisis de elementos clickeables")

    if st.button("Iniciar Sesión y Analizar Página de Ventas"):
        # Iniciar sesión y navegar a la página de ventas
        driver = login_and_navigate_selenium(EMAIL, PASSWORD, SALES_URL)
        
        if driver:
            st.success("Sesión iniciada y en la página de ventas.")
            
            # Analizar los elementos clickeables en la página de ventas
            clickable_elements = analyze_clickable_elements(driver)
            
            if clickable_elements is not None:
                st.success("Elementos clickeables extraídos.")
                st.dataframe(clickable_elements)  # Mostrar los elementos en un DataFrame
                
            driver.quit()  # Cerrar el navegador

if __name__ == "__main__":
    main()
