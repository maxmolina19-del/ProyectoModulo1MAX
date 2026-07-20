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

    #------------------------------
    # RESULTADO
    #------------------------------

    resultado = st.selectbox(
        "RESULTADO",
        [
            "DESCARTE",
            "BUENA",
            "FRAUDE",
            "PENDIENTE"
        ]
    )

    #====================================================
    # LÓGICA DEPENDIENTE DEL RESULTADO
    #====================================================

    if resultado == "DESCARTE":

        gestion = st.selectbox(
            "GESTIÓN",
            ["ANALISIS"],
            disabled=True
        )

        categoria = st.selectbox(
            "CATEGORÍA",
            ["NO APLICA"],
            disabled=True
        )

        subcategoria = st.selectbox(
            "SUB_CATEGORIA",
            ["NO APLICA"],
            disabled=True
        )

    elif resultado in ["BUENA", "FRAUDE"]:

        gestion = st.selectbox(
            "GESTIÓN",
            ["LLAMADA"],
            disabled=True
        )

        categoria = st.selectbox(
            "CATEGORÍA",
            ["CONTACTO EFECTIVO"],
            disabled=True
        )

        subcategoria = st.selectbox(
            "SUB_CATEGORIA",
            ["CONTACTO EFECTIVO"],
            disabled=True
        )

    elif resultado == "PENDIENTE":

        gestion = st.selectbox(
            "GESTIÓN",
            ["LLAMADA"],
            disabled=True
        )

        categoria = st.selectbox(
            "CATEGORÍA",
            ["CONTACTO NO EFECTIVO"],
            disabled=True
        )

        subcategoria = st.selectbox(
            "SUB_CATEGORIA",
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

    #====================================================
    # BOTÓN REGISTRAR
    #====================================================

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

            "RESULTADO": resultado,
            "GESTIÓN": gestion,
            "CATEGORÍA": categoria,
            "SUB_CATEGORIA": subcategoria,

            "ANALISIS_CASO": analisis

        }])

        if os.path.exists(ARCHIVO):

            datos = pd.read_csv(ARCHIVO)

            datos = pd.concat([datos, nuevo], ignore_index=True)

            datos.to_csv(ARCHIVO, index=False)

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
