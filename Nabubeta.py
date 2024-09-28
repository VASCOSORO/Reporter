import streamlit as st
import requests

# URL del sitio donde querés extraer la información
url_products = "https://smartycart.com.ar/Products/index/clearFilters:true"

# Aquí van las cookies que copiaste del navegador (debes reemplazar los valores)
cookies = {
    'cookie_name_1': 'cookie_value_1',
    'cookie_name_2': 'cookie_value_2',
    # Continúa agregando las cookies necesarias
}

# Hacer la solicitud HTTP con las cookies de sesión
response = requests.get(url_products, cookies=cookies)

# Revisar la respuesta
if response.status_code == 200:
    st.write("Productos obtenidos correctamente")
    st.write(response.text)  # o response.json() si los datos son JSON
else:
    st.write(f"Error al obtener los productos: {response.status_code}")
