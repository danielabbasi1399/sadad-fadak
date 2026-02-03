import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات صفحه
st.set_page_config(page_title="سداد فدک - ثبت تفکیکی کامل", page_icon="🌶️", layout="wide")

st.title("ثبت برداشت روزانه - تفکیک بذر هر سه گلخانه")

# اتصال به گوگل شیت
conn = st.connection("gsheets", type=GSheetsConnection)

# خواندن داده‌ها
try:
    existing_data = conn.read(worksheet="Sheet1", ttl=0)
    existing_data = existing_data.dropna(how="all")
except Exception:
    columns = [
        "تاریخ", "روز هفته", 
        "اندرومدا ۱ (S)", "اندرومدا ۱ (G)", "راگاراک ۱ (S)", "راگاراک ۱ (G)",
        "اندرومدا ۲ (S)", "اندرومدا ۲ (G)", "G20 2 (S)", "G20 2 (G)",
        "نیروین ۳ (S)", "نیروین ۳ (G)"
    ]
    existing_data = pd.DataFrame(columns=columns)

# --- انتخاب تاریخ (آپدیت آنی) ---
st.subheader("📅 انتخاب زمان برداشت")
now = jdatetime.datetime.now()
c_y, c_m, c_d = st.columns(3)
with c_y: year = st.selectbox("سال", [1403, 1404, 1405], index=1)
with c_m: 
    m_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    month = st.selectbox("ماه", range(1, 13), format_func=lambda x: m_names[x-1], index=now.month-1)
with c_d: day = st.selectbox("روز", range(1, 32), index=now.day-1)

try:
    p_date = jdatetime.date(year, month, day)
    shamsi_str = p_date.strftime('%Y/%m/%d')
    g_date = p_date.togregorian()
    w_map = {0: "دوشنبه", 1: "سه‌شنبه", 2: "چهارشنبه", 3: "پنج‌شنبه", 4: "جمعه", 5: "شنبه", 6: "یکشنبه"}
    current_day = w_map[g_date.weekday()]
    st.info(f"💡 روز هفته: {current_day} | تاریخ: {shamsi_str}")
except ValueError:
    st.error("تاریخ اشتباه است!")
    current_day = None

st.markdown("---")

# --- فرم ثبت تفکیکی برای هر سه گلخانه ---
with st.form(key="harvest_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.error("🏘️ گلخانه ۱")
        st.write("**بذر اندرومدا**")
        s1_an = st.text_input("سوپر (۱-اندرومدا)", value="", placeholder="وزن")
        g1_an = st.text_input("درجه (۱-اندرومدا)", value="", placeholder="وزن")
        st.write("---")
        st.write("**بذر راگاراک**")
        s1_ra = st.text_input("سوپر (۱-راگاراک)", value="", placeholder="وزن")
        g1_ra = st.text_input("درجه (۱-راگاراک)", value="", placeholder="وزن")

    with col2:
        st.info("🏘️ گلخانه ۲")
        st.write("**بذر اندرومدا**")
        s2_an = st.text_input("سوپر (۲-اندرومدا)", value="", placeholder="وزن")
        g2_an = st.text_input("درجه (۲-اندرومدا)", value="", placeholder="وزن")
        st.write("---")
        st.write("**بذر G20**")
        s2_g20 = st.text_input("سوپر (۲-G20)", value="", placeholder="وزن")
        g2_g20 = st.text_input("درجه (۲-G20)", value="", placeholder="وزن")

    with col3:
        st.success("🏘️ گلخانه ۳")
        st.write("**بذر نیروین**")
        s3_ni = st.text_input("سوپر (۳-نیروین)", value="", placeholder="وزن")
        g3_ni = st.text_input("درجه (۳-نیروین)", value="", placeholder="وزن")
        st.write("---")
        st.write(" ") # برای تراز شدن ستون‌ها
