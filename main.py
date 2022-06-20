import streamlit as st
import pandas as pd
import os
from io import StringIO

def replace_flag(x, flag, keywords):
    return x[0].replace(flag, keywords[x.name])

@st.cache
def convert_df(df):
    return df.to_csv(index=False, header=None).encode('utf-8')

st.title('Flag Replacer')
st.header('Joseo20')

with st.expander('Instrucciones de uso'):
    st.markdown("""
Reemplaza las BANDERAs encontradas en el archivo de CONTENIDOS con las palabras claves del archivo KEYWORDS con correspondencia de líneas 1:1

Se espera:

- Un archivo CONTENIDOS con un texto por línea que puede tener una BANDERA que será sustituida
- Un archivo KEYWORDS con una palabra clave por línea que será sustituida por la BANDERA del archivo CONTENIDO

Genera:

- Un archivo REEMPLAZADO con los textos de CONTENIDOS pero las BANDERAS sustituidas por las KEYWORDS, línea a línea
    """)


st.subheader('Entrada de archivos')

st.caption('Asegúrate de que el archivo de CONTENIDO y KEYWORDS tiene el mismo número de líneas. Si uno de los dos archivos contiene mayor número de filas, las filas extra del archivo más largo serán descartadas.')

contents_file = st.file_uploader(label='Contenidos', type=['txt','csv','xlsx'], key='contents_file_uploader', help='Sube el archivo de CONTENIDOS, con un post por línea')
# Previsualización file
if contents_file is not None:
    content = StringIO(contents_file.getvalue().decode("utf-8")).read().splitlines()
    dfContent = pd.DataFrame(content, columns=["RAW"])
    with st.expander('Inspect your contents file:'):
        st.table(dfContent.head())

keywords_file = st.file_uploader(label='Keywords', type=['txt','csv','xlsx'], key='kws_file_uploader', help='Sube el archivo de KEYWORDS, con una keyword por línea')
# Previsualización file
if keywords_file is not None:
    keywords = StringIO(keywords_file.getvalue().decode("utf-8")).read().splitlines()
    dfKeywords = pd.DataFrame(keywords, columns=["RAW"])
    with st.expander('Inspect your keywords file:'):
        st.table(dfKeywords.head())

st.subheader('Bandera para las keywords')
FLAG = st.text_input('Escribe la bandera a utilizar', value='%&AAA%&', key='flag_input', help='Asigna la bandera, e.g., el string de caracteres a ser reemplazado en el archivo de contenidos.')

st.markdown("---")

st.subheader('Reemplazador')
replace_flags_btn = st.button('Reemplazar banderas por keywords')
if replace_flags_btn:

    if keywords_file is not None and contents_file is not None:
        dfContent['REPLACED'] = dfContent.apply(lambda x: replace_flag(x, FLAG, keywords), axis=1)
        # Previsualización OUTPUT
        if dfContent['REPLACED'] is not None:
            with st.expander('Inspect your output file:'):
                st.text('El orangotán cósmeco te bendice con un archivo con banderas reemplazadas'); st.image('https://emoji-uc.akamaized.net/orig/f7/f1297a3ffec34c824497db1e3ca51f.png', width=30)
                st.table(dfContent["REPLACED"].head())

        # Save file
        csv = convert_df(dfContent['REPLACED'])

        download = st.download_button(label='👉 Descarga el archivo de CONTENIDOS con los reemplazos efectuados', data=csv, mime='text/csv')
    else:
        if contents_file is None and keywords_file is not None:
            st.warning('⚠️ Falta el archivo de CONTENIDOS. Por favor, sube un archivo de CONTENIDOS válido.')
        elif keywords_file is None and contents_file is not None:
            st.warning('⚠️ Falta el archivo de KEYWORDS. Por favor, sube un archivo de KEYWORDS válido.')
        else:
            st.warning('⚠️ Hay un problema con los archivos. Por favor, sube un archivo de CONTENIDOS y otro de KEYWORDS.')
            





