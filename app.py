import gspread
import json
import os
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials
from streamlit_extras.dataframe_explorer import dataframe_explorer

# Fetch secrets using os.getenv() directly
type_secret = os.getenv('type')
project_id = os.getenv('project_id')
private_key_id = os.getenv('private_key_id')
private_key = os.getenv('private_key')
client_email = os.getenv('client_email')
client_id = os.getenv('client_id')
auth_uri = os.getenv('auth_uri')
token_uri = os.getenv('token_uri')
auth_provider_x509_cert_url = os.getenv('auth_provider_x509_cert_url')
client_x509_cert_url = os.getenv('client_x509_cert_url')
universe_domain = os.getenv('universe_domain')

# Create a dictionary from the secrets
creds_dict = {
    "type": type_secret,
    "project_id": project_id,
    "private_key_id": private_key_id,
    "private_key": private_key,
    "client_email": client_email,
    "client_id": client_id,
    "auth_uri": auth_uri,
    "token_uri": token_uri,
    "auth_provider_x509_cert_url": auth_provider_x509_cert_url,
    "client_x509_cert_url": client_x509_cert_url,
    "universe_domain": universe_domain
}

# Define the scope for Google Sheets API
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# Authenticate using the service account dictionary
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

# Authorize gspread with the credentials
gc = gspread.authorize(creds)

# Open the Google Sheet by its ID (replace with your actual sheet ID)
sheet_id = "16bGYXkbWJXJrzqup1fAPRRWWaNjA5GYMgfVwp9Y5K9c"  # Replace with your actual Sheet ID
sh = gc.open_by_key(sheet_id)

# Select the first sheet (you can change this to any sheet you want to access)
worksheet = sh.get_worksheet(0)

# Fetch all records and load them into a pandas DataFrame
data = worksheet.get_all_records()
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

if "Years of Experience" in df.columns:
    df["Years of Experience"] = df["Years of Experience"].astype(str)  # Ensure it stays as a string

if "English Proficiency Score" in df.columns:
    df["English Proficiency Score"] = df["English Proficiency Score"].astype(str)  # Ensure it stays as a string


# Streamlit UI
st.set_page_config(page_title="🎓 University Decision Tracker", page_icon="📚", layout="wide")

# Title & Description
st.title("🎓 University Decision Tracker 📊")
st.markdown("""
🚀 **Track University Decisions, No Fuss!** 🚀  
💡 A **100% free** way to see where students are getting in—no paywalls, no hassle.  
🌍 Filter by country, track real-time trends, and stay ahead! 📊  
🎯 **Got an update?** Share yours here: [📋 Submit Your Decision](https://forms.gle/XKziTqc26pj5GeUE9)  
""")  

st.markdown("---")

# Filters: Country & Admit/Reject
col1, col2 = st.columns(2)

with col1:
    selected_country = st.selectbox("🌎 Filter by Country", ["All"] + sorted(df["Country"].unique()))
with col2:
    selected_decision = st.selectbox("✅ Filter by Admit/Reject", ["All"] + sorted(df["Admit/Reject"].unique()))

# Apply Filters
filtered_df = df.copy()
if selected_country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == selected_country]
if selected_decision != "All":
    filtered_df = filtered_df[filtered_df["Admit/Reject"] == selected_decision]

# Searchable Table
st.markdown("### 🔍 Search & Explore")
filtered_df = dataframe_explorer(filtered_df, case=False)

# Display Data
st.dataframe(filtered_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("🚀 **Be a part of this free initiative!** Submit your decision at [📋 Submit Your Decision](https://forms.gle/XKziTqc26pj5GeUE9)")


# AdSense Integration
st.html("""
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3535666961610166"
     crossorigin="anonymous"></script>
""")
# st.markdown("Add placed")
