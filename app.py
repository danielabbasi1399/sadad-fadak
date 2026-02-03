import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات اصلی
st.set_page_config(page_title="سداد فدک", page_icon="🌶️", layout="wide")

st.title("ثبت برداشت روزانه - سداد فدک")

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

# تابع کمکی برای تبدیل متن به عدد (برای محاسبات آنی)
def get_num(val):
    try:
        return float(val) if val.strip() else 0.0
    except:
        return 0.0

# --- انتخاب تاریخ ---
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

# --- فرم ثبت اطلاعات با نمایش جمع کل ---
with st.form(key="total_sum_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.error("🏘️ گلخانه ۱")
        st.markdown("---")
        st.markdown("**اندرومدا**")
        s1_an = st.text_input("سوپر", key="s1an", value="")
        g1_an = st.text_input("درجه", key="g1an", value="")
        # نمایش جمع (در لحظه ثبت محاسبه می‌شود)
        st.markdown("---")
        st.markdown("**راگاراک**")
        s1_ra = st.text_input("سوپر", key="s1ra", value="")
        g1_ra = st.text_input("درجه", key="g1ra", value="")

    with col2:
        st.info("🏘️ گلخانه ۲")
        st.markdown("---")
        st.markdown("**اندرومدا**")
        s2_an = st.text_input("سوپر", key="s2an", value="")
        g2_an = st.text_input("درجه", key="g2an", value="")
        st.markdown("---")
        st.markdown("**G20**")
        s2_g2 = st.text_input("سوپر", key="s2g2", value="")
        g2_g2 = st.text_input("درجه", key="g2g2", value="")

    with col3:
        st.success("🏘️ گلخانه ۳")
        st.markdown("---")
        st.markdown("**نیروین**")
        s3_ni = st.text_input("سوپر", key="s3ni", value="")
        g3_ni = st.text_input("درجه", key="g3ni", value="")

    st.markdown("---")
    submitted = st.form_submit_button("🚀 ثبت نهایی اطلاعات در اکسل")

# پردازش و ذخیره
if submitted and current_day:
    # مقادیر عددی
    v1_an_s = get_num(s1_an); v1_an_g = get_num(g1_an)
    v1_ra_s = get_num(s1_ra); v1_ra_g = get_num(g1_ra)
    v2_an_s = get_num(s2_an); v2_an_g = get_num(g2_an)
    v2_g2_s = get_num(s2_g2); v2_g2_g = get_num(g2_g2)
    v3_ni_s = get_num(s3_ni); v3_ni_g = get_num(g3_ni)

    # نمایش جمع کل هر بذر در پیام موفقیت
    total_1_an = v1_an_s + v1_an_g
    total_1_ra = v1_ra_s + v1_ra_g
    total_2_an = v2_an_s + v2_an_g
    total_2_g2 = v2_g2_s + v2_g2_g
    total_3_ni = v3_ni_s + v3_ni_g

    new_data = pd.DataFrame([{
        "تاریخ": shamsi_str, "روز هفته": current_day,
        "اندرومدا ۱ (S)": v1_an_s, "اندرومدا ۱ (G)": v1_an_g,
        "راگاراک ۱ (S)": v1_ra_s, "راگاراک ۱ (G)": v1_ra_g,
        "اندرومدا ۲ (S)": v2_an_s, "اندرومدا ۲ (G)": v2_an_g,
        "G20 2 (S)": v2_g2_s, "G20 2 (G)": v2_g2_g,
        "نیروین ۳ (S)": v3_ni_s, "نیروین ۳ (G)": v3_ni_g
    }])
    
    try:
        updated_df = pd.concat([existing_data, new_data], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
        st.balloons()
        # نمایش گزارش کوتاه به کاربر
        st.success(f"✅ ثبت شد! جمع اندرومدا ۱: {total_1_an} | راگاراک ۱: {total_1_ra} | بقیه موارد نیز ثبت شدند.")
        st.cache_data.clear()
        st.rerun()
    except Exception as e:
        st.error(f"خطا: {e}")

st.divider()
st.dataframe(existing_data, use_container_width=True)
