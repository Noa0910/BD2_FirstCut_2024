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

       
     
        

    except Exception as e:
        st.error(f"Error processing the Excel files: {e}")

else:
    st.warning("Please upload exactly two Excel files.")