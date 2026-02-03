import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات ظاهری
st.set_page_config(page_title="سداد فدک - نسخه نهایی", page_icon="🌶️", layout="wide")

st.title("ثبت هوشمند برداشت - گلخانه‌های ۱، ۲ و ۳")

# اتصال به گوگل شیت
conn = st.connection("gsheets", type=GSheetsConnection)

# خواندن داده‌ها
try:
    existing_data = conn.read(worksheet="Sheet1", ttl=0)
    existing_data = existing_data.dropna(how="all")
except Exception:
    columns = ["تاریخ", "روز هفته", "بذر ۱", "سوپر ۱", "درجه ۱", "بذر ۲", "سوپر ۲", "درجه ۲", "بذر ۳", "سوپر ۳", "درجه ۳"]
    existing_data = pd.DataFrame(columns=columns)

# --- انتخاب تاریخ (آپدیت آنی) ---
st.subheader("📅 انتخاب زمان برداشت")
now = jdatetime.datetime.now()
c_y, c_m, c_d = st.columns(3)

with c_y:
    year = st.selectbox("سال", [1403, 1404, 1405], index=1)
with c_m:
    m_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    month = st.selectbox("ماه", range(1, 13), format_func=lambda x: m_names[x-1], index=now.month-1)
with c_d:
    day = st.selectbox("روز", range(1, 32), index=now.day-1)

# محاسبه دقیق روز هفته (۱ بهمن = چهارشنبه)
try:
    p_date = jdatetime.date(year, month, day)
    shamsi_str = p_date.strftime('%Y/%m/%d')
    g_date = p_date.togregorian()
    w_map = {0: "دوشنبه", 1: "سه‌شنبه", 2: "چهارشنبه", 3: "پنج‌شنبه", 4: "جمعه", 5: "شنبه", 6: "یکشنبه"}
    current_day = w_map[g_date.weekday()]
    st.info(f"💡 روز هفته: {current_day} | تاریخ: {shamsi_str}")
except ValueError:
    st.error("تاریخ اشتباه است!")
    current_day = None

st.markdown("---")

# --- فرم ثبت با کادرهای خالی ---
with st.form(key="harvest_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.error("🏘️ گلخانه ۱")
        seed1 = st.selectbox("بذر ۱", ["اندرومدا", "راگاراک", "سایر"])
        s1 = st.text_input("وزن سوپر (۱)", value="", placeholder="مثلاً 120.5")
        g1 = st.text_input("وزن درجه (۱)", value="", placeholder="مثلاً 45")

    with col2:
        st.info("🏘️ گلخانه ۲")
        seed2 = st.selectbox("بذر ۲", ["اندرومدا", "G20", "سایر"])
        s2 = st.text_input("وزن سوپر (۲)", value="", placeholder="مثلاً 80")
        g2 = st.text_input("وزن درجه (۲)", value="", placeholder="مثلاً 15.5")

    with col3:
        st.success("🏘️ گلخانه ۳")
        seed3 = st.selectbox("بذر ۳", ["نیروین", "سایر"])
        s3 = st.text_input("وزن سوپر (۳)", value="", placeholder="مثلاً 200")
        g3 = st.text_input("وزن درجه (۳)", value="", placeholder="مثلاً 10")

    submit = st.form_submit_button(label="📥 ثبت در اکسل")

# عملیات ذخیره
if submit and current_day:
    # تابع کمکی ساده برای تبدیل متن به عدد بدون خطا
    def clean_val(v):
        if v.strip() == "": return 0.0
        try:
            return float(v)
        except:
            return 0.0

    new_row = pd.DataFrame([{
        "تاریخ": shamsi_str, "روز هفته": current_day,
        "بذر ۱": seed1, "سوپر ۱": clean_val(s1), "درجه ۱": clean_val(g1),
        "بذر ۲": seed2, "سوپر ۲": clean_val(s2), "درجه ۲": clean_val(g2),
        "بذر ۳": seed3, "سوپر ۳": clean_val(s3), "درجه ۳": clean_val(g3)
    }])
    
    try:
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
        st.success(f"✅ اطلاعات روز {current_day} ثبت شد.")
        st.cache_data.clear()
        st.rerun()
    except Exception as e:
        st.error(f"خطا در ثبت: {e}")

st.divider()
st.dataframe(existing_data, use_container_width=True)
