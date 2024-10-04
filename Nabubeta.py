# ===========================
# ======= DALEEEE DALEEEE ===== 2 ww
# ====== paso el lead ========

import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager

# Credenciales de BrowserStack
BROWSERSTACK_USERNAME = 'vascorepo_7EFbsI'
BROWSERSTACK_ACCESS_KEY = 'keVzqBxcjsyMJxYzUG9V'

# Credenciales de LeadSales
LEADSALES_EMAIL = "jsanovsky@gmail.com"
LEADSALES_PASSWORD = "Pasteur39"

# URLs de los sitios
LEADSALES_LOGIN_URL = "https://leadsales.services/login"
LEADSALES_ANALYTICS_URL = "https://leadsales.services/workspace/analytics"  # URL de la página de análisis de Leadsales a visitar después de iniciar sesión

def login_selenium_leadsales(email, password, use_browserstack=True):
    """
    Función para iniciar sesión en LeadSales con Selenium, con opción para usar BrowserStack o un controlador local.
    """
    try:
        if use_browserstack:
            # Configuración de BrowserStack con 'options'
            options = webdriver.ChromeOptions()
            options.set_capability('bstack:options', {
                'os': 'Windows',
                'osVersion': '10',
                'buildName': 'Build LeadSales',
                'sessionName': 'LeadSales Login Test',
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

        # Navegar a la página de LeadSales
        driver.get(LEADSALES_LOGIN_URL)
        st.write("Página de LeadSales cargada.")

        # Esperar a que la página cargue
        wait = WebDriverWait(driver, 10)

        # Encontrar y rellenar los campos de usuario y contraseña
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'email')))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, 'Password')))

        username_field.send_keys(email)
        password_field.send_keys(password)

        # Enviar el formulario
        password_field.send_keys(Keys.RETURN)

        # Esperar un poco para que procese el inicio de sesión
        time.sleep(5)

        # Verificar si el inicio de sesión fue exitoso
        if driver.current_url != LEADSALES_LOGIN_URL:
            st.success("Inicio de sesión exitoso en LeadSales.")

            # Navegar a la sección específica (Analytics)
            driver.get(LEADSALES_ANALYTICS_URL)
            st.write("Navegando a la sección de Análisis de LeadSales.")

            # Esperar a que la página cargue
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Extraer datos específicos de la sección de Análisis
            analytics_data = []
            try:
                # Suponiendo que los datos de análisis están en elementos con la clase 'analytics-card'
                cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'analytics-card')))
                for card in cards:
                    title = card.find_element(By.CLASS_NAME, 'analytics-card-title').text
                    value = card.find_element(By.CLASS_NAME, 'analytics-card-value').text
                    analytics_data.append({"title": title, "value": value})
            except Exception as e:
                st.error(f"Error al extraer los datos de análisis: {e}")

            # Mostrar los datos extraídos en Streamlit
            if analytics_data:
                st.write("Datos de Análisis de LeadSales:")
                for data in analytics_data:
                    st.write(f"{data['title']}: {data['value']}")
            else:
                st.write("No se encontraron datos de análisis.")

            # Tomar la captura de pantalla
            screenshot = driver.get_screenshot_as_png()
            return driver, screenshot
        else:
            st.error("Error al iniciar sesión en LeadSales. Verifica tus credenciales.")
            driver.quit()
            return None, None
    except Exception as e:
        st.error(f"Error durante el inicio de sesión en LeadSales: {e}")
        return None, None

def display_screenshot(screenshot):
    """
    Función para mostrar la captura de pantalla en Streamlit.
    """
    st.image(screenshot, caption='Captura de pantalla después del inicio de sesión', use_column_width=True)

def main():
    st.set_page_config(page_title="Automatización de Reportes", layout="wide")
    st.title("Automatización de Reportes - LeadSales")

    st.write("""
    Este aplicativo permite iniciar sesión en [LeadSales](https://leadsales.services/login) utilizando Selenium y navegar a una sección específica.
    ""
    )

    # Seleccionar si usar BrowserStack o un controlador local
    use_browserstack = st.checkbox("Usar BrowserStack", value=True)

    # Iniciar sesión en LeadSales
    if st.button("Iniciar Sesión en LeadSales"):
        driver, screenshot = login_selenium_leadsales(LEADSALES_EMAIL, LEADSALES_PASSWORD, use_browserstack=use_browserstack)
        if driver:
            st.success("Inicio de sesión exitoso en LeadSales y navegación a la sección deseada.")
            if screenshot:
                display_screenshot(screenshot)
            driver.quit()

if __name__ == "__main__":
    main()
