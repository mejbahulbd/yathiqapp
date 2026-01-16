import streamlit as st
import sqlite3
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import date

# ---------- Database ----------
conn = sqlite3.connect("babycare.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    age TEXT,
    stock INTEGER,
    barcode TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    baby_birthday TEXT
)
""")
conn.commit()

# ---------- UI ----------
st.set_page_config(page_title="Baby Care POS & Inventory", layout="wide")

st.markdown("""
<style>
body {background-color: #fef6fb;}
h1, h2 {color: #ff69b4;}
</style>
""", unsafe_allow_html=True)

st.title("🍼 Baby Care POS & Inventory")

menu = st.sidebar.radio(
    "Menu",
    ["➕ Add Product", "👶 Add Customer", "🧾 Create Invoice", "📦 Inventory"]
)

# ---------- Add Product ----------
if menu == "➕ Add Product":
    st.header("Add New Product")

    name = st.text_input("Product Name")
    price = st.number_input("Price", 0.0)
    age = st.text_input("Age Range (e.g. 0-2 years)")
    stock = st.number_input("Stock", 0)
    barcode = st.text_input("Barcode (scan or type)")

    if st.button("Save Product"):
        c.execute(
            "INSERT INTO products (name, price, age, stock, barcode) VALUES (?,?,?,?,?)",
            (name, price, age, stock, barcode)
        )
        conn.commit()
        st.success("✅ Product Added")

# ---------- Add Customer ----------
elif menu == "👶 Add Customer":
    st.header("Customer Info")

    cname = st.text_input("Customer Name")
    birthday = st.date_input("Baby Birthday")

    if st.button("Save Customer"):
        c.execute(
            "INSERT INTO customers (name, baby_birthday) VALUES (?,?)",
            (cname, birthday)
        )
        conn.commit()
        st.success("✅ Customer Saved")

# ---------- Invoice ----------
elif menu == "🧾 Create Invoice":
    st.header("Create Invoice")

    products = pd.read_sql("SELECT * FROM products", conn)
    selected = st.selectbox("Select Product", products["name"])

    qty = st.number_input("Quantity", 1)

    if st.button("Generate Invoice"):
        product = products[products["name"] == selected].iloc[0]
        total = product["price"] * qty

        file_name = f"invoice_{selected}.pdf"
        pdf = canvas.Canvas(file_name, pagesize=A4)

        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(50, 800, "Baby Care Invoice")

        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, 760, f"Product: {selected}")
        pdf.drawString(50, 740, f"Price: {product['price']} x {qty}")
        pdf.drawString(50, 720, f"Total: {total} BDT")
        pdf.drawString(50, 700, f"Date: {date.today()}")

        pdf.save()
        st.success(f"📄 Invoice Created: {file_name}")

# ---------- Inventory ----------
elif menu == "📦 Inventory":
    st.header("Inventory List")
    df = pd.read_sql("SELECT name, price, age, stock FROM products", conn)
    st.dataframe(df)
