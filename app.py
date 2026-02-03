import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات ظاهری صفحه
st.set_page_config(page_title="سداد فدک - مدیریت هوشمند", page_icon="🌶️", layout="wide")

st.title("ثبت برداشت روزانه - گلخانه‌های ۱، ۲ و ۳")

# اتصال به گوگل شیت
conn = st.connection("gsheets", type=GSheetsConnection)

# خواندن داده‌های موجود
try:
    existing_data = conn.read(worksheet="Sheet1", ttl=0)
    existing_data = existing_data.dropna(how="all")
except Exception:
    columns = ["تاریخ", "روز هفته", "بذر ۱", "سوپر ۱", "درجه ۱", "بذر ۲", "سوپر ۲", "درجه ۲", "بذر ۳", "سوپر ۳", "درجه ۳"]
    existing_data = pd.DataFrame(columns=columns)

# فرم ورودی اطلاعات با تقویم شمسی سفارشی
with st.form(key="shamsi_form"):
    st.subheader("📅 انتخاب تاریخ شمسی (بدون میلادی)")
    
    # دریافت تاریخ امروز شمسی برای پیش‌فرض
    now = jdatetime.datetime.now()
    
    col_y, col_m, col_d = st.columns(3)
    with col_y:
        y = st.selectbox("سال", [1403, 1404, 1405], index=1)
    with col_m:
        month_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
        m = st.selectbox("ماه", range(1, 13), format_func=lambda x: month_names[x-1], index=now.month-1)
    with col_d:
        d = st.selectbox("روز", range(1, 32), index=now.day-1)

    # محاسبه و نمایش روز هفته
    try:
        date_obj = jdatetime.date(y, m, d)
        shamsi_date_str = date_obj.strftime('%Y/%m/%d')
        weekdays = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یکشنبه"]
        day_of_week = weekdays[date_obj.weekday()]
        st.success(f"تاریخ انتخاب شده: {shamsi_date_str} ({day_of_week})")
    except ValueError:
        st.error("تاریخ وارد شده نامعتبر است!")
        day_of_week = None

    st.markdown("---")
    
    # بخش گلخانه‌ها (دقیقا مطابق لیست شما)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.error("🏘️ گلخانه ۱")
        seed1 = st.selectbox("نوع بذر ۱", ["اندرومدا", "راگاراک", "سایر"])
        s1 = st.number_input("سوپر (۱)", min_value=0.0, step=0.1)
        g1 = st.number_input("درجه (۱)", min_value=0.0, step=0.1)
    with c2:
        st.info("🏘️ گلخانه ۲")
        seed2 = st.selectbox("نوع بذر ۲", ["اندرومدا", "G20", "سایر"])
        s2 = st.number_input("سوپر (۲)", min_value=0.0, step=0.1)
        g2 = st.number_input("درجه (۲)", min_value=0.0, step=0.1)
    with c3:
        st.success("🏘️ گلخانه ۳")
        seed3 = st.selectbox("نوع بذر ۳", ["نیروین", "سایر"])
        s3 = st.number_input("سوپر (۳)", min_value=0.0, step=0.1)
        g3 = st.number_input("درجه (۳)", min_value=0.0, step=0.1)

    submit = st.form_submit_button(label="💾 ثبت نهایی در اکسل")

# عملیات ذخیره
if submit and day_of_week:
    new_data = pd.DataFrame([{
        "تاریخ": shamsi_date_str, "روز هفته": day_of_week,
        "بذر ۱": seed1, "سوپر ۱": s1, "درجه ۱": g1,
        "بذر ۲": seed2, "سوپر ۲": s2, "درجه ۲": g2,
        "بذر ۳": seed3, "سوپر ۳": s3, "درجه ۳": g3
    }])
    updated_df = pd.concat([existing_data, new_data], ignore_index=True)
    try:
        conn.update(worksheet="Sheet1", data=updated_df)
        st.success("✅ با موفقیت ثبت شد!")
        st.cache_data.clear()
        st.rerun()
    except Exception as e:
        st.error(f"خطا در ثبت: {e}")

# نمایش جدول پایین صفحه
st.dataframe(existing_data, use_container_width=True)
