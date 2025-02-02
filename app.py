from google.colab import auth
auth.authenticate_user()

import gspread
from google.auth import default

creds, _ = default()
gc = gspread.authorize(creds)

import pandas as pd

# Load the Google Sheet
sheet_id = "16bGYXkbWJXJrzqup1fAPRRWWaNjA5GYMgfVwp9Y5K9c"  # Replace with your Sheet ID
sh = gc.open_by_key(sheet_id)
worksheet = sh.get_worksheet(0)  # First sheet

# Convert to DataFrame
data = worksheet.get_all_records()
df = pd.DataFrame(data)

%%writefile app.py
import streamlit as st
import pandas as pd
import gspread
from google.auth import default
from streamlit_extras.dataframe_explorer import dataframe_explorer

# Authenticate and connect to Google Sheets
creds, _ = default()
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
st.markdown("🚀 **Be a part of this free initiative!** Submit your decision: [📋 Submit Here](https://forms.gle/XKziTqc26pj5GeUE9) ❤️")

