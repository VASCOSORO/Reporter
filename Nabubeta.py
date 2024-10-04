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

def extract_sales_data(driver):
    """
    Función para extraer datos de la tabla de ventas en EasyBuild.
    """
    time.sleep(10)  # Asegura que la tabla esté completamente cargada
    table = driver.find_element(By.TAG_NAME, "table")
    
    # Extraer los datos de la tabla de ventas
    rows = table.find_elements(By.TAG_NAME, "tr")
    data = []

    for row in rows[1:]:  # Ignorar la cabecera
        cols = row.find_elements(By.TAG_NAME, "td")
        order = cols[0].text
        buyer = cols[1].text
        date = cols[2].text
        products_link = cols[3].find_element(By.TAG_NAME, "a").get_attribute("href")
        total = cols[4].text
        status = cols[5].text
        pdf_link = cols[6].find_element(By.TAG_NAME, "a").get_attribute("href")
        
        # Almacenar los datos en una lista
        data.append([order, buyer, date, products_link, total, status, pdf_link])

    # Convertir a DataFrame para visualizar en Streamlit
    df = pd.DataFrame(data, columns=["Orden", "Comprador", "Fecha", "Productos Link", "Total", "Estado", "PDF Link"])
    return df

def login_and_extract_selenium(email, password, target_url):
    """
    Función para iniciar sesión en EasyBuild, navegar a las ventas y extraer la tabla de datos.
    """
    try:
        # Configuración del driver local
        driver = webdriver.Chrome(ChromeDriverManager().install())

        # Navegar a la página de inicio de sesión
        driver.get(LOGIN_URL)

        # Esperar a que la página cargue
        time.sleep(5)
        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')

        # Ingresar las credenciales
        username_field.send_keys(email)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        # Esperar a que el inicio de sesión sea exitoso
        time.sleep(5)

        # Navegar a la página de ventas
        driver.get(target_url)

        # Extraer la tabla de ventas
        sales_data = extract_sales_data(driver)

        return sales_data

    except Exception as e:
        st.error(f"Error durante el inicio de sesión o la extracción de datos: {e}")
        return None

def main():
    st.set_page_config(page_title="Automatización de EasyBuild", layout="wide")
    st.title("Automatización de EasyBuild")

    if st.button("Iniciar Sesión y Extraer Ventas"):
        sales_data = login_and_extract_selenium(EMAIL, PASSWORD, SALES_URL)
        if sales_data is not None:
            st.success("Datos extraídos exitosamente.")
            st.dataframe(sales_data)

if __name__ == "__main__":
    main()

