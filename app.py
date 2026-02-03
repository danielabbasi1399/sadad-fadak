import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات اصلی
st.set_page_config(page_title="سداد فدک - سیستم جامع", page_icon="🌶️", layout="wide")

st.title("ثبت تفکیکی برداشت روزانه - سداد فدک")

# اتصال به گوگل شیت
conn = st.connection("gsheets", type=GSheetsConnection)

# خواندن داده‌ها
try:
    existing_data = conn.read(worksheet="Sheet1", ttl=0)
    existing_data = existing_data.dropna(how="all")
except Exception:
    columns = [
        "تاریخ", "روز هفته", 
        "اندرومدا ۱ (S)", "اندرومدا ۱ (G)", "راگاراک ۱ (S)", "راگاراک ۱ (G)",
        "اندرومدا ۲ (S)", "اندرومدا ۲ (G)", "G20 2 (S)", "G20 2 (G)",
        "نیروین ۳ (S)", "نیروین ۳ (G)"
    ]
    existing_data = pd.DataFrame(columns=columns)

# --- بخش تاریخ (آپدیت زنده) ---
st.subheader("📅 انتخاب زمان")
now = jdatetime.datetime.now()
c_y, c_m, c_d = st.columns(3)
with c_y: year = st.selectbox("سال", [1403, 1404, 1405], index=1)
with c_m: 
    m_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    month = st.selectbox("ماه", range(1, 13), format_func=lambda x: m_names[x-1], index=now.month-1)
with c_d: day = st.selectbox("روز", range(1, 32), index=now.day-1)

try:
    p_date = jdatetime.date(year, month, day)
    shamsi_str = p_date.strftime('%Y/%m/%d')
    g_date = p_date.togregorian()
    w_map = {0: "دوشنبه", 1: "سه‌شنبه", 2: "چهارشنبه", 3: "پنج‌شنبه", 4: "جمعه", 5: "شنبه", 6: "یکشنبه"}
    current_day = w_map[g_date.weekday()]
    st.info(f"📅 روز هفته: {current_day} | تاریخ: {shamsi_str}")
except ValueError:
    st.error("تاریخ نامعتبر است!")
    current_day = None

st.divider()

# --- فرم نهایی با دکمه ثبت تضمینی ---
with st.form(key="final_harvest_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.error("🏘️ گلخانه ۱")
        st.markdown("**بذر اندرومدا**")
        s1_an = st.text_input("سوپر (۱-اندرومدا)", key="s1an", placeholder="وزن")
        g1_an = st.text_input("درجه (۱-اندرومدا)", key="g1an", placeholder="وزن")
        st.markdown("---")
        st.markdown("**بذر راگاراک**")
        s1_ra = st.text_input("سوپر (۱-راگاراک)", key="s1ra", placeholder="وزن")
        g1_ra = st.text_input("درجه (۱-راگاراک)", key="g1ra", placeholder="وزن")

    with col2:
        st.info("🏘️ گلخانه ۲")
        st.markdown("**بذر اندرومدا**")
        s2_an = st.text_input("سوپر (۲-اندرومدا)", key="s2an", placeholder="وزن")
        g2_an = st.text_input("درجه (۲-اندرومدا)", key="g2an", placeholder="وزن")
        st.markdown("---")
        st.markdown("**بذر G20**")
        s2_g2 = st.text_input("سوپر (۲-G20)", key="s2g2", placeholder="وزن")
        g2_g2 = st.text_input("درجه (۲-G20)", key="g2g2", placeholder="وزن")

    with col3:
        st.success("🏘️ گلخانه ۳")
        st.markdown("**بذر نیروین**")
        s3_ni = st.text_input("سوپر (۳-نیروین)", key="s3ni", placeholder="وزن")
        g3_ni = st.text_input("درجه (۳-نیروین)", key="g3ni", placeholder="وزن")
        st.markdown("---")
        st.caption("در این گلخانه فقط بذر نیروین کشت شده است.")

    # دکمه ثبت دقیقاً داخل فرم
    submitted = st.form_submit_button("🚀 ثبت نهایی اطلاعات در اکسل")

# پردازش بعد از کلیک
if submitted and current_day:
    def parse_val(v):
        try: return float(v) if v.strip() else 0.0
        except: return 0.0

    new_data = pd.DataFrame([{
        "تاریخ": shamsi_str, "روز هفته": current_day,
        "اندرومدا ۱ (S)": parse_val(s1_an), "اندرومدا ۱ (G)": parse_val(g1_an),
        "راگاراک ۱ (S)": parse_val(s1_ra), "راگاراک ۱ (G)": parse_val(g1_ra),
        "اندرومدا ۲ (S)":
