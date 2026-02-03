import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات اصلی برنامه
st.set_page_config(page_title="سداد فدک - نسخه نهایی", page_icon="🌶️", layout="wide")

st.title("ثبت تفکیکی برداشت روزانه - سداد فدک")

# اتصال به گوگل شیت
conn = st.connection("gsheets", type=GSheetsConnection)

# خواندن داده‌های موجود
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

# --- بخش انتخاب تاریخ (آپدیت آنی) ---
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

# محاسبه دقیق روز هفته (تبدیل به میلادی برای دقت ۱۰۰٪)
try:
    p_date = jdatetime.date(year, month, day)
    shamsi_str = p_date.strftime('%Y/%m/%d')
    g_date = p_date.togregorian()
    # دوشنبه در پایتون 0 است
    w_map = {0: "دوشنبه", 1: "سه‌شنبه", 2: "چهارشنبه", 3: "پنج‌شنبه", 4: "جمعه", 5: "شنبه", 6: "یکشنبه"}
    current_day = w_map[g_date.weekday()]
    st.info(f"💡 روز هفته: {current_day} | تاریخ: {shamsi_str}")
except ValueError:
    st.error("تاریخ انتخاب شده در تقویم وجود ندارد!")
    current_day = None

st.divider()

# --- فرم ثبت اطلاعات (تفکیک بذرها) ---
with st.form(key="harvest_form_final"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.error("🏘️ گلخانه ۱")
        st.markdown("**بذر اندرومدا**")
        s1_an = st.text_input("سوپر (۱-اندرومدا)", value="", placeholder="وزن")
        g1_an = st.text_input("درجه (۱-اندرومدا)", value="", placeholder="وزن")
        st.markdown("---")
        st.markdown("**بذر راگاراک**")
        s1_ra = st.text_input("سوپر (۱-راگاراک)", value="", placeholder="وزن")
        g1_ra = st.text_input("درجه (۱-راگاراک)", value="", placeholder="وزن")

    with col2:
        st.info("🏘️ گلخانه ۲")
        st.markdown("**بذر اندرومدا**")
        s2_an = st.text_input("سوپر (۲-اندرومدا)", value="", placeholder="وزن")
        g2_an = st.text_input("درجه (۲-اندرومدا)", value="", placeholder="وزن")
        st.markdown("---")
        st.markdown("**بذر G20**")
        s2_g2 = st.text_input("سوپر (۲-G20)", value="", placeholder="وزن")
        g2_g2 = st.text_input("درجه (۲-G20)", value="", placeholder="وزن")

    with col3:
        st.success("🏘️ گلخانه ۳")
        st.markdown("**بذر نیروین**")
        s3_ni = st.text_input("سوپر (۳-نیروین)", value="", placeholder="وزن")
        g3_ni = st.text_input("درجه (۳-نیروین)", value="", placeholder="وزن")
        st.markdown("---")
        st.caption("در این گلخانه فقط بذر نیروین کشت شده است.")

    # دکمه ثبت (حتماً باید داخل بلاک form باشد)
    submitted = st.form_submit_button("🚀 ثبت نهایی اطلاعات در اکسل")

# --- پردازش و ذخیره داده‌ها ---
if submitted and current_day:
    # تابع تبدیل متن به عدد
    def clean(v):
        try:
            return float(v) if v.strip() else 0.0
        except:
            return 0.0

    # ساخت ردیف جدید (دقت کنید تمام آکولادها و پرانتزها بسته شوند)
    new_data = pd.DataFrame([{
        "تاریخ": shamsi_str,
        "روز هفته": current_day,
        "اندرومدا ۱ (S)": clean(s1_an),
        "اندرومدا ۱ (G)": clean(g1_an),
        "راگاراک ۱ (S)": clean(s1_ra),
        "راگاراک ۱ (G)": clean(g1_ra),
        "اندرومدا ۲ (S)": clean(s2_an),
        "اندرومدا ۲ (G)": clean(g2_an),
        "G20 2 (S)": clean(s2_g2),
        "G20 2 (G)": clean(g2_g2),
        "نیروین ۳ (S)": clean(s3_ni),
        "نیروین ۳ (G)": clean(g3_ni)
    }])
    
    try:
        updated_df = pd.concat([existing_data, new_data], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
        st.balloons()
        st.success("✅ اطلاعات با موفقیت در گوگل‌شیت ثبت شد.")
        st.cache_data.clear()
        st.rerun()
    except Exception as e:
        st.error(f"خطا در اتصال به گوگل‌شیت: {e}")

st.divider()
st.subheader("📋 مشاهده سوابق اخیر")
st.dataframe(existing_data, use_container_width=True)
