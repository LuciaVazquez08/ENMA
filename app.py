import streamlit as st

from data_utils import load_data, sidebar_filters
from enma_palette import inject_fonts
from views import (
    discriminacion_violencia,
    documentacion,
    educacion,
    familia_hogar_vivienda,
    identidad_lenguas,
    participacion,
    salud,
    sociodemografico,
    trabajo,
    trayectoria_migratoria,
)

st.set_page_config(
    page_title="ENMA - Tablero",
    page_icon="🌎",
    layout="wide",
)
inject_fonts()

df = load_data()
st.session_state["df_filtrado"] = sidebar_filters(df)

paginas = [
    st.Page(sociodemografico.render, title="Sociodemográfico", icon="🧑‍🤝‍🧑", url_path="sociodemografico", default=True),
    st.Page(identidad_lenguas.render, title="Identidad y lenguas", icon="🌐", url_path="identidad-y-lenguas"),
    st.Page(trayectoria_migratoria.render, title="Trayectoria migratoria", icon="🧭", url_path="trayectoria-migratoria"),
    st.Page(documentacion.render, title="Documentación y asilo", icon="🪪", url_path="documentacion-y-asilo"),
    st.Page(familia_hogar_vivienda.render, title="Familia, hogar y vivienda", icon="🏠", url_path="familia-hogar-y-vivienda"),
    st.Page(educacion.render, title="Educación", icon="🎓", url_path="educacion"),
    st.Page(trabajo.render, title="Trabajo y economía", icon="💼", url_path="trabajo-y-economia"),
    st.Page(salud.render, title="Salud", icon="🏥", url_path="salud"),
    st.Page(discriminacion_violencia.render, title="Discriminación y violencia", icon="⚠️", url_path="discriminacion-y-violencia"),
    st.Page(participacion.render, title="Participación y percepción", icon="🗳️", url_path="participacion-y-percepcion"),
]

navegacion = st.navigation(paginas)
navegacion.run()
