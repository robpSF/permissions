import streamlit as st
import pandas as pd

# Function to load Excel file
def load_data(file):
    df = pd.read_excel(file)
    return df

# Function to update the DataFrame with new permissions
def update_permissions(df, new_permission):
    if new_permission not in df.columns:
        df[new_permission] = ""
    return df

st.title("Persona Permissions Management")

# Upload Excel file
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    df = load_data(uploaded_file)
    st.write("Original Data")
    st.dataframe(df)
    
    # Extracting required columns
    required_columns = ["Name", "Handle", "Faction", "Tags"]
    permissions_columns = [col for col in df.columns if col not in required_columns and col != "Permissions"]
    
    # Add a dropdown to filter by Faction
    faction_filter = st.selectbox("Select Faction", options=df["Faction"].unique())
    df_filtered = df[df["Faction"] == faction_filter]
    
    st.write(f"Filtered Data by Faction: {faction_filter}")
    
    # Displaying the table with checkmarks for permissions
    df_permissions = df_filtered[required_columns + permissions_columns]
    for perm in permissions_columns:
        df_permissions[perm] = df_permissions[perm].apply(lambda x: "✅" if x == 'x' else "")
    
    st.dataframe(df_permissions)
    
    # Add new permission
    new_permission = st.text_input("Add New Permission")
    if st.button("Add Permission"):
        df = update_permissions(df, new_permission)
        permissions_columns.append(new_permission)
        df_filtered = update_permissions(df_filtered, new_permission)  # Ensure new column is in filtered DataFrame
        st.success(f"Permission '{new_permission}' added.")
    
    # Update permission assignments
    for perm in permissions_columns:
        st.write(f"Manage Permission: {perm}")
        if perm not in df_filtered.columns:
            df_filtered[perm] = ''
        for i, row in df_filtered.iterrows():
            checked = st.checkbox(f"{row['Name']} ({row['Handle']})", value=(row[perm] == 'x'), key=f"{perm}_{i}")
            df.at[row.name, perm] = 'x' if checked else ''
    
    # Save updated DataFrame back to Excel
    if st.button("Save Updates"):
        df.to_excel("updated_persona_permissions.xlsx", index=False)
        st.success("Updates saved to 'updated_persona_permissions.xlsx'")

    # Download link for the updated file
    with open("updated_persona_permissions.xlsx", "rb") as file:
        btn = st.download_button(
            label="Download updated Excel file",
            data=file,
            file_name="updated_persona_permissions.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
