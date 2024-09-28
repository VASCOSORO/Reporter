import streamlit as st
from playwright.sync_api import sync_playwright

# Función para hacer login y obtener cookies usando Playwright
def login_smarti(page):
    url_login = "https://smartycart.com.ar/users/login"
    page.goto(url_login)
    
    # Ingresar credenciales
    page.fill('input[name="username"]', 'Soop')  # Ajustar selector de nombre de usuario
    page.fill('input[name="password"]', '74108520')  # Ajustar selector de contraseña
    
    # Hacer clic en el botón de login
    page.click('button#login_button')  # Cambiar a un selector válido para el botón de login
    
    # Esperar a que la página cargue después del login
    page.wait_for_timeout(5000)  # Esperar 5 segundos para asegurarse de que esté logueado

# Función para seleccionar productos y descargar el CSV
def download_csv(page):
    url_products = "https://smartycart.com.ar/Products/index/clearFilters:true"
    page.goto(url_products)
    
    # Seleccionar la casilla de verificación para todos los productos
    page.click('input[type="checkbox"]')  # Cambiar si es necesario
    
    # Seleccionar todos los productos de la búsqueda
    page.click('a:has-text("Seleccionar los xxx productos de la búsqueda")')  # Ajustar si es necesario
    
    # Descargar el archivo CSV
    page.click('a:has-text("Descargar CSV")')  # Cambiar si es necesario
    
    # Esperar la descarga
    page.wait_for_timeout(5000)  # Esperar 5 segundos para la descarga

# Interfaz en Streamlit
st.title("Automatización SmartyCart con Playwright")

if st.button("Solicitar Cookies de Acceso y Descargar CSV"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Iniciar sesión y descargar CSV
        login_smarti(page)
        st.write("Autenticado exitosamente.")
        
        download_csv(page)
        st.write("Descarga completada.")
        
        browser.close()
