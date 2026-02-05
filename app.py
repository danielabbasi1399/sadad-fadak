import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# ۱. تنظیمات صفحه
st.set_page_config(page_title="مدیریت سداد فدک", page_icon="📊", layout="wide")

# ۲. استایل CSS
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

if 'form_iteration' not in st.session_state:
    st.session_state.form_iteration = 0

def n(v):
    try: return float(v.strip()) if v and v.strip() else 0.0
    except: return 0.0

# --- بخش انتخاب تاریخ (۱ بهمن = چهارشنبه) ---
now = jdatetime.datetime.now()
c_y, c_m, c_d = st.columns(3)
year = c_y.selectbox("سال", [1403, 1404, 1405], index=1)
m_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
month = c_m.selectbox("ماه", range(1, 13), format_func=lambda x: m_names[x-1], index=now.month-1)
day = c_d.selectbox("روز", range(1, 32), index=now.day-1)

selected_date = jdatetime.date(year, month, day)
shamsi_str = selected_date.strftime('%Y/%m/%d')
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
        s1an_s = st.text_input("اندرومدا - سوپر", key=f"{iter_prefix}s1an_s")
        s1an_g = st.text_input("اندرومدا - درجه", key=f"{iter_prefix}s1an_g")
        st.markdown("---")
        s1ra_s = st.text_input("راگاراک - سوپر", key=f"{iter_prefix}s1ra_s")
        s1ra_g = st.text_input("راگاراک - درجه", key=f"{iter_prefix}s1ra_g")

with col2:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #3498db;">🏘️ گلخانه ۲</div>', unsafe_allow_html=True)
        s2an_s = st.text_input("اندرومدا - سوپر ", key=f"{iter_prefix}s2an_s")
        s2an_g = st.text_input("اندرومدا - درجه ", key=f"{iter_prefix}s2an_g")
        st.markdown("---")
        s2g2_s = st.text_input("G20 - سوپر", key=f"{iter_prefix}s2g2_s")
        s2g2_g = st.text_input("G20 - درجه", key=f"{iter_prefix}s2g2_g")

with col3:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #27ae60;">🏘️ گلخانه ۳</div>', unsafe_allow_html=True)
        s3ni_s = st.text_input("نیروین - سوپر", key=f"{iter_prefix}s3ni_s")
        s3ni_g = st.text_input("نیروین - درجه", key=f"{iter_prefix}s3ni_g")

st.divider()

# محاسبات نهایی
total_s = n(s1an_s) + n(s1ra_s) + n(s2an_s) + n(s2g2_s) + n(s3ni_s)
total_g = n(s1an_g) + n(s1ra_g) + n(s2an_g) + n(s2g2_g) + n(s3ni_g)

st.subheader("📊 آمار کل امروز")
f1, f2, f3 = st.columns(3)
f1.metric("کل سوپر", total_s)
f2.metric("کل درجه", total_g)
f3.metric("جمع نهایی", total_s + total_g)

# --- اصلاحیه بخش ثبت اطلاعات ---
if st.button("🚀 ثبت نهایی و تخلیه فرم", use_container_width=True):
    try:
        # در اینجا نام تمام ستون‌هایی که می‌خواهید در اکسل بیاید را تعریف می‌کنیم
        data_to_save = {
            "تاریخ": shamsi_str,
            "روز هفته": day_name,
            "گ۱ اندرومدا سوپر": n(s1an_s),
            "گ۱ اندرومدا درجه": n(s1an_g),
            "گ۱ راگاراک سوپر": n(s1ra_s),
            "گ۱ راگاراک درجه": n(s1ra_g),
            "گ۲ اندرومدا سوپر": n(s2an_s),
            "گ۲ اندرومدا درجه": n(s2an_g),
            "گ۲ G20 سوپر": n(s2g2_s),
            "گ۲ G20 درجه": n(s2g2_g),
            "گ۳ نیروین سوپر": n(s3ni_s),
            "گ۳ نیروین درجه": n(s3ni_g),
            "کل سوپر": total_s,
            "کل درجه": total_g,
            "جمع کل نهایی": total_s + total_g
        }
        
        new_row = pd.DataFrame([data_to_save])
        df = conn.read(worksheet="Sheet1", ttl=0).dropna(how="all")
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
        
        st.session_state.form_iteration += 1 
        st.success("✅ تمامی اطلاعات با موفقیت در گوگل‌شیت ثبت شد.")
        st.rerun()
    except Exception as e:
        st.error(f"خطا در ثبت: {e}")
