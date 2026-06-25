import pandas as pd
import numpy as np
import random
import unicodedata
import re
import openpyxl

def normalizar_pais(valor):
    if pd.isna(valor):
        return np.nan
    v = str(valor).strip()           
    v = v.title()                   
    return v

def filtrar_pais_nacimiento(df):
    conteo = df['pais_nacimiento'].value_counts()
    paises_validos = conteo[conteo >= 5].index
    df['pais_nacimiento'] = df['pais_nacimiento'].where(
        df['pais_nacimiento'].isin(paises_validos), other='Otro'
    )
    return df

def normalizar_idioma(valor):
    if pd.isna(valor):
        return np.nan
    v = str(valor).strip().lower()
    
    # Español / Castellano
    if any(x in v for x in ['español', 'castellano', 'espa']):
        return 'Español / Castellano'
    # Guaraní
    if 'guarani' in v or 'guaraní' in v or 'guaranu' in v:
        return 'Guaraní'
    # Quechua
    if 'quechua' in v or 'kichua' in v:
        return 'Quechua'
    # Aymara
    if 'aymara' in v or 'ayamara' in v or 'áyáman' in v:
        return 'Aymara'
    # Creole
    if 'creole' in v or 'criollo' in v or 'creol' in v or 'kreyol' in v:
        return 'Creole haitiano'
    # Wolof
    if 'wolof' in v or 'wilof' in v or 'wollof' in v:
        return 'Wolof'
    # Wayuunaiki
    if 'wayuu' in v or 'wayu' in v:
        return 'Wayuunaiki'
    # Neerlandés
    if 'neerland' in v or 'holland' in v or 'hollandes' in v:
        return 'Neerlandés'
    # Alemán
    if 'alem' in v:
        return 'Alemán'
    # Ruso
    if v in ['ruso', 'ruso ']:
        return 'Ruso'
    # Italiano
    if 'italian' in v:
        return 'Italiano'
    # Portugués
    if 'portugu' in v:
        return 'Portugués'
    # Francés
    if 'franc' in v:
        return 'Francés'
    # Inglés
    if 'ingl' in v:
        return 'Inglés'
    # Árabe
    if 'arab' in v or 'arabe' in v or 'darija' in v:
        return 'Árabe'
    # Chino
    if 'chin' in v or '\u4e2d\u6587' in v or '琉球' in v:
        return 'Chino'
    # Catalán
    if 'catal' in v:
        return 'Catalán'
    # Gallego
    if 'gallego' in v:
        return 'Gallego'
    # Turco
    if 'turco' in v:
        return 'Turco'
    # Sueco
    if 'sueco' in v:
        return 'Sueco'
    # Armenio
    if 'armenio' in v:
        return 'Armenio'
    # Búlgaro
    if 'bulgar' in v or 'búlgar' in v:
        return 'Búlgaro'
    # Griego
    if 'grieg' in v or 'griega' in v or 'griego' in v:
        return 'Griego'
    # Serbio
    if 'serbio' in v:
        return 'Serbio'
    # Esloveno
    if 'esloveno' in v:
        return 'Esloveno'
    # Punjabi
    if 'punjabi' in v:
        return 'Punjabi'
    # Urdu
    if 'urdu' in v:
        return 'Urdu'
    # Hindi
    if 'hindi' in v:
        return 'Hindi'
    # Ucraniano
    if 'ucraniano' in v or 'ucrani' in v:
        return 'Ucraniano'
    # Lingala
    if 'lingala' in v:
        return 'Lingala'
    # Persa
    if 'persa' in v:
        return 'Persa'
    # Lituano
    if 'lituano' in v:
        return 'Lituano'
    # Polaco
    if 'polaco' in v:
        return 'Polaco'
    # Kabyle
    if 'kabyle' in v:
        return 'Kabyle'
    # Mapuche
    if 'mapuche' in v or 'mapuzungun' in v:
        return 'Mapuche (Mapuzungun)'
    # Twi / Akan
    if v in ['twi', 'akan']:
        return 'Twi / Akan'
    # Serere
    if 'serere' in v or 'serrere' in v or 'sérère' in v:
        return 'Serere'
    # Toucouleur
    if 'toucouleur' in v:
        return 'Toucouleur'
    if v in ['no se', 'no sé', 'kaf']:
        return np.nan

    return str(valor).strip().title()

