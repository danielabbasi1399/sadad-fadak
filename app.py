import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# تنظیمات صفحه
st.set_page_config(page_title="مدیریت گلخانه سداد فدک", page_icon="🌱")

st.title("ثبت برداشت روزانه")

# اتصال به گوگل شیت
conn = st.connection("gsheets", type=GSheetsConnection)

# خواندن داده‌ها برای نمایش
try:
    existing_data = conn.read(worksheet="Sheet1", ttl=0)
    existing_data = existing_data.dropna(how="all")
except Exception:
    existing_data = pd.DataFrame(columns=["تاریخ", "گلخانه", "بذر", "سوپر", "درجه"])

# فرم ورودی
with st.form(key="input_form"):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("تاریخ", value=datetime.now())
        greenhouse = st.text_input("نام یا شماره گلخانه")
    with col2:
        seed_type = st.text_input("نوع بذر")
        super_weight = st.number_input("وزن سوپر", min_value=0.0)
        grade_weight = st.number_input("وزن درجه", min_value=0.0)
    
    submit_button = st.form_submit_button(label="ثبت اطلاعات در لیست")

# عملیات ثبت
if submit_button:
    if greenhouse and seed_type:
        # ایجاد ردیف جدید بر اساس نام دقیق ستون‌های شما در عکس (ستون ها.png)
        new_row = pd.DataFrame([{
            "تاریخ": date.strftime('%Y-%m-%d'),
            "گلخانه": greenhouse,
            "بذر": seed_type,
            "سوپر": super_weight,
            "درجه": grade_weight
        }])
        
        # ترکیب با داده‌های قبلی
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        
        try:
            # بروزرسانی شیت
            conn.update(worksheet="Sheet1", data=updated_df)
            st.success("✅ اطلاعات با موفقیت در گوگل شیت ذخیره شد!")
            st.cache_data.clear()
            st.rerun()
        except Exception as e:
            st.error(f"❌ خطا: {e}")
    else:
        st.warning("⚠️ لطفا نام گلخانه و نوع بذر را وارد کنید.")

# نمایش جدول نهایی در سایت
st.divider()
st.subheader("📊 گزارش برداشت‌های ثبت شده")
st.dataframe(existing_data, use_container_width=True)
