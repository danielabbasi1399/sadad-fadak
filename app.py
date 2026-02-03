import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات صفحه
st.set_page_config(page_title="سداد فدک - ثبت آنی", page_icon="🌶️", layout="wide")

st.title("ثبت هوشمند برداشت - گلخانه‌های ۱، ۲ و ۳")

# اتصال به گوگل شیت
conn = st.connection("gsheets", type=GSheetsConnection)

# خواندن داده‌ها
try:
    existing_data = conn.read(worksheet="Sheet1", ttl=0)
    existing_data = existing_data.dropna(how="all")
except Exception:
    columns = ["تاریخ", "روز هفته", "بذر ۱", "سوپر ۱", "درجه ۱", "بذر ۲", "سوپر ۲", "درجه ۲", "بذر ۳", "سوپر ۳", "درجه ۳"]
    existing_data = pd.DataFrame(columns=columns)

# --- بخش انتخاب تاریخ (خارج از فرم برای آپدیت آنی) ---
st.subheader("📅 انتخاب تاریخ شمسی")
now = jdatetime.datetime.now()
col_y, col_m, col_d = st.columns(3)

with col_y:
    year = st.selectbox("سال", [1403, 1404, 1405], index=1)
with col_m:
    month_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    month = st.selectbox("ماه", range(1, 13), format_func=lambda x: month_names[x-1], index=now.month-1)
with col_d:
    day = st.selectbox("روز", range(1, 32), index=now.day-1)

# محاسبه آنی و سریع روز هفته
try:
    picked_date = jdatetime.date(year, month, day)
    shamsi_date_str = picked_date.strftime('%Y/%m/%d')
    weekdays_map = {0: "دوشنبه", 1: "سه‌شنبه", 2: "چهارشنبه", 3: "پنج‌شنبه", 4: "جمعه", 5: "شنبه", 6: "یکشنبه"}
    current_day = weekdays_map[picked_date.weekday()]
    
    # نمایش روز هفته بلافاصله بعد از انتخاب تاریخ
    st.info(f"💡 روز هفته: {current_day} | تاریخ: {shamsi_date_str}")
except ValueError:
    st.error("تاریخ اشتباه است! (مثلاً ۳۱ شهریور وجود ندارد)")
    current_day = None

st.markdown("---")

# --- بخش فرم ثبت مقادیر ---
with st.form(key="values_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.error("🏘️ گلخانه ۱")
        seed1 = st.selectbox("بذر ۱", ["اندرومدا", "راگاراک", "سایر"])
        s1 = st.number_input("سوپر ۱", min_value=0.0, step=0.1)
        g1 = st.number_input("درجه ۱", min_value=0.0, step=0.1)
    with c2:
        st.info("🏘️ گلخانه ۲")
        seed2 = st.selectbox("بذر ۲", ["اندرومدا", "G20", "سایر"])
        s2 = st.number_input("سوپر ۲", min_value=0.0, step=0.1)
        g2 = st.number_input("درجه ۲", min_value=0.0, step=0.1)
    with c3:
        st.success("🏘️ گلخانه ۳")
        seed3 = st.selectbox("بذر ۳", ["نیروین", "سایر"])
        s3 = st.number_input("سوپر ۳", min_value=0.0, step=0.1)
        g3 = st.number_input("درجه ۳", min_value=0.0, step=0.1)

    submit = st.form_submit_button(label="📥 ثبت نهایی در اکسل")

# ذخیره اطلاعات
if submit and current_day:
    new_row =
