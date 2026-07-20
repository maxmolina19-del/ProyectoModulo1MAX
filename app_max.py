import streamlit as st
import pandas as pd
import os
from datetime import datetime
import getpass

#------------------------------------------------------
# CONFIGURACIÓN
#------------------------------------------------------

st.set_page_config(
    page_title="Prevención y Gestión de Fraudes",
    page_icon="🛡️",
    layout="wide"
)

ARCHIVO = "registro_fraudes.csv"

#-------------------------------------------------------
# TÍTULO PRINCIPAL
#-------------------------------------------------------

st.title("Prevención y gestión de fraudes")

st.image("titulo.png", use_container_width=True)

#-------------------------------------------------------
# BARRA LATERAL
#-------------------------------------------------------

st.sidebar.title("Parámetros")

st.sidebar.image("Banco.png", use_container_width=True)

modulo = st.sidebar.selectbox(
    "Seleccione el módulo",
    ["Home","Registro","Detalle"]
)

#=======================================================
# HOME
#=======================================================

if modulo == "Home":

    st.markdown("### Bienvenido")

    st.info(
        "Protegemos cada transacción mediante el monitoreo inteligente y la detección oportuna del fraude."
    )

#=======================================================
# REGISTRO
#=======================================================

elif modulo == "Registro":

    st.header("Registro de Gestión")

    dni = st.text_input("DNI_CLIENTE")

    celular = st.text_input("CELULAR")

    analisis = st.text_area("ANALISIS DE CASO")

    contacto = st.selectbox(
        "TIPO DE CONTACTO",
        [
            "CONTACTO EFECTIVO",
            "CONTACTO NO EFECTIVO"
        ]
    )

    if contacto == "CONTACTO EFECTIVO":

        resultado = st.selectbox(
            "RESULTADO",
            [
                "BUENA",
                "FRAUDE"
            ]
        )

    else:

        resultado = st.selectbox(
            "MOTIVO",
            [
                "NO CONTESTA",
                "TELÉFONO APAGADO",
                "NÚMERO EQUIVOCADO",
                "BUZÓN DE VOZ",
                "RECHAZA LA LLAMADA",
                "SIN COBERTURA",
                "OTRO MOTIVO"
            ]
        )

    if st.button("REGISTRAR", use_container_width=True):

        fecha = datetime.now().strftime("%d/%m/%Y")

        hora = datetime.now().strftime("%H:%M:%S")

        usuario = getpass.getuser()

        nuevo = pd.DataFrame([{

            "FECHA": fecha,

            "HORA": hora,

            "USUARIO": usuario,

            "DNI_CLIENTE": dni,

            "CELULAR": celular,

            "TIPO_CONTACTO": contacto,

            "RESULTADO": resultado,

            "ANALISIS_CASO": analisis

        }])

        if os.path.exists(ARCHIVO):

            existente = pd.read_csv(ARCHIVO)

            existente = pd.concat([existente, nuevo], ignore_index=True)

            existente.to_csv(ARCHIVO, index=False)

        else:

            nuevo.to_csv(ARCHIVO, index=False)

        st.success("Registro almacenado correctamente.")

#=======================================================
# DETALLE
#=======================================================

elif modulo == "Detalle":

    st.header("Detalle de registros")

    if os.path.exists(ARCHIVO):

        datos = pd.read_csv(ARCHIVO)

        st.dataframe(
            datos,
            use_container_width=True
        )

    else:

        st.warning("No existen registros.")
