import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# ۱. تنظیمات صفحه
st.set_config(page_title="سداد فدک", layout="wide")

# ۲. اتصال به گوگل‌شیت (حتماً باید Secrets ست شده باشد)
conn = st.connection("gsheets", type=GSheetsConnection)

# ۳. تابع تبدیل عدد
def n(v):
    try: return float(v.strip()) if v.strip() else 0.0
    except: return 0.0

# ۴. مدیریت ریست فرم
if "reset_key" not in st.session_state:
    st.session_state.reset_key = 0

rk = st.session_state.reset_key

st.title("📊 ثبت نهایی برداشت - سداد فدک")

# ۵. بخش تاریخ
c_y, c_m, c_d = st.columns(3)
year = c_y.selectbox("سال", [1403, 1404, 1405], index=1)
month = c_m.selectbox("ماه", range(1, 13), index=10)
day = c_d.selectbox("روز", range(1, 32), index=13)
shamsi_date = f"{year}/{month:02d}/{day:02d}"

st.divider()

# ۶. چیدمان گلخانه‌ها
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("🏘️ گلخانه ۱")
        s1an = st.text_input("اندرومدا - سوپر", key=f"s1an_{rk}")
        g1an = st.text_input("اندرومدا - درجه", key=f"g1an_{rk}")
        st.write(f"جمع بذر: {n(s1an) + n(g1an)}")
        st.divider()
        s1ra = st.text_input("راگاراک - سوپر", key=f"s1ra_{rk}")
        g1ra = st.text_input("راگاراک - درجه", key=f"g1ra_{rk}")
        st.write(f"جمع بذر: {n(s1ra) + n(g1ra)}")
        st.info(f"کل گ۱: {n(s1an)+n(g1an)+n(s1ra)+n(g1ra)}")

with col2:
    with st.container(border=True):
        st.subheader("🏘️ گلخانه ۲")
        s2an = st.text_input("اندرومدا - سوپر ", key=f"s2an_{rk}")
        g2an = st.text_input("اندرومدا - درجه ", key=f"g2an_{rk}")
        st.write(f"جمع بذر: {n(s2an) + n(g2an)}")
        st.divider()
        s2g2 = st.text_input("G20 - سوپر", key=f"s2g2_{rk}")
        g2g2 = st.text_input("G20 - درجه", key=f"g2g2_{rk}")
        st.write(f"جمع بذر: {n(s2g2) + n(g2g2)}")
        st.info(f"کل گ۲: {n(s2an)+n(g2an)+n(s2g2)+n(g2g2)}")

with col3:
    with st.container(border=True):
        st.subheader("🏘️ گلخانه ۳")
        s3ni = st.text_input("نیروین - سوپر", key=f"s3ni_{rk}")
        g3ni = st.text_input("نیروین - درجه", key=f"g3ni_{rk}")
        st.write(f"جمع بذر: {n(s3ni) + n(g3ni)}")
        
        # تراز دستی (اینجا را کم و زیاد کن تا کادرها یکی شوند)
        for _ in range(9): st.write("") 
        
        st.divider()
        st.info(f"کل گ۳: {n(s3ni)+n(g3ni)}")

# ۷. آمار نهایی
st.divider()
total_s = n(s1an) + n(s1ra) + n(s2an) + n(s2g2) + n(s3ni)
total_g = n(g1an) + n(g1ra) + n(g2an) + n(g2g2) + n(g3ni)

f1, f2, f3 = st.columns(3)
f1.metric("کل سوپر", total_s)
f2.metric("کل درجه", total_g)
f3.metric("جمع نهایی کل", total_s + total_g)

# ۸. دکمه ثبت (عملیات اصلی)
if st.button("🚀 ثبت در گوگل شیت و تخلیه فرم", use_container_width=True):
    try:
        # ساخت یک سطر جدید برای اکسل
        new_row = pd.DataFrame([{
            "تاریخ": shamsi_date,
            "اندرومدا سوپر": n(s1an) + n(s2an),
            "اندرومدا درجه": n(g1an) + n(g2an),
            "راگاراک سوپر": n(s1ra),
            "راگاراک درجه": n(g1ra),
            "G20 سوپر": n(s2g2),
            "G20 درجه": n(g2g2),
            "نیروین سوپر": n(s3ni),
            "نیروین درجه": n(g3ni),
            "جمع کل": total_s + total_g
        }])

        # خواندن دیتای قبلی و اضافه کردن سطر جدید
        existing_data = conn.read(worksheet="Sheet1", ttl=0)
        updated_data = pd.concat([existing_data, new_row], ignore_index=True)
        
        # آپدیت شیت
        conn.update(worksheet="Sheet1", data=updated_data)
        
        st.success("✅ اطلاعات با موفقیت در اکسل ثبت شد!")
        st.session_state.reset_key += 1
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ خطا در ثبت! مطمئن شو نام Worksheet در اکسل تو 'Sheet1' است. جزئیات: {e}")
