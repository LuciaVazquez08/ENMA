import streamlit as st

from data_utils import load_data

COLUMNAS_USADAS = {
    "Año",
    "pais_nacimiento",
    "pais_nacimiento_var",
    "genero_agrup",
    "edad_agrupada",
    "region",
    "descendencia",
    "nivel_educativo_agrup",
    "periodo_residencia",
}


def render():
    st.title("Control de variables")
    st.caption(
        "Variables del dataset que todavía no se usan en ninguna pestaña del tablero: "
        "opciones disponibles y cantidad de casos (en valor absoluto) de cada una."
    )

    df = load_data()
    columnas_no_usadas = [c for c in df.columns if c not in COLUMNAS_USADAS]

    st.caption(f"{len(columnas_no_usadas)} de {len(df.columns)} columnas del dataset sin usar todavía.")

    for columna in columnas_no_usadas:
        conteo = df[columna].value_counts(dropna=False).reset_index()
        conteo.columns = ["Opción", "Cantidad"]
        conteo["Opción"] = conteo["Opción"].fillna("Sin dato").astype(str)
        with st.expander(f"{columna} ({len(conteo)} opciones)"):
            st.dataframe(conteo, use_container_width=True, hide_index=True)
