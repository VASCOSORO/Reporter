import streamlit as st
import requests
from bs4 import BeautifulSoup

# URL del sitio donde queremos seleccionar todos los productos y descargar el CSV
url_products = "https://smartycart.com.ar/Products/index/clearFilters:true"
url_download_csv = "https://smartycart.com.ar/Products/export"

# Aquí van las cookies actualizadas que copiaste del navegador
cookies = {
    'CAKEPHP': '281cqqb5nkt2a3amtpajaqb00i',
    'cf_clearance': '9uatTmP0qGq3WCEtksagMkdqmEBfrIrqN1VOpd0UBkY-1727551385-1.2.1.1-34TP718Ov8NPELTlLBC7YTUeusGgXUvtSbZfw.Pu_LK0f9wo.jvxw3mIGqPIEfHoOsG.3bmpObm7ibSuC_L_pvZj9pnZ4g6gPNGvdtPuWIzai4hJ0QphWo3.s.nLPC7d8e5FrfVaJOgF6.OZzmeCswsDMn13YUzg1l9Gngr2dL8wARE7WOINbhscU5CxWdKsD573XXHLfJ7JogvT65YpQdMj8wMZUASIijuAXHpg.MS9E1eqp5PTaaN80mszVP4_ZzlYBtE4GHRrblzI38_28IUI5z6ZYw9cz4CS0zOzjLJE8yR.f8IOw4tsa_d5USFdaGJgbm9OHA_Sm30QnFbNBDB.It9GHYprZcaL1Kpq7svMqCDawYHJNQsknTJomeL2B_BFJSzTgvzLa_zSfTxYsQ'
}

def obtener_datos():
    # Hacer la solicitud HTTP para obtener el HTML de la página de productos
    response = requests.get(url_products, cookies=cookies)
    if response.status_code != 200:
        st.write(f"Error al obtener los productos: {response.status_code}")
        return 0

    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscar el enlace con la clase 'selectAll'
    select_all_link = soup.find('a', class_="selectAll")
    
    if select_all_link:
        st.write(f"Enlace para seleccionar todos los productos encontrado: {select_all_link['href']}")
        return 1813  # Número total de productos
    else:
        st.write("No se encontró el enlace para seleccionar todos los productos.")
        return 0

# Interfaz de usuario de Streamlit
st.title("Automatización SmartyCart")

if st.button("Obtener Datos"):
    cantidad_productos = obtener_datos()
    if cantidad_productos > 0:
        st.write(f"Se obtuvieron {cantidad_productos} productos.")

        # Botón de descarga CSV solo si los datos fueron obtenidos
        if st.button("Descargar CSV"):
            # Hacer la solicitud HTTP para descargar el CSV
            response = requests.get(url_download_csv, cookies=cookies)

            if response.status_code == 200:
                # Guardar el archivo CSV
                with open("productos.csv", "wb") as file:
                    file.write(response.content)
                st.write("CSV descargado exitosamente.")
            else:
                st.write(f"Error al descargar el CSV: {response.status_code}")
