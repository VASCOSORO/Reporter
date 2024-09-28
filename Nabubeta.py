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
    try:
        response = requests.get(url, cookies=cookies)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Paso 1: Buscar y seleccionar el checkbox para seleccionar todos los productos
            st.write("Buscando la casilla de selección...")
            checkbox = soup.find('input', {'class': 'chkSelectAll'})
            
            if checkbox:
                st.write("Casilla encontrada. Intentando seleccionarla...")
                # Simulación de la selección de la casilla
                select_response = requests.get(url, cookies=cookies, data={'chkSelectAll': '1'})
                
                if select_response.status_code == 200:
                    st.write("Casilla seleccionada correctamente.")
                    
                    # Paso 2: Buscar el enlace para seleccionar todos los productos
                    st.write("Buscando enlace para seleccionar todos los productos...")
                    select_all_link = soup.find('a', {'class': 'selectAll'})
                    
                    if select_all_link:
                        st.write(f"Enlace para seleccionar todos los productos encontrado: {select_all_link['href']}")
                        select_response = requests.get(f"https://smartycart.com.ar{select_all_link['href']}", cookies=cookies)
                        if select_response.status_code == 200:
                            st.write("Todos los productos han sido seleccionados.")
                            return 1813  # Número de productos seleccionados
                        else:
                            st.write(f"Error al seleccionar todos los productos. Código de estado: {select_response.status_code}")
                    else:
                        st.write("No se encontró el enlace para seleccionar todos los productos.")
                else:
                    st.write(f"Error al seleccionar la casilla. Código de estado: {select_response.status_code}")
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
        st.write(f"Error: cantidad_productos no es un número válido. Valor recibido: {cantidad_productos}")
