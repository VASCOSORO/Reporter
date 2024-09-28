import streamlit as st
import requests

# URL del sitio donde querés extraer la información
url_products = "https://smartycart.com.ar/Products/index/clearFilters:true"

# Cookies obtenidas de tu navegador
cookies = {
    'CAKEPHP': '281cqqb5nkt2a3amtpajaqb00i',  # Valor de CAKEPHP
    'cf_clearance': '9uatTmP0qGq3WCEtksagMkdqmEBfrIrqN1VOpd0UBkY-1727551385-1.2.1.1-34TP718Ov8NPELTlLBC7YTUeusGgXUvtSbZfw.Pu_LK0f9wo.jvxw3mIGqPIEfHoOsG.3bmpObm7ibSuC_L_pvZj9pnZ4g6gPNGvdtPuWIzai4hJ0QphWo3.s.nLPC7d8e5FrfVaJOgF6.OZzmeCswsDMn13YUzg1l9Gngr2dL8wARE7WOINbhscU5CxWdKsD573XXHLfJ7JogvT65YpQdMj8wMZUASIijuAXHpg.MS9E1eqp5PTaaN80mszVP4_ZzlYBtE4GHRrblzI38_28IUI5z6ZYw9cz4CS0zOzjLJE8yR.f8IOw4tsa_d5USFdaGJgbm9OHA_Sm30QnFbNBDB.It9GHYprZcaL1Kpq7svMqCDawYHJNQsknTJomeL2B_BFJSzTgvzLa_zSfTxYsQ'  # Valor de cf_clearance
}

# Función para descargar el CSV
def descargar_csv():
    # Realizamos la solicitud a la página con las cookies de la sesión
    response = requests.get(url_products, cookies=cookies)

    if response.status_code == 200:
        st.write("Productos obtenidos correctamente")
        # Guardar el contenido en un archivo CSV
        with open("productos.csv", "wb") as f:
            f.write(response.content)
        st.write("CSV descargado exitosamente.")
    else:
        st.write(f"Error al obtener los productos: {response.status_code}")

# Interfaz de Streamlit
st.title("Automatización SmartyCart")

if st.button("Descargar CSV"):
    descargar_csv()
