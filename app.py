import streamlit as st
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os


load_dotenv()

st.title('Upload and Merge Patient and Responsible Party Files')

st.write("Upload the Patient and Responsible Party files (both files are required).")

uploaded_files = st.file_uploader("Choose the Patient and Responsible Party files", type=["xlsx"], accept_multiple_files=True)

if len(uploaded_files) == 2:
    try:
        file1 = uploaded_files[0]
        file2 = uploaded_files[1]

        df_pacientes = pd.read_excel(file1)
        df_responsables = pd.read_excel(file2)

        st.success('Both files were uploaded successfully!')

        st.write("Patients:")
        st.dataframe(df_pacientes)
        st.write("Responsible Parties:")
        st.dataframe(df_responsables)

        df_combined = pd.merge(df_pacientes, df_responsables, left_on="Responsable", right_on="Nombre", how="inner")

        df_final = df_combined[['Nombre_x', 'Apellido_x', 'Diagnóstico', 'Responsable', 'Parentesco']]
        df_final.columns = ['Patient Name','Patient Last Name', 'Diagnosis', 'Responsible', 'Relationship']

        st.write("Combined content:")
        st.dataframe(df_final)

     
        

    except Exception as e:
        st.error(f"Error processing the Excel files: {e}")

else:
    st.warning("Please upload exactly two Excel files.")