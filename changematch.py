import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")   

st.title("💰 ChangeFinder - Find or Give Small Change Nearby")

# CSV file to store change data
DATA_FILE = "change_data.csv"

# Load data if fikle exists, else create an empty DataFrame

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Type", "Amount", "Details", "Name"])

st.subheader("Post Your Request")

mode = st.radio("I want to:", ("Find Change", "Give Change"))
amount = st.number_input("Amount (in inr)", min_value=0.01, step=0.01, format="%.2f")
details = st.text_area("Details (e.g., location, time)", max_chars=200)
name = st.text_input("Your Name (optional)")

if st.button("Post"):
    new_row = {"Type": mode, "Amount": amount, "Details": details, "Name": name}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("✅ Your request has been saved!")

st.divider()
st.subheader("🔍 Current Requests")

if len(df) > 0:
    st.dataframe(df)
    st.markdown("### ❌ Terminate (Delete) a Request")
    delete_index = st.number_input("Enter the index of the request to delete", 
    min_value=0,
    max_value=len(df)-1,
    step=1  
)
    
    if st.button("Delete Request"):
        df = df.drop(delete_index).reset_index(drop=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("✅ Request deleted!")
    
else:
    st.info("No requests found. Be the first to post!")


