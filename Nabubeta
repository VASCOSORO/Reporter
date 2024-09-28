from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Configurar el acceso a BrowserStack (Reemplazá con tus credenciales)
BROWSERSTACK_USERNAME = 'your_browserstack_username'
BROWSERSTACK_ACCESS_KEY = 'your_browserstack_access_key'

# URL para acceder a BrowserStack
url = f"http://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# Configurar opciones para el navegador remoto
desired_cap = {
    'browser': 'Chrome',
    'browser_version': 'latest',
    'os': 'Windows',
    'os_version': '10',
    'name': 'Test on Smarti',  # Nombre de la prueba
    'build': 'Selenium Colab Test',  # Nombre del build
}

# Conectar a BrowserStack
driver = webdriver.Remote(
    command_executor=url,
    desired_capabilities=desired_cap
)

# Navegar a la página de inicio de sesión de Smarti
driver.get('https://smartycart.com.ar/users/login')

# Esperar a que la página cargue
driver.implicitly_wait(10)

# Buscar los campos de usuario y contraseña (reemplazá con los IDs correctos)
username = driver.find_element(By.NAME, 'username')
password = driver.find_element(By.NAME, 'password')

# Ingresar las credenciales
username.send_keys('Soop')
password.send_keys('74108520')

# Enviar el formulario
login_button = driver.find_element(By.NAME, 'login')
login_button.click()

# Continuar interactuando con la página
