import json, streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="ChangeFinder 💰", page_icon="💰")
st.title("💰 ChangeFinder - Find or Give Small Change Nearby")

# --- Google Sheets Setup ---
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds_dict = st.secrets["google"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open the sheet
sheet = client.open("changefinder_data").sheet1

# Load data into pandas DataFrame
data = sheet.get_all_records()
df = pd.DataFrame(data)

# --- Streamlit UI ---
st.subheader("Post Your Request")
mode = st.radio("What do you want to do?", ["I have change", "I need change"])
amount = st.number_input("Amount (₹)", min_value=5, step=5)
details = st.text_input("Details (example: ₹10 coins, ₹20 notes)")
name = st.text_input("Your Name")

if st.button("Post"):
    sheet.append_row([mode, amount, details, name])
    st.success("✅ Your request has been saved to Google Sheets!")

st.divider()
st.subheader("🔍 Current Requests")

if not df.empty:
    st.dataframe(df)
else:
    st.info("No posts yet. Be the first to add one!")
