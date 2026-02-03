import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات صفحه
st.set_page_config(page_title="سداد فدک - ثبت هوشمند", page_icon="🌶️", layout="wide")

st.title("ثبت برداشت روزانه - گلخانه‌های ۱، ۲ و ۳")

# اتصال به گوگل شیت
conn = st.connection("gsheets", type=GSheetsConnection)

# خواندن داده‌ها
try:
    existing_data = conn.read(worksheet="Sheet1", ttl=0)
    existing_data = existing_data.dropna(how="all")
except Exception:
    columns = ["تاریخ", "روز هفته", "بذر ۱", "سوپر ۱", "درجه ۱", "بذر ۲", "سوپر ۲", "درجه ۲", "بذر ۳", "سوپر ۳", "درجه ۳"]
    existing_data = pd.DataFrame(columns=columns)

# فرم ورودی با تقویم شمسی اختصاصی (بدون نیاز به پکیج اضافی)
with st.form(key="final_safe_form"):
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

    # محاسبه دقیق روز هفته
    try:
        picked_date = jdatetime.date(year, month, day)
        shamsi_date_str = picked_date.strftime('%Y/%m/%d')
        weekdays = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یکشنبه"]
        current_day = weekdays[picked_date.weekday()]
        st.success(f"✅ تاریخ انتخاب شده: {shamsi_date_str} ({current_day})")
    except ValueError:
        st.error("تاریخ اشتباه است! (مثلاً ۳۱ شهریور نداریم)")
        current_day = None

    st.markdown("---")
    
    # چیدمان سه ستونه گلخانه‌ها
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
    new_row = pd.DataFrame([{
        "تاریخ": shamsi_date_str, "روز هفته": current_day,
        "بذر ۱": seed1, "سوپر ۱": s1, "درجه ۱": g1,
        "بذر ۲": seed2, "سوپر ۲": s2, "درجه ۲": g2,
        "بذر ۳": seed3, "سوپر ۳": s3, "درجه ۳": g3
    }])
    updated_df = pd.concat([existing_data, new_row], ignore_index=True)
    try:
        conn.update(worksheet="Sheet1", data=updated_df)
        st.success("✅ اطلاعات با موفقیت ثبت شد.")
        st.cache_data.clear()
        st.rerun()
    except Exception as e:
        st.error(f"خطا در ارتباط با گوگل‌شیت: {e}")

st.divider()
st.dataframe(existing_data, use_container_width=True)
