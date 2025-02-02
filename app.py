import gspread
import json
import os
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials
from streamlit_extras.dataframe_explorer import dataframe_explorer

# Embed the service account credentials directly for testing purposes (remove in production)
service_account_json = '''
{
  "type": "service_account",
  "project_id": "university-decision-tracker",
  "private_key_id": "069c89895833a78cfaa737c6637d35657d6437a1",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDP96er3RnzwTdq\nm0pxK+nGA8SqTXLfnovaAXpT+LwyMKVngX0Bc6u65oV2hWktE9MCRNnvNwe4A9T4\nwovZe2NGbf06q/RX1xT6+DKN2CNlu8VyECO9CRVQVd/6CnrsOR/w5LANibdbRP7+\nMTkkEpRd/JqtcEVu1oKPfXz7chEY7a3zwsoAzzHqDLWhjILpeq3jbIndjO232Lsq\nBvn+cKnDrvrgCL4V1uAj5DZbkGkbLHbuhbKaMsZhxnLmcFiuoDn6wD8N0p1LwGbo\ndsXeg6a8TNurCdtI8ayj/92ZzBqZ3Ci4As6XOm+9/KxtB0ABo9v49L0gvkAxp9JZ\ngwkyrEPzAgMBAAECggEAG44hYcS4eRMrUA1GZktevLVoG/aKF3YO6rJSbojhCrdm\nWxoNoaEdanS7z1Hq9yWOylisFaWReMDNOa6xT/4oz76oFFuPUwo1BfHX5PJz8jlY\ndn4L9jKbZ9sRA7Tax6zj/guXBhwutsGkFbMY8p4hmXhsWDmtgXubrf5/DmP1PvuV\ns2nlLCincsPkEho27VtCEdhE+j3y4p3jGZ2KWPDUZv9un9DfA2AjRqLmEj6rrlYo\n8PBnmHjApIORIndSSmQj8bPj+PIIBgnw2SgVcKx4OpGxQZ0YngzDk8tU4vlzCmIx\n3CsuonymkXlhjwr/viAiGG7eI1rnvnbuAN85trgirQKBgQD8Kp8nLBFLN5rUXf7f\nAkguv70wUYNNZLQzdM1e6uRRZvTlG8A2dmtLi9qFyFGZCxYSt19dP+dCYdL0XUOx\n1ZoNVLP4t7zntWVseeIoVUCVHHfsB7DKUPBc5tJZfYrbo1QZ+/Y5aanaL6IVuKIW\njKOq9W2VUgGqY9UQ6aIHvNsuTQKBgQDTIQUThXUMygUR1ZhAqtQ7kMFh/jhwTEfA\n9df62LpetKyYAeJpdMk1UTvNOgcy2qhQsioirZ0DVgPs+LA4AcToa0RuZ/NGtNrP\n40EfLBMXUCV73wHpvV7aAQvUFXbbaPDqPal5BLmTgOHoC6hmb2rvtgIa0ITc30zt\nOPLeaKDbPwKBgBdPMUsDrc2QJEXBMpAWu+lmW+ydfE+pIWcoQtulRtmndLfA6vGd\n3KktElQPgkttVOsB/FS4VX4zYLap8Fn97rGQxNoW0eVxRSDT223zA3dFHGi7BUKO\nXMmZpJQVIMLQxDNqsQX5mHPMt2Tenk0LTw28hhapb/H6LHXVwt6IPJJ5AoGANYJu\n6O2wJtekxUpfVjR1qcscWBu4bi3HGc61OKxpP8uG2tfPbG7e+BZok7EbVfY5Joqh\nRzy9SLUqNYsqDmfUYhudsmXCMK9xrbKpNJ9VD1mOxoBU2crXGWWee9gc0asdNCEA\nrN1Xs1y85LTfr2aZsbtteSJUKi6mLpF6bIgUDL0CgYB5sUAKcO856nsqDEW7dERR\nuHM+Ukbaqeh7USdmwlz9Qi+zhsV8ltpiDGulRdxk1bsh/5YnZdXl3ZfsbJB2fnkq\nXIMivFBQb4xXDhlk1UUicl1o67jfk7MBBPudquWsZ6sev3BYmT//5Vtzt5W5gaSS\nzNr7CECuLICjuvbHgfnsBQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "sheets-access-service-account@university-decision-tracker.iam.gserviceaccount.com",
  "client_id": "100595815732394570343",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sheets-access-service-account%40university-decision-tracker.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
'''

# Convert the JSON string to a dictionary
creds_dict = json.loads(service_account_json)

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
