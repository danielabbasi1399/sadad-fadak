import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات اصلی
st.set_page_config(page_title="سداد فدک", page_icon="🫑", layout="wide")
st.title("ثبت هوشمند برداشت - سداد فدک")

conn = st.connection("gsheets", type=GSheetsConnection)

# تابع تبدیل متن به عدد
def n(v):
    try: return float(v) if v.strip() else 0.0
    except: return 0.0

# --- بخش تاریخ ---
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
    # اندرومدا ۱
    st.markdown("🔴 **بذر اندرومدا**")
    s1an = st.text_input("سوپر", key="s1an", value="")
    g1an = st.text_input("درجه", key="g1an", value="")
    t1an = n(s1an) + n(g1an)
    if t1an > 0: st.write(f"جمع: {t1an}") # مربع آبی کاملا حذف شد
    
    st.markdown("---")
    # راگاراک ۱
    st.markdown("🟡 **بذر راگاراک**")
    s1ra = st.text_input("سوپر", key="s1ra", value="")
    g1ra = st.text_input("درجه", key="g1ra", value="")
    t1ra = n(s1ra) + n(g1ra)
    if t1ra > 0: st.write(f"جمع: {t1ra}")

with col2:
    st.info("🏘️ گلخانه ۲")
    # اندرومدا ۲
    st.markdown("🔴 **بذر اندرومدا**")
    s2an = st.text_input("سوپر", key="s2an", value="")
    g2an = st.text_input("درجه", key="g2an", value="")
    t2an = n(s2an) + n(g2an)
    if t2an > 0: st.write(f"جمع: {t2an}")
    
    st.markdown("---")
    # G20
    st.markdown("🔴 **بذر G20**")
    s2g2 = st.text_input("سوپر", key="s2g2", value="")
    g2g2 = st.text_input("درجه", key="g2g2", value="")
    t2g2 = n(s2g2) + n(g2g2)
    if t2g2 > 0: st.write(f"جمع: {t2g2}")

with col3:
    st.success("🏘️ گلخانه ۳")
    # نیروین
    st.markdown("🔴 **بذر نیروین**")
    s3ni = st.text_input("سوپر", key="s3ni", value="")
    g3ni = st.text_input("درجه", key="g3ni", value="")
    t3ni = n(s3ni) + n(g3ni)
    if t3ni > 0: st.write(f"جمع: {t3ni}")

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
        st.success("✅ اطلاعات با موفقیت ثبت شد.")
        st.cache_data.clear()
    except:
        st.error("خطا در ثبت!")

st.subheader("📋 سوابق")
st.dataframe(conn.read(worksheet="Sheet1", ttl=0).dropna(how="all"), use_container_width=True)
