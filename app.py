import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات اصلی برنامه
st.set_page_config(page_title="سداد فدک - ثبت آنی", page_icon="🌶️", layout="wide")

st.title("ثبت هوشمند برداشت - گلخانه‌های ۱، ۲ و ۳")

# اتصال به گوگل شیت
conn = st.connection("gsheets", type=GSheetsConnection)

# خواندن داده‌های قبلی
try:
    existing_data = conn.read(worksheet="Sheet1", ttl=0)
    existing_data = existing_data.dropna(how="all")
except Exception:
    columns = ["تاریخ", "روز هفته", "بذر ۱", "سوپر ۱", "درجه ۱", "بذر ۲", "سوپر ۲", "درجه ۲", "بذر ۳", "سوپر ۳", "درجه ۳"]
    existing_data = pd.DataFrame(columns=columns)

# --- بخش انتخاب تاریخ (آپدیت آنی روز هفته) ---
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

# محاسبه سریع روز هفته
try:
    picked_date = jdatetime.date(year, month, day)
    shamsi_date_str = picked_date.strftime('%Y/%m/%d')
    # نقشه دقیق روزهای هفته برای jdatetime
    weekdays_map = {0: "دوشنبه", 1: "سه‌شنبه", 2: "چهارشنبه", 3: "پنج‌شنبه", 4: "جمعه", 5: "شنبه", 6: "یکشنبه"}
    current_day = weekdays_map[picked_date.weekday()]
    
    # نمایش آنی نتیجه
    st.success(f"📅 تاریخ: {shamsi_date_str} | روز هفته: {current_day}")
except ValueError:
    st.error("تاریخ انتخاب شده در تقویم وجود ندارد (مثلاً ۳۱ شهریور)!")
    current_day = None

st.markdown("---")

# --- فرم ثبت مقادیر عددی ---
with st.form(key="harvest_form"):
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.error("🏘️ گلخانه ۱")
        seed1 = st.selectbox("نوع بذر ۱", ["اندرومدا", "راگاراک", "سایر"])
        s1 = st.number_input("سوپر (۱)", min_value=0.0, step=0.1, key="s1")
        g1 = st.number_input("درجه (۱)", min_value=0.0, step=0.1, key="g1")

    with c2:
        st.info("🏘️ گلخانه ۲")
        seed2 = st.selectbox("نوع بذر ۲", ["اندرومدا", "G20", "سایر"])
        s2 = st.number_input("سوپر (۲)", min_value=0.0, step=0.1, key="s2")
        g2 = st.number_input("درجه (۲)", min_value=0.0, step=0.1, key="g2")

    with c3:
        st.success("🏘️ گلخانه ۳")
        seed3 = st.selectbox("نوع بذر ۳", ["نیروین", "سایر"])
        s3 = st.number_input("سوپر (۳)", min_value=0.0, step=0.1, key="s3")
        g3 = st.number_input("درجه (۳)", min_value=0.0, step=0.1, key="g3")

    submit = st.form_submit_button(label="📥 ثبت نهایی در فایل اکسل")

# عملیات ذخیره‌سازی پس از فشردن دکمه
if submit and current_day:
    new_row = pd.DataFrame([{
        "تاریخ": shamsi_date_str,
        "روز هفته": current_day,
        "بذر ۱": seed1, "سوپر ۱": s1, "درجه ۱": g1,
        "بذر ۲": seed2, "سوپر ۲": s2, "درجه ۲": g2,
        "بذر ۳": seed3, "سوپر ۳": s3, "درجه ۳": g3
    }])
    
    updated_df = pd.concat([existing_data, new_row], ignore_index=True)
    
    try:
        conn.update(worksheet="Sheet1", data=updated_df)
        st.balloons()
        st.success(f"✅ اطلاعات روز {current_day} با موفقیت ثبت شد.")
        st.cache_data.clear()
        st.rerun()
    except Exception as e:
        st.error(f"خطا در ثبت اطلاعات: {e}")

st.divider()
st.subheader("📋 سوابق اخیر در اکسل")
st.dataframe(existing_data, use_container_width=True)
