import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuración de opciones para Selenium (navegador en modo headless)
def init_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Función para hacer login en SmartyCart y obtener las cookies de sesión
def login_smarti(driver):
    url_login = "https://smartycart.com.ar/users/login"
    driver.get(url_login)
    
    # Esperar a que cargue la página de login
    driver.implicitly_wait(10)
    
    # Ingresar las credenciales de login (modificar según los selectores del sitio)
    username = driver.find_element(By.NAME, 'username')  # Cambiar por el selector correcto
    password = driver.find_element(By.NAME, 'password')  # Cambiar por el selector correcto
    
    # Completar el login
    username.send_keys('Soop')  # Tu usuario
    password.send_keys('74108520')  # Tu contraseña
    login_button = driver.find_element(By.ID, 'login_button')  # Reemplazar por el ID correcto
    login_button.click()
    
    # Esperar unos segundos para completar el login
    time.sleep(5)
    
    # Obtener las cookies de la sesión
    cookies = driver.get_cookies()
    return cookies

# Función para seleccionar todos los productos y descargar CSV
def download_csv(driver):
    url_products = "https://smartycart.com.ar/Products/index/clearFilters:true"
    driver.get(url_products)
    
    # Seleccionar la casilla para marcar todos los productos
    checkbox = driver.find_element(By.XPATH, '//input[@type="checkbox"]')  # Cambiar si es necesario
    checkbox.click()
    
    # Seleccionar la opción para marcar todos los productos de la búsqueda
    select_all = driver.find_element(By.XPATH, '//a[text()="Seleccionar los xxx productos de la búsqueda"]')  # Cambiar por el texto real
    select_all.click()
    
    # Confirmar la selección y descargar el CSV
    download_button = driver.find_element(By.XPATH, '//a[text()="Descargar CSV"]')  # Cambiar si es necesario
    download_button.click()

# Interfaz en Streamlit
st.title("Automatización SmartyCart")
st.write("Haz clic en el botón para solicitar las cookies y descargar el CSV.")

if st.button("Solicitar Cookies de Acceso y Descargar CSV"):
    driver = init_browser()
    cookies = login_smarti(driver)
    
    if cookies:
        st.write("Autenticación exitosa, iniciando descarga...")
        download_csv(driver)
        st.write("Descarga completada.")
    else:
        st.write("Error en la autenticación.")
