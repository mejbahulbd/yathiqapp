import streamlit as st
import pandas as pd

SHEET_URL = "https://docs.google.com/spreadsheets/d/1YUkvJej2HehutG4sA0ybC8HtOgN81Z_BYIFFj-43uJM/export?format=csv"

st.title("👶 বেবি কেয়ার স্মার্ট POS")
barcode = st.text_input("বারকোড স্ক্যান করুন...")

if barcode:
    df = pd.read_csv(SHEET_URL)
    res = df[df['Barcode'].astype(str) == barcode]
    if not res.empty:
        st.success(f"পণ্য: {res.iloc[0]['Name']} | মূল্য: {res.iloc[0]['Price']} টাকা")
    else:
        st.error("পাওয়া যায়নি!")
