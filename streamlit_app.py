import streamlit as st
import pandas as pd

# Function to process the file and update permissions
def update_permissions(df):
    # Identify the columns with 'x' marks
    permission_columns = df.columns[5:]  # Assuming permissions start from the 6th column
    for col in permission_columns:
        df[col] = df[col].apply(lambda x: col if x == 'x' else None)
    
    # Combine the permissions into the Permissions column
    df['Permissions'] = df[permission_columns].apply(lambda row: ', '.join(filter(None, row)), axis=1)
    return df

# Streamlit app
st.title("Permission Updater")

uploaded_file = st.file_uploader("Upload your Excel file", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Original Data:")
    st.write(df)
    
    st.write("Processed Data:")
    processed_df = update_permissions(df)
    st.write(processed_df)
    
    # Allow downloading the processed file
    @st.cache
    def convert_df(df):
        return df.to_excel(index=False)

    processed_file = convert_df(processed_df)
    
    st.download_button(
        label="Download Processed Data",
        data=processed_file,
        file_name="processed_permissions.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
