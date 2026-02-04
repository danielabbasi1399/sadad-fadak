import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات پیشرفته صفحه
st.set_page_config(page_title="داشبورد سداد فدک", page_icon="🌿", layout="wide")

# استایل CSS برای گرافیک بالا
st.markdown("""
    <style>
    /* استایل کلی پس‌زمینه */
    .main {
        background-color: #f0f2f6;
    }
    /* استایل کارت‌های گلخانه */
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: white !important;
        border: none !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        padding: 25px !important;
        transition: transform 0.3s;
    }
    /* استایل تیتر گلخانه‌ها */
    .gh-header {
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 15px;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        color: white;
    }
    /* دکمه ثبت مدرن */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background: linear-gradient(90deg, #1D976C 0%, #93F9B9 100%);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(29, 151, 108, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚜 مدیریت هوشمند برداشت - سداد فدک")

conn = st.connection("gsheets", type=GSheetsConnection)

def n(v):
    try: return float(v) if v.strip() else 0.0
    except: return 0.0

# --- بخش انتخاب تاریخ ---
with st.expander("📅 تنظیم تاریخ"):
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
st.success(f"🗓️ {current_day} - {shamsi_str}")

st.divider()

# --- چیدمان گلخانه‌ها ---
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #e74c3c;">🏘️ گلخانه ۱</div>', unsafe_allow_html=True)
        st.markdown("🔴 **بذر اندرومدا**")
        s1an = st.text_input("سوپر", key="s1an")
        g1an = st.text_input("درجه", key="g1an")
        t1an = n(s1an) + n(g1an)
        st.write(f"جمع: {t1an if t1an > 0 else ''}")
        
        st.divider()
        st.markdown("🟡 **بذر راگاراک**")
        s1ra = st.text_input("سوپر", key="s1ra")
        g1ra = st.text_input("درجه", key="g1ra")
        t1ra = n(s1ra) + n(g1ra)
        st.write(f"جمع: {t1ra if t1ra > 0 else ''}")

with col2:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #3498db;">🏘️ گلخانه ۲</div>', unsafe_allow_html=True)
        st.markdown("🔴 **بذر اندرومدا**")
        s2an = st.text_input("سوپر", key="s2an")
        g2an = st.text_input("درجه", key="g2an")
        t2an = n(s2an) + n(g2an)
        st.write(f"جمع: {t2an if t2an > 0 else ''}")
        
        st.divider()
        st.markdown("🔴 **بذر G20**")
        s2g2 = st.text_input("سوپر", key="s2g2")
        g2g2 = st.text_input("درجه", key="g2g2")
        t2g2 = n(s2g2) + n(g2g2)
        st.write(f"جمع: {t2g2 if t2g2 > 0 else ''}")

with col3:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #27ae60;">🏘️ گلخانه ۳</div>', unsafe_allow_html=True)
        st.markdown("🔴 **بذر نیروین**")
        s3ni = st.text_input("سوپر", key="s3ni")
        g3ni = st.text_input("درجه", key="g3ni")
        t3ni = n(s3ni) + n(g3ni)
        st.write(f"جمع: {t3ni if t3ni > 0 else ''}")
        # توازن ارتفاع
        st.write("")
        st.write("")
        st.write("")

st.divider()

# دکمه ثبت مدرن
if st.button("🚀 ثبت نهایی در جدول"):
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
        st.success("✅ اطلاعات با موفقیت ثبت شد.")
        st.cache_data.clear()
    except:
        st.error("خطا در ثبت اطلاعات!")

st.subheader("📋 سوابق اخیر")
st.dataframe(conn.read(worksheet="Sheet1", ttl=0).dropna(how="all"), use_container_width=True)
