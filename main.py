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
st.header('Powered by Joseo20')

with st.expander('Instrucciones de uso'):
    st.markdown("""
Reemplaza las BANDERAs encontradas en el archivo de CONTENIDO con las palabras claves del archivo KEYWORDS con correspondencia de líneas 1:1

Se espera:

- Un archivo CONTENIDO con un texto por línea que puede tener una BANDERA que será sustituida
- Un archivo KEYWORDS con una palabra clave por línea que será sustituida por la BANDERA del archivo CONTENIDO

Genera:

- Un archivo REEMPLAZADO con los textos de CONTENIDO pero las BANDERAS sustituidas por las KEYWORDS, línea a línea
    """)


st.subheader('File input')

st.caption('Make sure that the contents and keywords file have the same number of lines. If one is longer, the extra files from the longer will be ignored.')

contents_file = st.file_uploader(label='Contents', type=['txt','csv','xlsx'], key='contents_file_uploader', help='Upload the CONTENTS file, with one post per line')
# Previsualización file
if contents_file is not None:
    content = StringIO(contents_file.getvalue().decode("utf-8")).read().splitlines()
    dfContent = pd.DataFrame(content, columns=["RAW"])
    with st.expander('Inspect your contents file:'):
        st.table(dfContent.head())

keywords_file = st.file_uploader(label='Keywords', type=['txt','csv','xlsx'], key='kws_file_uploader', help='Upload the KEYWORDS file, with one keyword per line')
# Previsualización file
if keywords_file is not None:
    keywords = StringIO(keywords_file.getvalue().decode("utf-8")).read().splitlines()
    dfKeywords = pd.DataFrame(keywords, columns=["RAW"])
    with st.expander('Inspect your keywords file:'):
        st.table(dfKeywords.head())

st.subheader('Keywords flag')
FLAG = st.text_input('Set your desired flag', value='%&AAA%&', key='flag_input', help='Sets the flag, i.e., string to be replaced on the content file.')

st.markdown("---")

st.subheader('Replacer')
replace_flags_btn = st.button('Replace flags')
if replace_flags_btn:

    dfContent['REPLACED'] = dfContent.apply(lambda x: replace_flag(x, FLAG, keywords), axis=1)
    # Previsualización OUTPUT
    if dfContent['REPLACED'] is not None:
        st.image('https://emoji-uc.akamaized.net/orig/f7/f1297a3ffec34c824497db1e3ca51f.png', width=30)
        with st.expander('Inspect your output file:'):
            st.table(dfContent["REPLACED"].head())

    # Save file
    csv = convert_df(dfContent['REPLACED'])

    download = st.download_button(label='👉 Download replaced contents file', data=csv, mime='text/csv')

    if download is not None:
        st.balloons()