def resolver_idioma(row, col_principal, col_otro, valor_otro):
    principal = row[col_principal]
    if principal == valor_otro:
        return normalizar_idioma(row[col_otro])
    return normalizar_idioma(principal)

def filtrar_por_frecuencia(df, col, minimo=5):
    conteo = df[col].value_counts()
    validos = conteo[conteo >= minimo].index
    df[col] = df[col].where(df[col].isin(validos), other='Otro')
    return df

def mapear_hijos_2023(row):
    tiene_hijos = row["q29_hijos_num"]
    arg = row["q30_hijos_arg"]
    ext = row["q30_hijos_exterior"]
    
    def valido(x):
        return x if (pd.notna(x) and x >= 0) else np.nan
    
    arg_v = valido(arg)
    ext_v = valido(ext)
      
    if tiene_hijos == "No":
        return "No, no tengo hijos"
    
    if tiene_hijos == "Si":
        tiene_arg = pd.notna(arg_v) and arg_v > 0
        tiene_ext = pd.notna(ext_v) and ext_v > 0
        
        if tiene_arg and tiene_ext:
            return "Sí, algunos nacidos en Argentina y otros/as en otro país"
        elif tiene_arg:
            return "Sí, nacidos en Argentina"
        elif tiene_ext:
            return "Sí, nacidos en otro país"
        else:
            return "---" #TODO: Analizar si seria mejor crear una variable "Prefiero no responder"
    
    return np.nan


