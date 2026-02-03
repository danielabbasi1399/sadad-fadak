import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات صفحه
st.set_page_config(page_title="مدیریت برداشت سداد فدک", page_icon="🌶️", layout="wide")

st.title("ثبت روزانه فروش و وزن فلفل")

# اتصال به گوگل شیت
conn = st.connection("gsheets", type=GSheetsConnection)

# خواندن داده‌ها
try:
    existing_data = conn.read(worksheet="Sheet1", ttl=0)
    existing_data = existing_data.dropna(how="all")
except Exception:
    columns = ["تاریخ", "روز هفته", "بذر ۱", "سوپر ۱", "درجه ۱", "بذر ۲", "سوپر ۲", "درجه ۲", "بذر ۳", "سوپر ۳", "درجه ۳"]
    existing_data = pd.DataFrame(columns=columns)

# فرم ورودی
with st.form(key="farm_form"):
    st.subheader("📅 اطلاعات پایه")
    col_date1, col_date2 = st.columns(2)
    
    with col_date1:
        # دریافت تاریخ امروز به شمسی به عنوان پیش‌فرض
        today_shamsi = jdatetime.date.today().strftime('%Y/%m/%d')
        shamsi_date = st.text_input("تاریخ (مثلاً ۱۴۰۴/۰۹/۱۵)", value=today_shamsi)
    
    with col_date2:
        # تشخیص خودکار روز هفته از روی تاریخ وارد شده
        try:
            date_obj = jdatetime.datetime.strptime(shamsi_date, '%Y/%m/%d')
            weekdays = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یکشنبه"]
            current_day = weekdays[date_obj.weekday()]
        except:
            current_day = "نامشخص"
        
        st.write(f"**روز هفته:** {current_day}")

    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.error("🏘️ گلخانه ۱")
        seed1 = st.selectbox("نوع بذر (۱)", ["اندرومدا", "راگاراک", "سایر"])
        super1 = st.number_input("وزن سوپر ۱", min_value=0.0, step=0.1, key="s1")
        grade1 = st.number_input("وزن درجه ۱", min_value=0.0, step=0.1, key="g1")

    with col2:
        st.info("🏘️ گلخانه ۲")
        seed2 = st.selectbox("نوع بذر (۲)", ["اندرومدا", "G20", "سایر"])
        super2 = st.number_input("وزن سوپر ۲", min_value=0.0, step=0.1, key="s2")
        grade2 = st.number_input("وزن درجه ۲", min_value=0.0, step=0.1, key="g2")

    with col3:
        st.success("🏘️ گلخانه ۳")
        seed3 = st.selectbox("نوع بذر (۳)", ["نیروین", "سایر"])
        super3 = st.number_input("وزن سوپر ۳", min_value=0.0, step=0.1, key="s3")
        grade3 = st.number_input("وزن درجه ۳", min_value=0.0, step=0.1, key="g3")

    st.markdown("---")
    submit_button = st.form_submit_button(label="💾 ثبت اطلاعات در جدول اصلی")

# عملیات ثبت
if submit_button:
    if shamsi_date:
        new_row = pd.DataFrame([{
            "تاریخ": shamsi_date,
            "روز هفته": current_day,
            "بذر ۱": seed1, "سوپر ۱": super1, "درجه ۱": grade1,
            "بذر ۲": seed2, "سوپر ۲": super2, "درجه ۲": grade2,
            "بذر ۳": seed3, "سوپر ۳": super3, "درجه ۳": grade3
        }])
        
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        
        try:
            conn.update(worksheet="Sheet1", data=updated_df)
            st.success(f"✅ اطلاعات روز {current_day} با موفقیت ثبت شد!")
            st.cache_data.clear()
            st.rerun()
        except Exception as e:
            st.error(f"خطا در اتصال: {e}")
