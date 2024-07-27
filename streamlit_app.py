import streamlit as st
import pandas as pd

def convert_to_columns(df):
    # Split the 'Permission' column into multiple columns
    permissions = df['Permission'].str.split(',', expand=True).stack().str.strip().unique()
    for perm in permissions:
        df[perm] = df['Permission'].apply(lambda x: 'x' if perm in x else '')
    return df.drop(columns=['Permission'])

# Streamlit App
st.title("Permission Converter")

mode = st.selectbox("Select Mode", ["Convert to Columns", "Convert Columns to Permissions"])

if mode == "Convert to Columns":
    st.header("Convert to Columns Mode")
    
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        
        if 'Permission' not in df.columns:
            st.error("The uploaded file does not contain a 'Permission' column.")
        else:
            st.write("Original Data")
            st.dataframe(df)
            
            converted_df = convert_to_columns(df)
            
            st.write("Converted Data")
            st.dataframe(converted_df)
            
            @st.cache
            def convert_df_to_excel(df):
                return df.to_excel(index=False, engine='xlsxwriter')
            
            excel_data = convert_df_to_excel(converted_df)
            st.download_button(
                label="Download Converted Data as Excel",
                data=excel_data,
                file_name='converted_permissions.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
