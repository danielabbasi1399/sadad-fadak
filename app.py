import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات اصلی
st.set_page_config(page_title="سداد فدک", page_icon="🌶️", layout="wide")

st.title("ثبت برداشت روزانه - سداد فدک")

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

# --- انتخاب تاریخ ---
st.subheader("📅 انتخاب زمان")
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
    st.info(f"📅 روز هفته: {current_day} | تاریخ: {shamsi_str}")
except ValueError:
    st.error("تاریخ نامعتبر است!")
    current_day = None

st.divider()

# --- فرم نهایی با کادرهای کاملاً خالی ---
with st.form(key="clean_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.error("🏘️ گلخانه ۱")
        st.markdown("**بذر اندرومدا**")
        s1_an = st.text_input("سوپر", key="s1an", value="")
        g1_an = st.text_input("درجه", key="g1an", value="")
        st.markdown("---")
        st.markdown("**بذر راگاراک**")
        s1_ra = st.text_input("سوپر", key="s1ra", value="", label_visibility="visible")
        g1_ra = st.text_input("درجه", key="g1ra", value="", label_visibility="visible")

    with col2:
        st.info("🏘️ گلخانه ۲")
        st.markdown("**بذر اندرومدا**")
        s2_an = st.text_input("سوپر", key="s2an", value="")
        g2_an = st.text_input("درجه", key="g2an", value="")
        st.markdown("---")
        st.markdown("**بذر G20**")
        s2
