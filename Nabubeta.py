import streamlit as st
import requests
from bs4 import BeautifulSoup

# URL para obtener los productos
url_products = "https://smartycart.com.ar/Products/index/clearFilters:true"
# URL para descargar el CSV
url_csv = "https://smartycart.com.ar/Products/export"

# Cookies obtenidas de tu navegador
cookies = {
    'CAKEPHP': '281cqqb5nkt2a3amtpajaqb00i',  # Valor de CAKEPHP
    'cf_clearance': '9uatTmP0qGq3WCEtksagMkdqmEBfrIrqN1VOpd0UBkY-1727551385-1.2.1.1-34TP718Ov8NPELTlLBC7YTUeusGgXUvtSbZfw.Pu_LK0f9wo.jvxw3mIGqPIEfHoOsG.3bmpObm7ibSuC_L_pvZj9pnZ4g6gPNGvdtPuWIzai4hJ0QphWo3.s.nLPC7d8e5FrfVaJOgF6.OZzmeCswsDMn13YUzg1l9Gngr2dL8wARE7WOINbhscU5CxWdKsD573XXHLfJ7JogvT65YpQdMj8wMZUASIijuAXHpg.MS9E1eqp5PTaaN80mszVP4_ZzlYBtE4GHRrblzI38_28IUI5z6ZYw9cz4CS0zOzjLJE8yR.f8IOw4tsa_d5USFdaGJgbm9OHA_Sm30QnFbNBDB.It9GHYprZcaL1Kpq7svMqCDawYHJNQsknTJomeL2B_BFJSzTgvzLa_zSfTxYsQ'  # Valor de cf_clearance
}

# Headers adicionales para simular un navegador real
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Referer': 'https://smartycart.com.ar/Products/index/clearFilters:true'
}

# Función para obtener los productos y seleccionar todos
def obtener_datos():
    # Realizamos la solicitud para obtener la página de productos
    response = requests.get(url_products, cookies=cookies, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Imprimimos el HTML por si necesitamos inspeccionar los elementos
        st.write(soup.prettify())
        
        # Buscar el enlace que selecciona todos los productos
        select_all_link = soup.find('a', href=True, text=lambda t: "productos de la búsqueda" in t)
        
        if select_all_link:
            select_all_url = "https://smartycart.com.ar" + select_all_link['href']
            # Simular clic en "Seleccionar todos los productos"
            response_select_all = requests.get(select_all_url, cookies=cookies, headers=headers)
            
            if response_select_all.status_code == 200:
                st.write("Se seleccionaron todos los productos correctamente.")
                # Devolvemos la cantidad de productos seleccionados
                cantidad_productos = select_all_link.text.split()[2]  # Captura el número de productos seleccionados
                return cantidad_productos
            else:
                st.write("Error al seleccionar todos los productos.")
                return None
        else:
            st.write("No se encontró el enlace para seleccionar todos los productos.")
            return None
    else:
        st.write(f"Error al obtener los productos: {response.status_code}")
        return None

# Función para descargar el CSV
def descargar_csv():
    # Realizamos la solicitud a la URL directa del CSV con cookies y headers
    response = requests.get(url_csv, cookies=cookies, headers=headers)

    if response.status_code == 200:
        st.write("Productos obtenidos correctamente")
        return response.content  # Devuelve el contenido del CSV para la descarga
    else:
        st.write(f"Error al descargar el CSV: {response.status_code}")
        return None

# Interfaz de Streamlit
st.title("Automatización SmartyCart")

if st.button("Obtener Datos"):
    cantidad_productos = obtener_datos()
    
    if cantidad_productos:
        st.write(f"Se obtuvieron {cantidad_productos} productos.")
        if st.button("Descargar CSV"):
            contenido_csv = descargar_csv()
            
            if contenido_csv:
                # Botón para descargar el archivo CSV
                st.download_button(
                    label="Descargar CSV",
                    data=contenido_csv,
                    file_name="productos.csv",
                    mime="text/csv"
                )
