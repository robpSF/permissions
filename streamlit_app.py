import streamlit as st
import pandas as pd
import tempfile

def convert_to_columns(df):
    # Split the 'Permissions' column into multiple columns
    permissions = df['Permissions'].dropna().str.split(',', expand=True).stack().str.strip().unique()
    for perm in permissions:
        df[perm] = df['Permissions'].apply(lambda x: 'x' if pd.notna(x) and perm in x else '')
    return df.drop(columns=['Permissions']).fillna('')

def convert_columns_to_permissions(df):
    tags_index = df.columns.get_loc('Tags') + 1
    permission_cols = df.columns[tags_index:]
    
    df['Permissions'] = df.apply(lambda row: ', '.join([col for col in permission_cols if row[col] == 'x']), axis=1)
    df = df.drop(columns=permission_cols).fillna('')
    
    faction_index = df.columns.get_loc('Faction') + 1
    cols = df.columns.tolist()
    cols.insert(faction_index, cols.pop(cols.index('Permissions')))
    df = df[cols]
    
    return df

# Streamlit App
st.set_page_config(layout="wide")
st.title("Permission Converter")

mode = st.selectbox("Select Mode", ["Convert to Columns", "Convert Columns to Permissions"])

if mode == "Convert to Columns":
    st.header("Convert to Columns Mode")
    
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file).fillna('')
        
        if 'Permissions' not in df.columns:
            st.error("The uploaded file does not contain a 'Permissions' column.")
        else:
            st.write("Original Data")
            st.write(df)
            
            converted_df = convert_to_columns(df)
            
            st.write("Converted Data")
            st.write(converted_df)
            
            @st.cache
            def convert_df_to_excel(df):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                    with pd.ExcelWriter(tmp.name, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False)
                    return tmp.name
            
            excel_data = convert_df_to_excel(converted_df)
            with open(excel_data, 'rb') as f:
                st.download_button(
                    label="Download Converted Data as Excel",
                    data=f.read(),
                    file_name='converted_permissions.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )

elif mode == "Convert Columns to Permissions":
    st.header("Convert Columns to Permissions Mode")
    
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file).fillna('')
        
        if 'Tags' not in df.columns:
            st.error("The uploaded file does not contain a 'Tags' column.")
        else:
            st.write("Original Data")
            st.write(df)
            
            converted_df = convert_columns_to_permissions(df)
            
            st.write("Converted Data")
            st.write(converted_df)
            
            @st.cache
            def convert_df_to_excel(df):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                    with pd.ExcelWriter(tmp.name, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False)
                    return tmp.name
            
            excel_data = convert_df_to_excel(converted_df)
            with open(excel_data, 'rb') as f:
                st.download_button(
                    label="Download Converted Data as Excel",
                    data=f.read(),
                    file_name='converted_permissions.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
