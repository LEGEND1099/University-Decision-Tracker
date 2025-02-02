import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from streamlit_extras.dataframe_explorer import dataframe_explorer

# Define the service account credentials JSON directly in the code (replace with your own)
service_account_info = {
    "type": "service_account",
    "project_id": "university-decision-tracker",
    "private_key_id": "b8796598f410bde3a370c6d72531e145dcf7d06c",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDIOJ8K5frYCPva
Fl2yp/Pr6S0zel6K0R3wE6Xu0+A4p8PFHerjqcj3ic7h69rkZws5R4g7uw8McPZg
M/ZGv2c5jEmxY2J4qhviEOIVK4jhDYyfLxhIkJmowK1v1SO+oc3ph6w6tX1cTog2
DHikyLFU53pJyirVr2Vl4Q1l2RmJeTpWcVQ8vDyoDv5LQb4JLxhc9/hRDaJ8wHYm
6oLsOjjWRRQJU41JbaFrbd3WwwilL1N8HyjA9b2yESKbdIaH23KJ9VQYjJIlN0v8
X7Y7gAhzdCEH/82iL5/bB/a39Oc3EWYX1VpVM325JUZiKlxwIj+txrhHfZUpTcwz
QVURzl+VAgMBAAECggEANyEIAZszR1qp5fG0mOWPzwwkKwFtmLFdmeX/EVR7b34Z
9GN5cngkYqwqL6CeY7dPqtTcWP33dciAvhpwnChFht3uyI4B5hGIneViKswS40y0
xHvWJtzRwlpTJvC759hrdvqpXHzuaIUjEia67TxpP2SBEmI9CxtBQx0FcF6nnmcq
OA1Vl4EoB6CAwalg8s/erGP2siNw+3GTmcAJdksqnpMqW2zf+UaO9arPe8jhBGty
EAMhv9aFaftALXqMWbmn0zlmPDhF+ZkraAKc/nQSv1HPg7/OOCj+U5/iiqWPKVpK
Gr0gRUsTXVpCkDZFlrO/XhTEttP30FJR8z1dA1/UXQKBgQD+YMHvcZpuo/WHH2wA
xg+tuMM21qzRTmfiYW/y9T0Xmp8dYPl1SgmUnTBQJUuWhjHKOvh5YkpVZOGYWrZH
D7QRnWG7doURG4T+yRBcDoXMSlvxcImgQNMoKwsZBwK1/hpwKmpzQohUndlNmddX
iItcD4OGc1o6pDFR5Kx6Bb5vowKBgQDJf3WETfdD6TjiPICf0mz7nLh6g7Jq6QzK
fC5R2boOWqY/inFlnHkkc6WnXOFII2G3Vzy0zcMfxY0HTH5hrxW49GPoc/jNxp6U
9/sN8wYMuod4GzzkP4IyiE3tPxwwExunwgufzpE3xQhNW3Uc3c9Z93BBMtp3laMM
qezwCHYHZwKBgQDOSnF8WUjAST8ooZbY2caFP70wj8/+vfMJZ7N9+NvedIptLOOg
9rXmS8OOe3BdVd6y/jfbWJanwfQhtg70egux7UwA1xD62rJ0XWJjBXQERJljp7w0
td2ISb/qQAE2zidqpztE1cPxu0Eq6YP1fMpnkj07n/igbd+BZk1pd5cEuQKBgDDl
FAAx5yF8k4gahF/D8RwxUHayRHY67RapgZftDH/1MUhT8OZmTOMyiO0O1b/qjgiu
S5XYJFQuXOV7g2Ny2AOUkjXTBnnwi4S8lBgzc7FdBgh4G5OLca2Pc9FxMgbcbCaO
KMHznzt4PWaAHfAORwWezIeVrnu8PN+S0GMCuplbAoGBAJhLVHAIZeIMlkgKb4MW
GQv+XZ3bYNmLEy1VnyNP23vYTGmwM44XsgcWTZeIZ+v21CyihJCw0BPd4Il2fsLZ
01R9MhdwN+hhu5DhVz03iR/644VVRiNgs9hPyGcLpCEgEn4R4pLqu1nrUMJzESbT
c52wYdPQZD9pgUnLMzCi36jx
-----END PRIVATE KEY-----\n""",
    "client_email": "sheets-access-service-account@university-decision-tracker.iam.gserviceaccount.com",
    "client_id": "100595815732394570343",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sheets-access-service-account%40university-decision-tracker.iam.gserviceaccount.com"
}

# Authenticate using the service account credentials
creds = Credentials.from_service_account_info(service_account_info)

# Authorize gspread
gc = gspread.authorize(creds)

# Load Google Sheet
sheet_id = "16bGYXkbWJXJrzqup1fAPRRWWaNjA5GYMgfVwp9Y5K9c"  # Replace with your actual Sheet ID
sh = gc.open_by_key(sheet_id)
worksheet = sh.get_worksheet(0)  # First sheet
data = worksheet.get_all_records()

# Convert to DataFrame
df = pd.DataFrame(data)

# Hide "Timestamp" and "Email" columns
columns_to_hide = ["Timestamp", "Email"]  # "column" refers to the email column
df = df.drop(columns=[col for col in columns_to_hide if col in df.columns], errors="ignore")

# Convert "Applied Date" & "Result Date" to YYYY-MM-DD format (ensures no time)
date_columns = ["Applied Date", "Result Date"]
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d")  # Only date

# Ensure "CGPA" is treated as a number/text, not a timestamp
if "CGPA" in df.columns:
    df["CGPA"] = df["CGPA"].astype(str)  # Convert CGPA to string to prevent timestamp issues

# Streamlit UI
st.set_page_config(page_title="🎓 University Decision Tracker", page_icon="📚", layout="wide")

# Title & Description
st.title("🎓 University Decision Tracker 📊")
st.markdown("""
🚀 **Your Ultimate University Decision Tracker!** 🚀  
💡 Tired of expensive decision-tracking tools? This **100% free** alternative lets you track where students are getting admitted—**without spending a dime!** 💰❌  
🌍 See which universities are accepting students, filter by country, and check real-time trends! 📊  
🎯 **Want to contribute?** Submit your decision here: [📋 Submit Your Decision](https://forms.gle/XKziTqc26pj5GeUE9)  
""")

st.markdown("---")

# Filters: Country & Admit/Reject
col1, col2 = st.columns(2)

with col1:
    selected_country = st.selectbox("🌎 Select Country", ["All"] + df["Country"].unique().tolist())
with col2:
    selected_status = st.selectbox("📑 Select Admission Status", ["All", "Admitted", "Rejected"])

# Filter data based on selections
filtered_df = df.copy()
if selected_country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == selected_country]
if selected_status != "All":
    filtered_df = filtered_df[filtered_df["Result"] == selected_status]

# Display Filtered Data
st.subheader(f"Filtered Data ({filtered_df.shape[0]} entries)")
dataframe_explorer(filtered_df)

# Display Data
st.dataframe(filtered_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("🚀 **Be a part of this free initiative!** Submit your decision: [📋 Submit Here](https://forms.gle/XKziTqc26pj5GeUE9) ❤️")
