import streamlit as st
import requests

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

if st.button("Descargar CSV"):
    contenido_csv = descargar_csv()
