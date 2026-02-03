import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات صفحه
st.set_page_config(page_title="سیستم ثبت سداد فدک", page_icon="🌶️", layout="wide")

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

# فرم ورودی اطلاعات
with st.form(key="main_form"):
    st.subheader("📅 زمان برداشت")
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        # تاریخ امروز شمسی به صورت خودکار
        today = jdatetime.date.today().strftime('%Y/%m/%d')
        shamsi_date = st.text_input("تاریخ (مثال: ۱۴۰۴/۰۹/۱۵)", value=today)
    
    with col_d2:
        # تشخیص خودکار روز هفته
        try:
            d_obj = jdatetime.datetime.strptime(shamsi_date, '%Y/%m/%d')
            weekdays = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یکشنبه"]
            current_day = weekdays[d_obj.weekday()]
        except:
            current_day = "خطا در تاریخ"
        st.info(f"روز هفته: {current_day}")

    st.markdown("---")
    
    # چیدمان سه ستونه برای سه گلخانه مطابق درخواست شما
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

    st.markdown("---")
    submit = st.form_submit_button(label="🚀 ثبت در اکسل")

# عملیات ذخیره‌سازی
if submit:
    if current_day != "خطا در تاریخ":
        new_row = pd.DataFrame([{
            "تاریخ": shamsi_date,
            "روز هفته": current_day,
            "بذر ۱": seed1, "سوپر ۱": s1, "درجه ۱": g1,
            "بذر ۲": seed2, "سوپر ۲": s2, "درجه ۲": g2,
            "بذر ۳": seed3, "سوپر ۳": s3, "درجه ۳": g3
        }])
        
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        
        try:
            conn.update(worksheet="Sheet1", data=updated_df)
            st.success(f"✅ اطلاعات روز {current_day} با موفقیت ثبت شد!")
            st.cache_data.clear()
            st.rerun()
        except Exception as e:
            st.error(f"خطا در ثبت: {e}")
    else:
        st.error("لطفاً فرمت تاریخ را درست وارد کنید (مثال: ۱۴۰۴/۰۹/۱۵)")

# نمایش لیست
st.subheader("📊 آخرین ورودی‌ها")
st.dataframe(existing_data, use_container_width=True)
