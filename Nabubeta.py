import requests
from bs4 import BeautifulSoup
import streamlit as st

# URL de la página de productos
url = "https://smartycart.com.ar/Products/index/clearFilters:true"

# Cookies necesarias para mantener la sesión
cookies = {
    'CAKEPHP': 'f7dis3hebde797gnj5k9vm9ocs',
    'CakeCookie[lang]': 'es',
    'CakeCookie[remember_me_cookie]': 'Q2FrZQ==.AlIt6frdN4QUnIb3MqdrWtQKdYii/L2O+k/P+xZTXOT2fxeNDpgdPLFbmffkpXUR6q0WIhHoP9i69oFYAE3Y7HGm1uy+CTm1+5salzLW9/lnIzN2bd+lSoDhEPMRCao=',
    '_ga': 'GA1.1.1689468051.1724804957',
    '_ga_HCC7RPPQ8T': 'GS1.1.1727556736.9.1.1727556737.59.0.0',
    'cf_clearance': '5aCqoec_qC0Qya5RWjhAtPaYxP6JN5cBHOXDetMX4wU-1727556739-1.2.1.1-48R9USx.QP5yOVhnm8.SEO.J0P6ZQ5UdW4wA_1uLPfINBVeBZ.0epsHEV9wPWe8z4W5LPfJJO4mgC0EXh68WAWbcekgMiHHjFmSZT1KuoeXgzWhRXmEGFxBBQ8y2zHUeq6QZ3g44wPskPTMDGgN9nx58wR2.rheuZ_TN9sG4QAPRszf9CXcBmWGaMS__TZEsw6VXNhMexTNXKXocGu3DMb4ETEuIYzsOINZWRUMjukjy_XQvajof8PmSFhIhSV3RLGrAwBVHgH_zzwOi84YQ4eBhKVdoqdKLgxHH_V79zYFPEnCgBYepD9deIef2AAqrv0vPZ5lhFec344WIv9koll7EMUz01h17C37wt..gM1zBMZcY5dCgdQKSkqxVVkEAFojHJbL4bVsafQ4VgZoAng'
}

# Función para obtener y seleccionar todos los productos
def obtener_datos():
    try:
        response = requests.get(url, cookies=cookies)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            st.write("HTML recibido:")
            st.code(soup.prettify())  # Mostrar el HTML completo para debug

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
