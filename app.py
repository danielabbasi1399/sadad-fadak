import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# ۱. تنظیمات صفحه برای پهنای کامل
st.set_page_config(page_title="مدیریت سداد فدک", page_icon="📊", layout="wide")

# ۲. استایل CSS برای کادربندی تمیز
st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: white !important;
        border-radius: 15px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
        padding: 20px !important;
    }
    .gh-header {
        font-size: 18px; font-weight: bold; padding: 8px; 
        border-radius: 8px; text-align: center; color: white; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 مدیریت هوشمند برداشت - سداد فدک")

conn = st.connection("gsheets", type=GSheetsConnection)

# --- مدیریت ریست کردن فرم ---
if 'form_iteration' not in st.session_state:
    st.session_state.form_iteration = 0

def n(v):
    try: return float(v) if v.strip() else 0.0
    except: return 0.0

# --- بخش انتخاب تاریخ و روز هفته ---
now = jdatetime.datetime.now()
c_y, c_m, c_d = st.columns(3)
year = c_y.selectbox("سال", [1403, 1404, 1405], index=1)
m_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
month = c_m.selectbox("ماه", range(1, 13), format_func=lambda x: m_names[x-1], index=now.month-1)
day = c_d.selectbox("روز", range(1, 32), index=now.day-1)

# محاسبه روز هفته
selected_date = jdatetime.date(year, month, day)
shamsi_str = selected_date.strftime('%Y/%m/%d')
# منطق صحیح: 0=دوشنبه ... 2=چهارشنبه
weekdays = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یکشنبه"]
day_name = weekdays[selected_date.weekday()]

st.success(f"🗓️ تاریخ: {shamsi_str} ({day_name})")

st.divider()

# --- بخش ورودی‌ها ---
iter_prefix = f"v_{st.session_state.form_iteration}_"
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #e74c3c;">🏘️ گلخانه ۱</div>', unsafe_allow_html=True)
        st.markdown("🔴 **بذر اندرومدا**")
        s1an = st.text_input("سوپر", key=f"{iter_prefix}s1an")
        g1an = st.text_input("درجه", key=f"{iter_prefix}g1an")
        st.write(f"جمع: {n(s1an) + n(g1an) if n(s1an) + n(g1an) > 0 else ''}")
        st.markdown("---")
        st.markdown("🟡 **بذر راگاراک**")
        s1ra = st.text_input("سوپر ", key=f"{iter_prefix}s1ra")
        g1ra = st.text_input("درجه ", key=f"{iter_prefix}g1ra")
        st.write(f"جمع: {n(s1ra) + n(g1ra) if n(s1ra) + n(g1ra) > 0 else ''}")
        st.markdown("---")
        st.write(f"**جمع کل گ۱:** {n(s1an) + n(s1ra) + n(g1an) + n(g1ra)}")

with col2:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #3498db;">🏘️ گلخانه ۲</div>', unsafe_allow_html=True)
        st.markdown("🔴 **بذر اندرومدا**")
        s2an = st.text_input("سوپر  ", key=f"{iter_prefix}s2an")
        g2an = st.text_input("درجه  ", key=f"{iter_prefix}g2an")
        st.write(f"جمع: {n
