import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات اصلی
st.set_page_config(page_title="سداد فدک", page_icon="🌶️", layout="wide")
st.title("ثبت هوشمند برداشت - سداد فدک")

conn = st.connection("gsheets", type=GSheetsConnection)

# تابع تبدیل متن به عدد (فقط برای محاسبات)
def n(v):
    try: return float(v) if v.strip() else 0.0
    except: return 0.0

# --- انتخاب تاریخ ---
now = jdatetime.datetime.now()
c_y, c_m, c_d = st.columns(3)
with c_y: year = st.selectbox("سال", [1403, 1404, 1405], index=1)
with c_m: 
    m_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    month = st.selectbox("ماه", range(1, 13), format_func=lambda x: m_names[x-1], index=now.month-1)
with c_d: day = st.selectbox("روز", range(1, 32), index=now.day-1)

p_date = jdatetime.date(year, month, day)
shamsi_str = p_date.strftime('%Y/%m/%d')
g_date = p_date.togregorian()
w_map = {0: "دوشنبه", 1: "سه‌شنبه", 2: "چهارشنبه", 3: "پنج‌شنبه", 4: "جمعه", 5: "شنبه", 6: "یکشنبه"}
current_day = w_map[g_date.weekday()]
st.info(f"📅 {current_day} - {shamsi_str}")

st.divider()

# --- بخش ورودی‌ها ---
col1, col2, col3 = st.columns(3)

with col1:
    st.error("🏘️ گلخانه ۱")
    st.write("**اندرومدا**")
    s1an = st.text_input("سوپر", key="s1an", value="")
    g1an = st.text_input("درجه", key="g1an", value="")
    # فقط اگر عددی وارد شده باشد، جمع را نشان بده
    if s1an.strip() or g1an.strip():
        total = n(s1an) + n(g1an)
        if total > 0: st.success(f"جمع: {total}")
    
    st.markdown("---")
    st.write("**راگاراک**")
    s1ra = st.text_input("سوپر", key="s1ra", value="")
    g1ra = st.text_input("درجه", key="g1ra", value="")
    if s1ra.strip() or g1ra.strip():
        total = n(s1ra) + n(g1ra)
        if total > 0: st.success(f"جمع: {total}")

with col2:
    st.info("🏘️ گلخانه ۲")
    st.write("**اندرومدا**")
    s2an = st.text_input("سوپر", key="s2an", value="")
    g2an = st.text_input("درجه", key="g2an", value="")
    if s2an.strip() or g2an.strip():
        total = n(s2an) + n(g2an)
        if total > 0: st.success(f"جمع: {total}")
    
    st.markdown("---")
    st.write("**G20**")
    s2g2 = st.text_input("سوپر", key="s2g2", value="")
    g2g2 = st.text_input("درجه", key="g2g2", value="")
    if s2g2.strip() or g2g2.strip():
        total = n(s2g2) + n(g2g2)
        if total > 0: st.success(f"جمع: {total}")

with col3:
    st.success("🏘️ گلخانه ۳")
    st.write("**نیروین**")
    s3ni = st.text_input("سوپر", key="s3ni", value="")
    g3ni = st.text_input("درجه", key="g3ni", value="")
    if s3ni.strip() or g3ni.strip():
        total = n(s3ni) + n(g3ni)
        if total > 0: st.success(f"جمع: {total}")

st.divider()

if st.button("🚀 ثبت نهایی در اکسل"):
    new_data = pd.DataFrame([{
        "تاریخ": shamsi_str, "روز هفته": current_day,
        "اندرومدا ۱ (S)": n(s1an), "اندرومدا ۱ (G)": n(g1an),
        "راگاراک ۱ (S)": n(s1ra), "راگاراک ۱ (G)": n(g1ra),
        "اندرومدا ۲ (S)": n(s2an), "اندرومدا ۲ (G)": n(g2an),
        "G20 2 (S)": n(s2g2), "G20 2 (G)": n(g2g2),
        "نیروین ۳ (S)": n(s3ni), "نیروین ۳ (G)": n(g3ni)
    }])
    
    try:
        existing_data = conn.read(worksheet="Sheet1", ttl=0).dropna(how="all")
        updated_df = pd.concat([existing_data, new_data], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
        st.balloons()
        st.success("✅ با موفقیت ثبت شد.")
        st.cache_data.clear()
    except:
        st.error("خطا در ثبت!")

st.subheader("📋 سوابق")
st.dataframe(conn.read(worksheet="Sheet1", ttl=0).dropna(how="all"), use_container_width=True)
