import json
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Función para cargar cookies de sesión
def load_cookies(driver, cookie_file):
    with open(cookie_file, 'r') as f:
        cookies = json.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)

# Función para iniciar sesión en Smarty con cookies
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

        # Cargar las cookies de sesión
        load_cookies(driver, 'cookies.json')

        # Refrescar la página para aplicar las cookies y acceder como usuario autenticado
        driver.refresh()
        time.sleep(3)

        # Ahora ya estás autenticado y puedes automatizar acciones dentro de Smarty
        st.success("Inicio de sesión exitoso con cookies. Ahora puedes automatizar acciones.")

        # Aquí puedes agregar acciones automatizadas
        
