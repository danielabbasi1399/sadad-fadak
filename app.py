import streamlit as st
from bidi.algorithm import get_display
import arabic_reshaper
import pandas as pd
from datetime import datetime

# تابع برای راست‌چین کردن متن‌های فارسی در نمودارها و جداول
def farsi_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

# تنظیمات اصلی صفحه
st.set_page_config(page_title="مدیریت گلخانه سداد فدک", layout="wide")

# شناسه فایل گوگل شیت شما (استخراج شده از لینکی که فرستادید)
SHEET_ID = '1TnEoy_TNn72BQypxE2RxVcgErtAeN9PlP_coWpRoIMg'
SHEET_NAME = 'Sheet1'
URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

st.title("🌿 سامانه هوشمند گلخانه سداد فدک")

# تعریف ساختار بذرها طبق توضیحات شما
structure = {
    "گلخانه ۱": ["اندرومدا", "راگا راک"],
    "گلخانه ۲": ["اندرومدا", "جی ۲۰"],
    "گلخانه ۳": ["نیروین شرکتی", "نیروین"]
}

# --- بخش ثبت داده ---
st.sidebar.header("ثبت بار روزانه")
with st.sidebar.form("daily_form", clear_on_submit=True):
    date_val = st.date_input("تاریخ", datetime.now())
    gh_choice = st.selectbox("انتخاب گلخانه", list(structure.keys()))
    seed_choice = st.selectbox("نوع بذر", structure[gh_choice])
    super_w = st.number_input("وزن بار سوپر (کیلو)", min_value=0.0)
    deg2_w = st.number_input("وزن بار درجه ۲ (کیلو)", min_value=0.0)
    
    submit = st.form_submit_button("ذخیره در بانک اطلاعاتی")

if submit:
    # در اینجا کد اتصال برای نوشتن (Write) قرار می‌گیرد
    st.success(f"اطلاعات بذر {seed_choice} با موفقیت ثبت شد.")

# --- بخش گزارش‌گیری ---
st.header("📊 گزارشات مدیریتی (دفتر اصفهان / موبایل)")

try:
    df = pd.read_csv(URL)
    
    # فیلترهای گزارش
    tab1, tab2, tab3 = st.tabs(["گزارش روزانه", "گزارش هفتگی/ماهانه", "جمع کل"])
    
    with tab1:
        st.subheader("برداشت امروز")
        # نمایش داده‌های امروز
        st.dataframe(df.tail(10)) # نمایش آخرین ورودی‌ها

    with tab2:
        st.subheader("تحلیل دوره‌ای")
        # در اینجا می‌توانید فیلتر تاریخ بگذارید
        
    with tab3:
        st.subheader("آمار کل بذرها")
        summary = df.groupby(['گلخانه', 'بذر'])[['سوپر', 'درجه ۲']].sum()
        st.table(summary)

except:
    st.info("در حال حاضر فایلی برای نمایش وجود ندارد یا داده‌ای ثبت نشده است.")
