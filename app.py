import streamlit as st
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os


load_dotenv()

st.title('Upload and Merge Patient and Responsible Party Files')

st.write("Upload the Patient and Responsible Party files (both files are required).")

uploaded_files = st.file_uploader("Choose the Patient and Responsible Party files", type=["xlsx"], accept_multiple_files=True)

def connect_to_db():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    return conn

# Function to insert data into the database
def insert_into_db(df):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    # Insert each row of the DataFrame into the table
    for index, row in df.iterrows():
        sql = """INSERT INTO pacientes_responsables 
                 (nombre_paciente, apellido_paciente, diagnostico, responsable, parentesco) 
                 VALUES (%s, %s, %s, %s, %s)"""
        values = (row['Nombre Paciente'], row['Apellido Paciente'], row['Diagnóstico'], row['Responsable'], row['Parentesco'])
        cursor.execute(sql, values)

    conn.commit()
    cursor.close()
    conn.close()

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

        if st.button('Save to Database'):
            insert_into_db(df_final)
            st.success('Data successfully saved to the database.')

     
        

    except Exception as e:
        st.error(f"Error processing the Excel files: {e}")

else:
    st.warning("Please upload exactly two Excel files.")