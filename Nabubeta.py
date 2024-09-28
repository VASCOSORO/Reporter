from selenium.common.exceptions import WebDriverException

def login_smarti(username, password):
    # Configurar opciones de Chrome para modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # Deshabilitar el uso de GPU en headless mode
    chrome_options.add_argument("--window-size=1920x1080")  # Configurar tamaño de ventana
    chrome_options.add_argument("--disable-extensions")  # Deshabilitar extensiones del navegador

    # Inicializar el controlador de Selenium
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Navegar a la página de inicio de sesión
        driver.get("https://smartycart.com.ar/users/login")
        time.sleep(3)  # Esperar a que la página cargue

        # Encontrar los campos de usuario y contraseña e ingresar las credenciales
        user_field = driver.find_element(By.ID, "username")  # Ajusta el selector según la página
        pass_field = driver.find_element(By.ID, "password")  # Ajusta el selector según la página

        user_field.send_keys(username)
        pass_field.send_keys(password)

        # Enviar el formulario
        pass_field.submit()
        time.sleep(5)  # Esperar a que el inicio de sesión se procese

        # Verificar si el inicio de sesión fue exitoso
        if "dashboard" in driver.current_url.lower():
            return True, "Inicio de sesión exitoso."
        else:
            return False, "Fallo al iniciar sesión. Verifica tus credenciales."

    except WebDriverException as e:
        return False, f"Error al iniciar WebDriver: {str(e)}"
    finally:
        driver.quit()
