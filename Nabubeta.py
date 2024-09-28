import requests
from bs4 import BeautifulSoup
import streamlit as st

# URL de la página
url = "https://smartycart.com.ar/Products/index/clearFilters:true"

# Cookies necesarias
cookies = {
    'CAKEPHP': 'tu_cookie',
    'cf_clearance': 'tu_cookie',
}

# Función para obtener y seleccionar todos los productos
def obtener_datos():
    response = requests.get(url, cookies=cookies)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Paso 1: Activar la casilla para seleccionar los primeros 20 productos
        casilla_primera = soup.find('input', {'class': 'chkSelectAllResults', 'type': 'checkbox'})
        if casilla_primera:
            # Paso 2: Encontrar el enlace que selecciona todos los productos
            select_all_link = soup.find('a', text=lambda t: "Seleccionar los" in t and "productos de la búsqueda" in t)
            if select_all_link:
                # Confirmar selección de los 1813 productos
                st.write(f"Enlace encontrado: {select_all_link['href']}")
                select_response = requests.get(f"https://smartycart.com.ar{select_all_link['href']}", cookies=cookies)
                if select_response.status_code == 200:
                    return 1813  # Número de productos seleccionados
                else:
                    st.write("Error al seleccionar todos los productos.")
            else:
                st.write("No se encontró el enlace para seleccionar todos los productos.")
        else:
            st.write("No se encontró la casilla para seleccionar los productos.")
    else:
        st.write(f"Error en la solicitud inicial: {response.status_code}")
        return 0

# Función para descargar el CSV
def descargar_csv():
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

# Interfaz de Streamlit
st.title("Automatización SmartyCart")

if st.button("Obtener Datos"):
    cantidad_productos = obtener_datos()
    if cantidad_productos > 0:
        st.write(f"Se seleccionaron {cantidad_productos} productos.")
        if st.button("Descargar CSV"):
            descargar_csv()
    else:
        st.write("No se encontraron productos para descargar.")
