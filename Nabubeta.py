import streamlit as st
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL del sitio donde querés extraer la información
url_products = "https://smartycart.com.ar/Products/index/clearFilters:true"

# Configuración del driver
def init_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Función para automatizar la selección de productos y descarga del CSV
def automate_smartycart():
    driver = init_browser()
    driver.get(url_products)
    
    # Esperar hasta que el botón de selección de todos los productos sea visible
    try:
        select_all_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Seleccionar los 1813 productos de la búsqueda."))
        )
        select_all_link.click()  # Hacer clic en el enlace para seleccionar todos los productos
        
        st.write("Se seleccionaron todos los productos correctamente.")
        
        # Esperar hasta que el botón de descarga esté disponible y hacer clic
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.downloadCsv"))
        )
        csv_url = download_button.get_attribute("href")
        
        # Descargar el CSV
        csv_response = requests.get(csv_url)
        if csv_response.status_code == 200:
            with open("productos.csv", "wb") as f:
                f.write(csv_response.content)
            st.write("CSV descargado exitosamente.")
        else:
            st.write(f"Error al descargar el CSV: {csv_response.status_code}")
    except Exception as e:
        st.write(f"Error durante la automatización: {str(e)}")
    finally:
        driver.quit()

# Botón de Streamlit para ejecutar el proceso
if st.button("Obtener Datos"):
    automate_smartycart()
