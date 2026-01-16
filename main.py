import streamlit as st
import pandas as pd
from datetime import datetime

# অ্যাপের টাইটেল ও কালার সেটআপ
st.set_page_config(page_title="Baby Care POS", layout="wide")

# সিএসএস দিয়ে ডিজাইন সুন্দর করা (Baby Pink & Blue Theme)
st.markdown("""
    <style>
    .main { background-color: #FFF5F7; }
    .stButton>button { background-color: #FFB6C1; color: white; border-radius: 20px; border: none; }
    .stTextInput>div>div>input { border-radius: 10px; border: 1px solid #ADD8E6; }
    h1 { color: #FF69B4; font-family: 'SolaimanLipi', sans-serif; }
    .memo-box { background-color: white; padding: 20px; border: 2px dashed #FFB6C1; border-radius: 10px; }
    </style>
    """, unsafe_allow_input_with_html=True)

st.title("👶 বেবি কেয়ার - বিক্রয় ও মেমো অ্যাপ")

# সাইডবার - ইনভেন্টরি বা স্টক এন্ট্রি
with st.sidebar:
    st.header("📦 নতুন স্টক যোগ করুন")
    p_name = st.text_input("পণ্যের নাম")
    p_price = st.number_input("বিক্রয় মূল্য", min_value=0)
    p_stock = st.number_input("স্টক পরিমাণ", min_value=0)
    if st.button("স্টক আপডেট করুন"):
        st.success(f"{p_name} স্টকে যোগ হয়েছে!")

# মেইন সেকশন - বিলিং বা মেমো তৈরি
st.header("🛒 নতুন মেমো তৈরি করুন")

col1, col2 = st.columns(2)

with col1:
    cust_name = st.text_input("ক্রেতার নাম")
    cust_phone = st.text_input("মোবাইল নম্বর")
    baby_bday = st.date_input("বাচ্চার জন্মদিন (ঐচ্ছিক)")

with col2:
    item_name = st.text_input("পণ্যের নাম (যা বিক্রি হচ্ছে)")
    item_qty = st.number_input("পরিমাণ", min_value=1, value=1)
    unit_price = st.number_input("একক মূল্য", min_value=0)
    discount = st.number_input("ডিসকাউন্ট (টাকা)", min_value=0)

total = (item_qty * unit_price) - discount

# মেমো জেনারেটর
if st.button("মেমো দেখুন ও প্রিন্ট করুন"):
    st.markdown("---")
    st.markdown(f"""
    <div class="memo-box">
        <h2 style="text-align: center; color: #FF69B4;">বেবি কেয়ার শপ</h2>
        <p style="text-align: center;">ঠিকানা: আপনার দোকানের ঠিকানা এখানে</p>
        <p><strong>তারিখ:</strong> {datetime.now().strftime('%d/%m/%Y')} | <strong>সময়:</strong> {datetime.now().strftime('%H:%M')}</p>
        <hr>
        <p><strong>ক্রেতা:</strong> {cust_name}</p>
        <p><strong>মোবাইল:</strong> {cust_phone}</p>
        <p><strong>বাচ্চার জন্মদিন:</strong> {baby_bday}</p>
        <hr>
        <table style="width:100%">
            <tr><th>বিবরণ</th><th>পরিমাণ</th><th>দাম</th></tr>
            <tr><td>{item_name}</td><td>{item_qty}</td><td>{unit_price * item_qty} টাকা</td></tr>
        </table>
        <hr>
        <h3 style="text-align: right;">মোট বিল: {total} টাকা</h3>
        <p style="text-align: center; font-size: 12px;">পণ্য কেনার ৭ দিনের মধ্যে ক্যাশ মেমোসহ পরিবর্তনের সুযোগ থাকবে।</p>
        <p style="text-align: center; font-weight: bold;">ধন্যবাদ, আবার আসবেন!</p>
    </div>
    """, unsafe_allow_input_with_html=True)
    
    st.balloons() # সেলস সাকসেস হলে বেলুন উড়বে

# আজকের বিক্রয় রিপোর্ট (নিচে ছোট করে)
st.markdown("---")
st.subheader("📊 আজকের বিক্রয় রিপোর্ট")
st.info("অ্যাপটি চালু রাখার পর থেকে এখানে আপনার মোট বিক্রয় জমা হবে।")
