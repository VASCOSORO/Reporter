import requests
from bs4 import BeautifulSoup
import streamlit as st

# URL de la página de productos
url = "https://smartycart.com.ar/Products/index/clearFilters:true"

# Cookies necesarias
cookies = {
    'CAKEPHP': 'f7dis3hebde797gnj5k9vm9ocs',  # Cookie de sesión
    'cf_clearance': '5aCqoec_qC0Qya5RWjhAtPaYxP6JN5cBHOXDetMX4wU-1727556739-1.2.1.1-48R9USx.QP5yOVhnm8.SEO.J0P6ZQ5UdW4wA_1uLPfINBVeBZ.0epsHEV9wPWe8z4W5LPfJJO4mgC0EXh68WAWbcekgMiHHjFmSZT1KuoeXgzWhRXmEGFxBBQ8y2zHUeq6QZ3g44wPskPTMDGgN9nx58wR2.rheuZ_TN9sG4QAPRszf9CXcBmWGaMS__TZEsw6VXNhMexTNXKXocGu3DMb4ETEuIYzsOINZWRUMjukjy_XQvajof8PmSFhIhSV3RLGrAwBVHgH_zzwOi84YQ4eBhKVdoqdKLgxHH_V79zYFPEnCgBYepD9deIef2AAqrv0vPZ5lhFec344WIv9koll7EMUz01h17C37wt..gM1zBMZcY5dCgdQKSkqxVVkEAFojHJbL4bVsafQ4VgZoAng',  # Cookie de seguridad
}

# Función para obtener y seleccionar todos los productos
def obtener_datos():
    try:
        response = requests.get(url, cookies=cookies)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Imprimir todo el HTML de la página para verificar
            st.write("HTML recibido:")
            st.code(soup.prettify())  # Muestra el HTML completo en formato legible
            
            # Paso 1: Buscar y seleccionar el checkbox para seleccionar todos los productos
            st.write("Buscando la casilla de selección...")
            checkbox = soup.find('input', {'class': 'chkSelectAll'})
            
            if checkbox:
                st.write("Casilla encontrada.")
                return 1813  # Número de productos seleccionados (placeholder)
            else:
                st.write("No se encontró la casilla para seleccionar los productos.")
        else:
            st.write(f"Error en la solicitud inicial: {response.status_code}")
            return 0
    except Exception as e:
        st.write(f"Ocurrió un error: {str(e)}")
        return 0

# Función para descargar el CSV
def descargar_csv():
    try:
        # URL para descargar el CSV
        csv_url = "https://smartycart.com.ar/Products/export"
        
        # Solicitud para descargar el CSV
        response = requests.get(csv_url, cookies=cookies)
        if response.status_code == 200:
            # Guardar el archivo CSV
            with open("productos.csv", "wb") as f:
                f.write(response.content)
            st.write("CSV descargado exitosamente.")
            st.download_button('Descargar CSV', data=response.content, file_name='productos.csv')
        else:
            st.write(f"Error al descargar el CSV: {response.status_code}")
    except Exception as e:
        st.write(f"Ocurrió un error al descargar el CSV: {str(e)}")

# Interfaz de Streamlit
st.title("Automatización SmartyCart")

if st.button("Obtener Datos"):
    cantidad_productos = obtener_datos()
    
    # Verificar si cantidad_productos es un número válido
    if isinstance(cantidad_productos, int):
        if cantidad_productos > 0:
            st.write(f"Se seleccionaron {cantidad_productos} productos.")
            if st.button("Descargar CSV"):
                descargar_csv()
        else:
            st.write("No se encontraron productos para descargar.")
    else:
        st.write(f"Error: cantidad_productos no es un número válido. Valor recib
