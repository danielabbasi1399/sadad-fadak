import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# تنظیمات صفحه
st.set_page_config(page_title="سیستم پیشرفته سداد فدک", page_icon="🌶️", layout="wide")

st.title("ثبت تفکیکی برداشت گلخانه‌ها")

# اتصال به گوگل شیت
conn = st.connection("gsheets", type=GSheetsConnection)

# خواندن داده‌ها
try:
    existing_data = conn.read(worksheet="Sheet1", ttl=0)
    existing_data = existing_data.dropna(how="all")
except Exception:
    # ستون‌ها مطابق با عکس اکسل شما: تاریخ، بذر، و وزن‌های تفکیکی
    columns = ["تاریخ", "بذر", "گلخانه ۱ (سوپر)", "گلخانه ۱ (درجه)", "گلخانه ۲ (سوپر)", "گلخانه ۲ (درجه)", "گلخانه ۳ (سوپر)", "گلخانه ۳ (درجه)"]
    existing_data = pd.DataFrame(columns=columns)

# فرم ورود اطلاعات با چیدمان مشابه اکسل
with st.form(key="advanced_form"):
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        date = st.date_input("📅 انتخاب تاریخ", value=datetime.now())
    with col_info2:
        seed_type = st.text_input("🌱 نوع بذر", placeholder="مثلاً فلفل دلمه")

    st.markdown("---")
    
    # ایجاد سه ستون برای سه گلخانه (مطابق عکس اکسل)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🏘️ گلخانه ۱")
        g1_super = st.number_input("وزن سوپر (۱)", min_value=0.0, step=0.1)
        g1_grade = st.number_input("وزن درجه (۱)", min_value=0.0, step=0.1)

    with col2:
        st.subheader("🏘️ گلخانه ۲")
        g2_super = st.number_input("وزن سوپر (۲)", min_value=0.0, step=0.1)
        g2_grade = st.number_input("وزن درجه (۲)", min_value=0.0, step=0.1)

    with col3:
        st.subheader("🏘️ گلخانه ۳")
        g3_super = st.number_input("وزن سوپر (۳)", min_value=0.0, step=0.1)
        g3_grade = st.number_input("وزن درجه (۳)", min_value=0.0, step=0.1)

    submit_button = st.form_submit_button(label="📥 ثبت نهایی در جدول اکسل")

# عملیات ثبت
if submit_button:
    new_row = pd.DataFrame([{
        "تاریخ": date.strftime('%Y-%m-%d'),
        "بذر": seed_type,
        "گلخانه ۱ (سوپر)": g1_super,
        "گلخانه ۱ (درجه)": g1_grade,
        "گلخانه ۲ (سوپر)": g2_super,
        "گلخانه ۲ (درجه)": g2_grade,
        "گلخانه ۳ (سوپر)": g3_super,
        "گلخانه ۳ (درجه)": g3_grade
    }])
    
    updated_df = pd.concat([existing_data, new_row], ignore_index=True)
    
    try:
        conn.update(worksheet="Sheet1", data=updated_df)
        st.success("✅ اطلاعات با تفکیک گلخانه‌ها در گوگل شیت ذخیره شد!")
        st.cache_data.clear()
        st.rerun()
    except Exception as e:
        st.error(f"❌ خطا در ثبت: {e}")

# نمایش جدول
st.divider()
st.subheader("📊 مشاهده لیست ثبت شده (مشابه فایل اکسل شما)")
st.dataframe(existing_data, use_container_width=True)