def run_etl():
    df_2020 = pd.read_csv('data/raw/ENMA_2020.csv', sep=';')
    df_2023 = pd.read_csv('data/raw/ENMA_2023.csv', sep=';', low_memory=False)

    df_2020.rename(columns={'Id': 'ID'}, inplace=True)
    
    #EDAD
    df_2020['edad_agrupada'] = pd.cut(df_2020['q2_edad'], bins=[0, 17, 29, 44, 64, 10000], labels=['0-17', '18-29', '30-44', '45-64', '65+'])
    df_2020.drop(columns=['q2_edad'], inplace=True)

    df_2023['edad_agrupada'] = pd.cut(df_2023['q2_edad'], bins=[0, 17, 29, 44, 64, 10000], labels=['0-17', '18-29', '30-44', '45-64', '65+'])
    df_2023.drop(columns=['q2_edad'], inplace=True)
    df_2023.drop(columns=['edad_agrup'], inplace=True)

    #NACIONALIDAD
    df_2020['pais_nacimiento'] = np.where(df_2020['q3_pais'] == 'Otro (especifique)', df_2020['q3_otro'], df_2020['q3_pais'])
    df_2020.replace({'pais_nacimiento': {'Holanda': 'Países Bajos'}}, inplace=True)
    df_2020['pais_nacimiento'] = df_2020['pais_nacimiento'].apply(normalizar_pais)

    df_2020['pais_nacimiento_var'] = df_2020['q3_pais']
    df_2020.replace({'pais_nacimiento_var': {'Otro (especifique)': 'Otro'}}, inplace=True)

    df_2020.drop(columns=['q3_pais', 'q3_otro', 'nacionalidad_c'], inplace=True)

    df_2023['pais_nacimiento'] = np.where(df_2023['q3_pais_nacimiento'] == 'Otro', df_2023['q3_pais_otro'], df_2023['q3_pais_nacimiento'])
    df_2023['pais_nacimiento'] = df_2023['pais_nacimiento'].apply(normalizar_pais)
    df_2023.replace({'pais_nacimiento': {'Usa': 'Estados Unidos', 'Ee.Uu.': 'Estados Unidos', 'Estados Unidos De América': 'Estados Unidos', 'Estados Unidos Mexicanos': 'México', 'Hondurqwy': 'Honduras', 'Eeuu': 'Estados Unidos', 'Los Estados Unidos': 'Estados Unidos', 'Hungria pero soy Venezolana': 'Hungría', 'Costa Rics': 'Costa Rica', 'Mexico': 'México', 'El salvador': 'El Salvador'}}, inplace=True)
    
    df_2023['pais_nacimiento_var'] = df_2023['q3_pais_nacimiento']

    df_2023.drop(columns=["q3_pais_nacimiento", "q3_pais_otro"], inplace=True)

    df_2020 = filtrar_pais_nacimiento(df_2020)
    df_2023 = filtrar_pais_nacimiento(df_2023)

    conteo_2020 = df_2020['pais_nacimiento_var'].value_counts()
    conteo_2023 = df_2023['pais_nacimiento_var'].value_counts()

    conteo_total = conteo_2020.add(conteo_2023, fill_value=0)
    conteo_total = conteo_total.drop(labels='Otro', errors='ignore')
    top9 = conteo_total.nlargest(9).index.tolist()

    if 'China' not in top9:
        top9 = top9[:-1] + ['China']  # saca el último, agrega China

    df_2020['pais_nacimiento_var'] = df_2020['pais_nacimiento_var'].where(
        df_2020['pais_nacimiento_var'].isin(top9), other='Otro'
    )
    df_2023['pais_nacimiento_var'] = df_2023['pais_nacimiento_var'].where(
        df_2023['pais_nacimiento_var'].isin(top9), other='Otro'
    )

    #GENERO
    df_2020["genero_agrup"] = np.where(df_2020['q1_genero'] == 'Mujer', df_2020['q1_genero'], np.where(df_2020['q1_genero'] == 'Hombre', 'Varón', np.where(df_2020['q1_genero'] == 'No quiere informar', 'Prefiero no responder', 'Otro género')))
    df_2020.drop(columns=['q1_genero', 'Genero_i'], inplace=True)
    df_2023.drop(columns=['q4_genero'], inplace=True)

    #IDIOMA
    df_2020['idioma'] = df_2020.apply(lambda r: resolver_idioma(r, 'q5_idioma', 'q5_otro', 'Otro (especifique)'), axis=1)
    df_2023['idioma'] = df_2023.apply(lambda r: resolver_idioma(r, 'q6_idioma', 'q6_otro', 'Otro'), axis=1)
    
    df_2020 = filtrar_por_frecuencia(df_2020, 'idioma')
    df_2023 = filtrar_por_frecuencia(df_2023, 'idioma')

    conteo_total = (df_2020['idioma'].value_counts().add(df_2023['idioma'].value_counts(), fill_value=0)    )
    conteo_total = conteo_total.drop(labels='Otro', errors='ignore')
    top7 = conteo_total.nlargest(7).index.tolist()

    df_2020['idioma_var'] = df_2020['idioma'].where(df_2020['idioma'].isin(top7), other='Otro')
    df_2023['idioma_var'] = df_2023['idioma'].where(df_2023['idioma'].isin(top7), other='Otro')


    #DESCENDENCIA
    df_2020["descendencia"] = df_2020['q4_descendientes']
    df_2020.replace({'descendencia': {'Asiático/a o descendiente de asiático/a.':'Descendencia Asiática', np.nan: 'Ninguna de las anteriores', 'Indígena o descendiente de pueblos indígenas u originarios': 'Descendencia Indígena', 'Afrodescendiente, africano o afroargentino/a': 'Afrodescendiente'}}, inplace=True)
    df_2020.drop(columns=['q4_descendientes'], inplace=True)

    df_2023["descendencia"] = np.where(df_2023['q5_descendencia_afro'] == 1, 'Afrodescendiente',np.where(df_2023['q5_descendencia_indigena'] == 1, 'Descendencia Indígena', np.where(df_2023['q5_descendencia_asiatica'] == 1, 'Descendencia Asiática', 'Ninguna de las anteriores')))
    df_2023.drop(columns=['q5_descendencia_afro', 'q5_descendencia_indigena', 'q5_descendencia_asiatica', 'q5_descendencia_ninguno', 'q5_descendencia_otro'], inplace=True)

    # REGION

    PARTIDOS_AMBA = {
        "tigre", "san fernando", "san isidro", "vicente lopez", "vicente lópez",
        "general san martin", "general san martín", "gral san martin", "gral. san martín",
        "tres de febrero", "hurlingham", "ituzaingo", "ituzaingó",
        "moron", "la matanza", "merlo", "moreno",
        "jose c paz", "josé c paz", "jose c. paz", "josé c. paz",
        "malvinas argentinas", "san miguel",
        "avellaneda", "lanus", "lanús", "quilmes", "berazategui",
        "florencio varela", "almirante brown", "lomas de zamora",
        "esteban echeverria", "esteban echeverría", "ezeiza",
    }

    PROVINCIA_A_REGION = {
        "Ciudad de Buenos Aires (CABA)": "AMBA",
        # Buenos Aires (Provincia) → se resuelve aparte
        "Córdoba":           "Región Pampeana",
        "Santa Fe":          "Región Pampeana",
        "Entre Ríos":        "Región Pampeana",
        "La Pampa":          "Región Pampeana",
        "Mendoza":           "Cuyo",
        "San Juan":          "Cuyo",
        "San Luis":          "Cuyo",
        "Río Negro":         "Patagonia",
        "Neuquén":           "Patagonia",
        "Chubut":            "Patagonia",
        "Santa Cruz":        "Patagonia",
        "Tierra del Fuego, Antártida e Islas del Atlántico Sur": "Patagonia",
        "Misiones":          "NEA",
        "Chaco":             "NEA",
        "Corrientes":        "NEA",
        "Formosa":           "NEA",
        "Salta":             "NOA",
        "Jujuy":             "NOA",
        "Tucumán":           "NOA",
        "Santiago del Estero": "NOA",
        "Catamarca":         "NOA",
        "La Rioja":          "NOA",
    }

    def normalize(text: str) -> str:
        if not isinstance(text, str):
            return ""
        text = text.lower().strip()
        text = unicodedata.normalize("NFD", text)
        text = "".join(c for c in text if unicodedata.category(c) != "Mn")
        text = re.sub(r"[.\-_]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def is_amba_localidad(localidad: str) -> bool:
        n = normalize(localidad)
        return any(
            n == p or n in p or p in n
            for p in PARTIDOS_AMBA  # ya están normalizados en el set
        )

    def get_region(provincia: str, localidad: str) -> str | None:
        if provincia == "Buenos Aires (Provincia)":
            return "AMBA" if is_amba_localidad(localidad) else "Región Pampeana"
        return PROVINCIA_A_REGION.get(provincia)
    
    df_2020["region"] = df_2020.apply(lambda r: get_region(r["q7_provincia_res"], r["q8_localidad"]), axis=1)
    df_2020.drop(columns=['q7_provincia_res', 'q8_localidad'], inplace=True)

    df_2023['region'] = df_2023['region_amba_agrup']
    df_2023.drop(columns=['region_amba_agrup', 'q8_provincia_res', 'q9_localidad', 'q10_barrio'], inplace=True)

    #VIVIO EN OTRA PROVINCIA
    df_2020.rename(columns={'q9_otra_provincia': 'vivio_otra_provincia'}, inplace=True)
    df_2023.rename(columns={'q11_otra_provincia': 'vivio_otra_provincia'}, inplace=True)

    #MUDANZA
    # print(df_2020['q5_mudanza'].value_counts())
    # print(df_2023['q15_mudanza'].value_counts())
    # print(df_2023['q16_mudanza_lugar'].value_counts())

    #TIEMPO DE RESIDENCIA
    df_2020["periodo_residencia"] = df_2020['tiempo_i']
    df_2020["migracion_reciente"] = np.where(df_2020['q10_anios_res'] == 'Entre 1 y 2 años', 'si', np.where(df_2020['q10_anios_res'] == 'Menos de 1 año', 'si', 'no'))
    df_2020.drop(columns=['q10_anios_res', 'tiempo_i'], inplace=True)

    df_2023["periodo_residencia"] = df_2023['tiempo_residencia_agrup'].replace({'2 10 años o +': 'Más de 10 años', '1 De 6 a 9 años': 'Entre 5 y 9 años', '0 Hasta 5 años': 'Hasta 5 años'})
    df_2023["migracion_reciente"] = np.where(df_2023['q13_anio_llegada'] == 2022, 'si', np.where(df_2023['q13_anio_llegada'] == 2021, 'si', np.where(df_2023['q13_anio_llegada'] == 2023, 'si', 'no')))
    df_2023.drop(columns=['q13_anio_llegada','tiempo_residencia_agrup'], inplace=True)

    #MOTIVO MIGRATORIO
    df_2020["motivo_estudios_nuevas_experiencias"] = np.where((df_2020['q11_motivos_estudio'] == 'Para estudiar') | (df_2020['q11_motivos_experiencias'] == 'Para tener nuevas experiencias'), 1, 0)
    df_2020["motivo_mejor_trabajo"] = np.where(df_2020['q11_motivos_trabajo'] == 'Por trabajo', 1, 0)
    df_2020["motivo_violencias_persecuciones"] = np.where((df_2020['q11_motivos_discriminacion'] == 'Por violencia y/o discriminación (racismo, pertenencia étnica, de género)') | (df_2020['q11_motivos_violencias'] == 'Por violencias y/o persecuciones políticas'), 1, 0)
    df_2020["motivo_necesidades_basicas"] = np.where((df_2020['q11_motivos_salud'] == 'Por problemas de salud (para tratamiento)') | (df_2020['q11_motivos_sit_economica'] == "Por la situación económica/no podía cubrir mis necesidades básicas"), 1, 0)
    df_2020["motivo_familiar"] = np.where((df_2020['q11_motivos_familia'] == 'Para reencontrarme con mi familia') | (df_2020['q11_motivos_proyecto_otro'] == 'Para acompañar el proyecto de trabajo o estudio de otro/a'),1,0)
    df_2020.rename(columns={'q11_motivos_otros': 'motivo_otro'}, inplace=True)

    df_2020.drop(columns=['q11_motivos_proyecto_otro','q11_motivos_familia','q11_motivos_estudio', 'q11_motivos_experiencias', 'q11_motivos_trabajo', 'q11_motivos_discriminacion', 'q11_motivos_violencias', 'q11_motivos_salud', 'q11_motivos_sit_economica'], inplace=True)
    detalle = df_2023["q14_motivos_otros_detalle"].fillna('').str.lower()

    df_2023["motivo_estudios_nuevas_experiencias"] = np.where((df_2023['q14_motivos_estudio'] == 1) | (df_2023['q14_motivos_nuevas_experiencias'] == 1), 1, 0)
    df_2023['motivo_estudios_nuevas_experiencias'] = np.where(
        (df_2023['motivo_estudios_nuevas_experiencias'] == 1) |
        detalle.str.contains(
            'estudi|doctorado|seminar|jesuita|religios|intercambio|cultura|viajar|experiencia|idioma',
            regex=True
        ),
        1, 0
    )
    df_2023['motivo_mejor_trabajo'] = np.where(
        (df_2023['q14_motivos_mejor_trabajo'] == 1) |
        detalle.str.contains(
            'trabajo|laboral|empresa|expatri|designación|startup|camionero',
            regex=True
        ),
        1, 0
    )
    df_2023["motivo_violencias_persecuciones"] = np.where((df_2023['q14_motivos_violencia_genero'] == 1) | (df_2023['q14_motivos_orientacion_sexual'] == 1) | (df_2023['q14_motivos_persecucion'] == 1), 1, 0)
    df_2023['motivo_violencias_persecuciones'] = np.where(
        (df_2023['motivo_violencias_persecuciones'] == 1) |
        detalle.str.contains(
            'violencia|guerra|dictadura|chavismo|terrorismo|persec|xenofobia|inseguridad|comunismo',
            regex=True
        ),
        1, 0
    )
    df_2023["motivo_necesidades_basicas"] = np.where((df_2023['q14_motivos_salud'] == 1) | (df_2023['q14_motivos_necesidades_basicas'] == 1), 1, 0)
    df_2023["motivo_familiar"] = np.where(
        (df_2023['q14_motivos_reunificacion'] == 1) |
        (df_2023['q14_motivos_acompañar_otrx'] == 1) |
        (detalle.str.contains(
            'amor|pareja|novio|novia|espos|marid|casa|matrimonio|familia|padre|madre|hijo|me trajeron|menor|conyuge',
            regex=True
        )),
        1,0)
    df_2023["motivos_habitat"] = df_2023['q14_motivos_habitat']

    df_2023['motivo_necesidades_basicas'] = np.where(
        (df_2023['motivo_necesidades_basicas'] == 1) |
        detalle.str.contains(
            'calidad de vida|escasez|servicios|inflación|econom|salud|cáncer|comida|futuro mejor',
            regex=True
        ),
        1, 0
    )
    df_2023["motivo_otro"] = np.where(
        (df_2023["motivo_estudios_nuevas_experiencias"] == 0) &
        (df_2023["motivo_mejor_trabajo"] == 0) &
        (df_2023["motivo_violencias_persecuciones"] == 0) &
        (df_2023["motivo_necesidades_basicas"] == 0) &
        (df_2023["motivo_familiar"] == 0) &
        (df_2023["motivos_habitat"] == 0),
        1,
        0
    )
    df_2023.drop(columns=['q14_motivos_otros', 'q14_motivos_otros_detalle','q14_motivos','q14_motivos_estudio', 'q14_motivos_nuevas_experiencias', 'q14_motivos_mejor_trabajo', 'q14_motivos_violencia_genero', 'q14_motivos_orientacion_sexual', 'q14_motivos_persecucion', 'q14_motivos_salud', 'q14_motivos_necesidades_basicas', 'q14_motivos_reunificacion', 'q14_motivos_acompañar_otrx', 'q14_motivos_habitat'], inplace=True)

    #HIJOS
    df_2020["hijos"] = df_2020['q19_hijes']
    df_2020.drop(columns=['q19_hijes'], inplace=True)

    df_2023["hijos"] = df_2023.apply(mapear_hijos_2023, axis=1)
    df_2023.drop(columns=['q31_hijos_menores_exterior', 'q30_hijos_exterior', 'q30_hijos_arg', 'q29_hijos_num'], inplace=True)
    # print(df_2023['hijos'].value_counts())

    # SITUACION DOCUMENTAL 
    df_2020['dni_tenencia'] = (df_2020['q13_sit_docu'].str.contains('Tengo DNI', na=False).map({True: 'Si', False: 'No'}))
    df_2020.drop(columns=['q13_sit_docu'], inplace=True)

    df_2023["dni_tenencia"] = df_2023['q17_dni_tenencia']
    df_2023.drop(columns=['q17_dni_tenencia', 'q18_dni_situacion', 'q19_situacion_documentaria'], inplace=True)

    #DIFICULTAD DNI
    dificultad_cols = {
        'q21_dni_dificultad_turnos':               'Sí, no pude sacar turno o me lo postergaron',
        'q21_dni_dificultad_demora':               'Sí, no pude sacar turno o me lo postergaron',
        'q21_dni_dificultad_costo':                'Sí, por dificultades económicas',
        'q21_dni_dificultad_documentacion_origen': 'Sí, me falta documentación de mi país de origen para completar el trámite',
        'q21_dni_dificultad_falta_info':           'Sí, no sé cómo iniciar el trámite (no entiendo el idioma, etc.)',
        'q21_dni_dificultad_internet':             'Sí, no tengo internet o herramientas para hacerlo (teléfono, computadora, etc.)',
        'q21_dni_dificultad_identidad_genero':     'Otro (especifique)',
        'q21_dni_dificultad_otros':                'Otro (especifique)',
    } 

    def resolver_dificultad_2023(row):
        if row['q20_dni_dificultad_binaria'] == 'No':
            return 'No, no he tenido dificultades'

        if row['q20_dni_dificultad_binaria'] == 'Prefiero no responder':
            return 'Prefiero no responder'

        for col, categoria in dificultad_cols.items():
            if row.get(col) == 1.0:
                return categoria

        return 'Prefiero no responder'

    df_2023['dni_dificultad'] = df_2023.apply(resolver_dificultad_2023, axis=1)

    df_2020['dni_dificultad'] = df_2020['q14_problemas_docu'].replace({
        np.nan: 'Prefiero no responder'
    })
    df_2020['dni_dificultad'] = df_2020['dni_dificultad'].replace({
        'Sí, no cumplo con los requisitos para regularizarme': 'Otro (especifique)',
        'Sí, no sé usar el sistema online para el trámite (RADEX)': 'Sí, no tengo internet o herramientas para hacerlo (teléfono, computadora, etc.)'
    })

    df_2020.drop(columns=['q14_problemas_docu'], inplace=True)
    df_2023.drop(columns=list(dificultad_cols.keys()) + ['q20_dni_dificultad_binaria'], inplace=True)

    #PREGUNTAS SOLO UN AÑO
    df_2023.drop(columns=['q12_modo_ingreso'], inplace=True)
    
    #PREGUNTAS ELIMINADAS
    #nivel castellano
    df_2020.drop(columns=['q6_nivel_castellano'], inplace=True)
    df_2023.drop(columns=['q7_nivel_castellano'], inplace=True)

    #naturalizacion
    df_2020.drop(columns=['q16_naturalizacion'], inplace=True)
    df_2023.drop(columns=['q25_naturalizacion'], inplace=True)

    #pandemia
    df_2020.drop(columns=['q23_continuidad_mail'], inplace=True)
    df_2020.drop(columns=['q23_continuidad_zoom'], inplace=True)
    df_2020.drop(columns=['q23_continuidad_radio'], inplace=True)
    df_2020.drop(columns=['q23_continuidad_tv'], inplace=True)
    df_2020.drop(columns=['q23_continuidad_plataforma'], inplace=True)
    df_2020.drop(columns=['q23_continuidad_telefono'], inplace=True)
    df_2020.drop(columns=['q23_continuidad_cuadernillosdig'], inplace=True)
    df_2020.drop(columns=['q23_continuidad_cuadernillos'], inplace=True)
    df_2020.drop(columns=['q23_continuidad_presencial'], inplace=True)
    df_2020.drop(columns=['q23_continuidad_redes'], inplace=True)
    df_2020.drop(columns=['q23_continuidad_telfijo'], inplace=True)
    df_2020.drop(columns=['q23_continuidad_otro'], inplace=True)

    print("ETL completado con éxito.")
    print(" ")

    solo_2020 = set(df_2020.columns) - set(df_2023.columns)
    solo_2023 = set(df_2023.columns) - set(df_2020.columns)

    print(f"Columnas en 2020 que no están en 2023: {len(solo_2020)}")
    print(f"Columnas en 2023 que no están en 2020: {len(solo_2023)}")
    print(f"Total : {len(solo_2020) + len(solo_2023)}")

    solo_una = list(solo_2020 | solo_2023)

    if solo_una:
        print(f"Columna elegida aleatoriamente: {random.choice(solo_una)}")
    else:
        print("No hay columnas exclusivas; ambos DataFrames tienen las mismas columnas.")

if __name__ == "__main__":
    run_etl()