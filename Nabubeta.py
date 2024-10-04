# ===========================
# ======= DALEEEE DALEEEE ===== 2 ww
# ====== paso el lead ========

import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Credenciales de BrowserStack
BROWSERSTACK_USERNAME = 'vascorepo_7EFbsI'
BROWSERSTACK_ACCESS_KEY = 'keVzqBxcjsyMJxYzUG9V'

def open_whatsapp_web(use_browserstack=True):
    """
    Función para abrir WhatsApp Web en un navegador utilizando Selenium y BrowserStack.
    """
    try:
        if use_browserstack:
            # Configuración de BrowserStack con 'options'
            options = webdriver.ChromeOptions()
            options.set_capability('bstack:options', {
                'os': 'Windows',
                'osVersion': '10',
                'buildName': 'Build WhatsApp Web',
                'sessionName': 'WhatsApp Web Login Test',
                'userName': BROWSERSTACK_USERNAME,
                'accessKey': BROWSERSTACK_ACCESS_KEY
            })
            options.set_capability('browserName', 'Chrome')
            options.set_capability('browserVersion', 'latest')

            # URL de BrowserStack
            browserstack_url = f"http://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

            # Conectarse a BrowserStack con 'options'
            driver = webdriver.Remote(command_executor=browserstack_url, options=options)
        else:
            # Usar controlador local (ChromeDriver)
            driver = webdriver.Chrome(ChromeDriverManager().install())

        # Navegar a la página de WhatsApp Web
        driver.get("https://web.whatsapp.com")
        st.write("Página de WhatsApp Web cargada. Escaneá el código QR desde tu teléfono.")

        # Esperar hasta que aparezca un elemento del DOM que confirme que la página cargó
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas'))  # El QR se encuentra dentro de un <canvas>
        )

        st.write("Código QR detectado, esperando que lo escanees con tu teléfono...")

        # Mantener abierta la página para que puedas escanear el QR
        while True:
            time.sleep(10)

    except Exception as e:
        st.error(f"Error durante la apertura de WhatsApp Web: {e}")

def main():
    st.set_page_config(page_title="Login WhatsApp Web", layout="wide")
    st.title("Login en WhatsApp Web usando QR")

    st.write("""
    Este aplicativo abre WhatsApp Web en un navegador usando Selenium y espera a que escanees el código QR.
    """)

    # Seleccionar si usar BrowserStack o un controlador local
    use_browserstack = st.checkbox("Usar BrowserStack", value=True)

    if st.button("Abrir WhatsApp Web"):
        open_whatsapp_web(use_browserstack=use_browserstack)

if __name__ == "__main__":
    main()

