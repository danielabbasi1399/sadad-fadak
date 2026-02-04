import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات اصلی
st.set_page_config(page_title="سداد فدک", layout="wide")

# اتصال به گوگل‌شیت
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("خطا در اتصال! لطفاً تنظیمات Secrets را در استریم‌لیت چک کنید.")

# تابع تبدیل متن به عدد
def n(v):
    try:
        val = str(v).strip()
        return float(val) if val else 0.0
    except:
        return 0.0

# مدیریت ریست فرم
if "reset_key" not in st.session_state:
    st.session_state.reset_key = 0

rk = st.session_state.reset_key

st.title("📊 سیستم ثبت برداشت - سداد فدک")

# بخش تاریخ
c_y, c_m, c_d = st.columns(3)
year = c_y.selectbox("سال", [1403, 1404, 1405], index=1)
month = c_m.selectbox("ماه", range(1, 13), index=10)
day = c_d.selectbox("روز", range(1, 32), index=13)
shamsi_date = f"{year}/{month:02d}/{day:02d}"

st.divider()

# چیدمان گلخانه‌ها (با تراز دستی)
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("🏘️ گلخانه ۱")
        s1an = st.text_input("اندرومدا - سوپر", key=f"s1an_{rk}")
        g1an = st.text_input("اندرومدا - درجه", key=f"g1an_{rk}")
        st.write(f"جمع: {n(s1an) + n(g1an)}")
        st.divider()
        s1ra = st.text_input("راگاراک - سوپر", key=f"s1ra_{rk}")
        g1ra = st.text_input("راگاراک - درجه", key=f"g1ra_{rk}")
        st.write(f"جمع: {n(s1ra) + n(g1ra)}")
        st.info(f"کل گ۱: {n(s1an)+n(g1an)+n(s1ra)+n(g1ra)}")

with col2:
    with st.container(border=True):
        st.subheader("🏘️ گلخانه ۲")
        s2an = st.text_input("اندرومدا - سوپر ", key=f"s2an_{rk}")
        g2an = st.text_input("اندرومدا - درجه ", key=f"g2an_{rk}")
        st.write(f"جمع: {n(s2an) + n(g2an)}")
        st.divider()
        s2g2 = st.text_input("G20 - سوپر", key=f"s2g2_{rk}")
        g2g2 = st.text_input("G20 - درجه", key=f"g2g2_{rk}")
        st.write(f"جمع: {n(s2g2) + n(g2g2)}")
        st.info(f"کل گ۲: {n(s2an)+n(g2an)+n(s2g2)+n(g2g2)}")

with col3:
    with st.container(border=True):
        st.subheader("🏘️ گلخانه ۳")
        s3ni = st.text_input("نیروین - سوپر", key=f"s3ni_{rk}")
        g3ni = st.text_input("نیروین - درجه", key=f"g3ni_{rk}")
        st.write(f"جمع: {n(s3ni) + n(g3ni)}")
        
        # تراز دستی (برای اینکه شروع و پایان یکی باشد)
        for _ in range(9): st.write("") 
        
        st.divider()
        st.info(f"کل گ۳: {n(s3ni)+n(g3ni)}")

total_s = n(s1an) + n(s1ra) + n(s2an) + n(s2g2) + n(s3ni)
total_g = n(g1an) + n(g1ra) + n(g2an) + n(g2g2) + n(g3ni)

# دکمه ثبت
if st.button("🚀 ثبت اطلاعات و تخلیه فرم", use_container_width=True):
    try:
        # ایجاد دیتای جدید
        new_row = {
            "تاریخ": shamsi_date,
            "جمع کل": total_s + total_g
        }
        
        # تبدیل به دیتافریم
        new_df = pd.DataFrame([new_row])

        # خواندن شیت (حتماً چک کنید نام شیت شما Sheet1 باشد)
        df_existing = conn.read(worksheet="Sheet1")
        
        # ترکیب و آپدیت
        updated_df = pd.concat([df_existing, new_df], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
        
        st.success("✅ ثبت شد!")
        st.session_state.reset_key += 1
        st.rerun()
        
    except Exception as e:
        st.error(f"خطای فنی: {str(e)}")
