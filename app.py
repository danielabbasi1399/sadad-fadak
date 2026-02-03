import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime
from streamlit_jalali_calendar import date_picker

# تنظیمات صفحه
st.set_page_config(page_title="سیستم هوشمند سداد فدک", page_icon="🌶️", layout="wide")

st.title("ثبت هوشمند برداشت - گلخانه‌های ۱، ۲ و ۳")

# اتصال به گوگل شیت
conn = st.connection("gsheets", type=GSheetsConnection)

# خواندن داده‌های موجود
try:
    existing_data = conn.read(worksheet="Sheet1", ttl=0)
    existing_data = existing_data.dropna(how="all")
except Exception:
    columns = ["تاریخ", "روز هفته", "بذر ۱", "سوپر ۱", "درجه ۱", "بذر ۲", "سوپر ۲", "درجه ۲", "بذر ۳", "سوپر ۳", "درجه ۳"]
    existing_data = pd.DataFrame(columns=columns)

# فرم ورودی اطلاعات
with st.form(key="smart_form"):
    st.subheader("📅 انتخاب زمان (فقط تقویم شمسی)")
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        # ایجاد تقویم کشویی کاملاً شمسی
        picked_date = date_picker("انتخاب تاریخ شمسی", key="date_p")
        
        # تبدیل تاریخ برای محاسبات و نمایش
        shamsi_date_str = picked_date.strftime('%Y/%m/%d')
        
    with col_d2:
        # محاسبه دقیق روز هفته فارسی
        weekdays = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یکشنبه"]
        current_day = weekdays[picked_date.weekday()]
        
        st.info(f"تاریخ انتخاب شده: {shamsi_date_str}")
        st.success(f"روز هفته: {current_day}")

    st.markdown("---")
    
    # بخش گلخانه‌ها
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.error("🏘️ گلخانه ۱")
        seed1 = st.selectbox("نوع بذر ۱", ["اندرومدا", "راگاراک", "سایر"], key="sel1")
        s1 = st.number_input("سوپر (۱)", min_value=0.0, step=0.1)
        g1 = st.number_input("درجه (۱)", min_value=0.0, step=0.1)

    with c2:
        st.info("🏘️ گلخانه ۲")
        seed2 = st.selectbox("نوع بذر ۲", ["اندرومدا", "G20", "سایر"], key="sel2")
        s2 = st.number_input("سوپر (۲)", min_value=0.0, step=0.1)
        g2 = st.number_input("درجه (۲)", min_value=0.0, step=0.1)

    with c3:
        st.success("🏘️ گلخانه ۳")
        seed3 = st.selectbox("نوع بذر ۳", ["نیروین", "سایر"], key="sel3")
        s3 = st.number_input("سوپر (۳)", min_value=0.0, step=0.1)
        g3 = st.number_input("درجه (۳)", min_value=0.0, step=0.1)

    st.markdown("---")
    submit = st.form_submit_button(label="📥 ثبت نهایی در فایل اکسل")

# عملیات ذخیره‌سازی
if submit:
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
        st.success(f"✅ اطلاعات روز {current_day} با موفقیت در اکسل ثبت شد.")
        st.cache_data.clear()
        st.rerun()
    except Exception as e:
        st.error(f"خطا در ثبت: {e}")

# نمایش لیست
st.subheader("📋 لیست داده‌های ثبت شده")
st.dataframe(existing_data, use_container_width=True)
