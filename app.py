import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ۱. تنظیمات اولیه (ساده و بدون دست‌کاری اضافی)
st.set_page_config(page_title="مدیریت سداد فدک", layout="wide")

# ۲. تابع محاسبات عددی
def n(v):
    try:
        return float(v.strip()) if v.strip() else 0.0
    except:
        return 0.0

# ۳. مدیریت ریست شدن فرم (بدون پیچیدگی)
if "rk" not in st.session_state:
    st.session_state.rk = 0

rk = st.session_state.rk

st.title("📊 سیستم مدیریت برداشت فدک")

# ۴. بخش ورودی‌ها (استفاده از ستون‌های استاندارد)
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("🏘️ گلخانه ۱")
        s1an = st.text_input("اندرومدا - سوپر", key=f"s1an_{rk}")
        g1an = st.text_input("اندرومدا - درجه", key=f"g1an_{rk}")
        st.divider()
        s1ra = st.text_input("راگاراک - سوپر", key=f"s1ra_{rk}")
        g1ra = st.text_input("راگاراک - درجه", key=f"g1ra_{rk}")
        st.info(f"جمع کل گ۱: {n(s1an)+n(g1an)+n(s1ra)+n(g1ra)}")

with col2:
    with st.container(border=True):
        st.subheader("🏘️ گلخانه ۲")
        s2an = st.text_input("اندرومدا - سوپر ", key=f"s2an_{rk}")
        g2an = st.text_input("اندرومدا - درجه ", key=f"g2an_{rk}")
        st.divider()
        s2g2 = st.text_input("G20 - سوپر", key=f"s2g2_{rk}")
        g2g2 = st.text_input("G20 - درجه", key=f"g2g2_{rk}")
        st.info(f"جمع کل گ۲: {n(s2an)+n(g2an)+n(s2g2)+n(g2g2)}")

with col3:
    with st.container(border=True):
        st.subheader("🏘️ گلخانه ۳")
        s3ni = st.text_input("نیروین - سوپر", key=f"s3ni_{rk}")
        g3ni = st.text_input("نیروین - درجه", key=f"g3ni_{rk}")
        
        # --- تراز دستی ساده (فقط فضا اضافه می‌کنیم تا با بقیه هم‌قد شود) ---
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        # ---------------------------------------------------------
        
        st.info(f"جمع کل گ۳: {n(s3ni)+n(g3ni)}")

# ۵. دکمه ثبت (فقط عملیات ضروری)
if st.button("🚀 ثبت نهایی و تخلیه فرم", use_container_width=True):
    try:
        # اینجا فقط عملیات ریست فرم را انجام می‌دهیم تا برنامه هنگ نکند
        st.session_state.rk += 1
        st.success("فروم با موفقیت ریست شد.")
        st.rerun()
    except Exception as e:
        st.error(f"خطا: {e}")
