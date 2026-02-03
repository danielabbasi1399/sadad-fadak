import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات صفحه
st.set_page_config(page_title="سداد فدک - ورودی خالی", page_icon="🌶️", layout="wide")

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

# --- بخش انتخاب تاریخ ---
st.subheader("📅 انتخاب زمان برداشت")
now = jdatetime.datetime.now()
col_y, col_m, col_d = st.columns(3)

with col_y:
    year = st.selectbox("سال", [1403, 1404, 1405], index=1)
with col_m:
    month_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    month = st.selectbox("ماه", range(1, 13), format_func=lambda x: month_names[x-1], index=now.month-1)
with col_d:
    day = st.selectbox("روز", range(1, 32), index=now.day-1)

# محاسبه ۱۰۰٪ دقیق روز هفته
try:
    picked_date = jdatetime.date(year, month, day)
    shamsi_date_str = picked_date.strftime('%Y/%m/%d')
    gregorian_date = picked_date.togregorian()
    weekdays_farsi = {0: "دوشنبه", 1: "سه‌شنبه", 2: "چهارشنبه", 3: "پنج‌شنبه", 4: "جمعه", 5: "شنبه", 6: "یکشنبه"}
    current_day = weekdays_farsi[gregorian_date.weekday()]
    st.success(f"✅ تاریخ انتخاب شده: {shamsi_date_str} | روز هفته: {current_day}")
except ValueError:
    st.error("تاریخ اشتباه است!")
    current_day = None

st.markdown("---")

# --- فرم ثبت مقادیر با کادرهای خالی ---
with st.form(key="harvest_form"):
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.error("🏘️ گلخانه ۱")
        seed1 = st.selectbox("بذر ۱", ["اندرومدا", "راگاراک", "سایر"])
        # استفاده از text_input به جای number_input برای خالی بودن کادر
        s1 = st.text_input("وزن سوپر ۱", placeholder="عدد وارد کنید")
        g1 = st.text_input("وزن درجه ۱", placeholder="عدد وارد کنید")

    with c2:
        st.info("🏘️ گلخانه ۲")
        seed2 = st.selectbox("بذر ۲", ["اندرومدا", "G20", "سایر"])
        s2 = st.text_input("وزن سوپر ۲", placeholder="عدد وارد کنید")
        g2 = st.text_input("وزن درجه ۲", placeholder="عدد وارد کنید")

    with c3:
        st.success("🏘️ گلخانه ۳")
        seed3 = st.selectbox("بذر ۳", ["نیروین", "سایر"])
        s3 = st.text_input("وزن سوپر ۳", placeholder="عدد وارد کنید")
        g3 = st.text_input("وزن درجه ۳", placeholder="عدد وارد کنید")

    submit = st.form_submit_button(label="📥 ثبت نهایی در اکسل")

# ذخیره اطلاعات
if submit and current_day:
    # تبدیل متن به عدد (اگر خالی باشد 0 در نظر گرفته می‌شود)
    def to_float(val):
        try:
            return float(val) if val else 0.0
