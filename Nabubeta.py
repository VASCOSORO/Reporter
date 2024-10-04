# ===== version 1.o.1 andando ....

import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Esta es la importación que faltaba
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import pandas as pd

# Credenciales de BrowserStack
BROWSERSTACK_USERNAME = 'vascorepo_7EFbsI'
BROWSERSTACK_ACCESS_KEY = 'keVzqBxcjsyMJxYzUG9V'

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
    # Esperar a que la tabla esté presente
    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

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

def login_and_extract_selenium(email, password):
    """
    Función para iniciar sesión en EasyBuild, navegar a las ventas y extraer la tabla de datos.
    """
    try:
        # Configuración de BrowserStack con 'options'
        options = webdriver.ChromeOptions()
        options.set_capability('bstack:options', {
            'os': 'Windows',
            'osVersion': '10',
            'buildName': 'Build 1.0',
            'sessionName': 'EasyBuild Ventas Extractor',
            'userName': BROWSERSTACK_USERNAME,
            'accessKey': BROWSERSTACK_ACCESS_KEY
        })
        options.set_capability('browserName', 'Chrome')
        options.set_capability('browserVersion', 'latest')

        # URL de BrowserStack
        browserstack_url = f"http://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

        # Conectarse a BrowserStack con 'options'
        driver = webdriver.Remote(command_executor=browserstack_url, options=options)

        # Navegar a la página de inicio de sesión
        driver.get(LOGIN_URL)

        # Esperar a que la página cargue
        wait = WebDriverWait(driver, 10)
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))

        # Ingresar las credenciales
        username_field.send_keys(email)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)  # Aquí es donde se usa 'Keys'

        # Esperar a que el inicio de sesión sea exitoso
        time.sleep(5)

        # Navegar a la página de ventas
        driver.get(SALES_URL)

        # Extraer la tabla de ventas
        sales_data = extract_sales_data(driver)

        return sales_data

    except Exception as e:
        st.error(f"Error durante el inicio de sesión o la extracción de datos: {e}")
        return None

def main():
    st.set_page_config(page_title="Automatización de Ventas - EasyBuild", layout="wide")
    st.title("Automatización de Ventas - EasyBuild")

    if st.button("Iniciar Sesión y Extraer Ventas"):
        sales_data = login_and_extract_selenium(EMAIL, PASSWORD)
        if sales_data is not None:
            st.success("Datos extraídos exitosamente.")
            st.dataframe(sales_data)

if __name__ == "__main__":
    main()
