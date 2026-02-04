import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات اصلی
st.set_page_config(page_title="سداد فدک", page_icon="🌶️", layout="wide")
st.title("ثبت هوشمند برداشت - سداد فدک")

conn = st.connection("gsheets", type=GSheetsConnection)

# تابع تبدیل متن به عدد
def n(v):
    try: return float(v) if v.strip() else 0.0
    except: return 0.0

# --- انتخاب تاریخ ---
now = jdatetime.datetime.now()
c_y, c_m, c_d = st.columns(3)
with c_y: year = st.selectbox("سال", [1403, 1404, 1405], index=1)
with c_m: 
    m_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    month = st.selectbox("ماه", range(1, 13), format_func=lambda x: m_names[x-1], index=now.month-1)
with c_d: day = st.selectbox("روز", range(1, 32), index=now.day-1)

p_date = jdatetime.date(year, month, day)
shamsi_str = p_date.strftime('%Y/%m/%d')
g_date = p_date.togregorian()
w_map = {0: "دوشنبه", 1: "سه‌شنبه", 2: "چهارشنبه", 3: "پنج‌شنبه", 4: "جمعه", 5: "شنبه", 6: "یکشنبه"}
current_day = w_map[g_date.weekday()]
st.info(f"📅 {current_day} - {shamsi_str}")

st.divider()

# --- بخش ورودی‌ها ---
col1, col2, col3 = st.columns(3)

with col1:
    st.error("🏘️ گلخانه ۱")
    # اندرومدا
    st.write("**اندرومدا**")
    s1an = st.text_input("سوپر", key="s1an", value="")
    g1an = st.text_input("درجه", key="g1an", value="")
    total1an = n(s1an) + n(g1an)
    st.write(f"🔹 جمع: {total1an if total1an > 0 else ''}")
    
    st.markdown("---")
    # راگاراک
    st.write("**راگاراک**")
    s1ra = st.text_input("سوپر", key="s1ra", value="")
    g1ra = st.text_input("درجه", key="g1ra", value="")
    total1ra = n(s1ra) + n(g1ra)
    st.write(f"🔹 جمع: {total1ra if total1ra > 0 else ''}")

with col2:
    st.info("🏘️ گلخانه ۲")
    # اندرومدا
    st.write("**اندرومدا**")
    s2an = st.text_input("سوپر", key="s2an", value="")
    g2an = st.text_input("درجه", key="g2an", value="")
    total2an = n(s2an) + n(g2an)
    st.write(f"🔹 جمع: {total2an if total2an > 0 else ''}")
    
    st.markdown("---")
    # G20
    st.write("**G20**")
    s2g2 = st.text_input("سوپر", key="s2g2", value="")
    g2g2 = st.text_input("درجه", key="g2g2", value="")
    total2g2 = n(s2g2) + n(g2g2)
    st.write(f"🔹 جمع: {total2g2 if total2g2 > 0 else ''}")

with col3:
    st.success("🏘️ گلخانه ۳")
    # نیروین
    st.write("**نیروین**
