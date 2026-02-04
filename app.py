import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات پیشرفته صفحه
st.set_page_config(page_title="داشبورد سداد فدک", page_icon="🌿", layout="wide")

# استایل CSS برای گرافیک بالا
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: white !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        padding: 25px !important;
    }
    .gh-header {
        font-size: 20px; font-weight: bold; margin-bottom: 15px;
        padding: 10px; border-radius: 10px; text-align: center; color: white;
    }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3em;
        background: linear-gradient(90deg, #1D976C 0%, #93F9B9 100%);
        color: white; font-weight: bold; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚜 مدیریت هوشمند برداشت - سداد فدک")

conn = st.connection("gsheets", type=GSheetsConnection)

def n(v):
    try: return float(v) if v.strip() else 0.0
    except: return 0.0

# --- انتخاب تاریخ ---
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
        st.markdown("🔴 **اندرومدا**")
        s1an = st.text_input("سوپر", key="s1an")
        g1an = st.text_input("درجه", key="g1an")
        st.markdown("---")
        st.markdown("🟡 **راگاراک**")
        s1ra = st.text_input("سوپر", key="s1ra")
        g1ra = st.text_input("درجه", key="g1ra")

with col2:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #3498db;">🏘️ گلخانه ۲</div>', unsafe_allow_html=True)
        st.markdown("🔴 **اندرومدا**")
        s2an = st.text_input("سوپر", key="s2an")
        g2an = st.text_input("درجه", key="g2an")
        st.markdown("---")
        st.markdown("🔴 **G20**")
        s2g2 = st.text_input("سوپر", key="s2g2")
        g2g2 = st.text_input("درجه", key="g2g2")

with col3:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #27ae60;">🏘️ گلخانه ۳</div>', unsafe_allow_html=True)
        st.markdown("🔴 **نیروین**")
        s3ni = st.text_input("سوپر", key="s3ni")
        g3ni = st.text_input("درجه", key="g3ni")

# --- محاسبه مقادیر کل ---
total_s1 = n(s1an) + n(s1ra)
total_g1 = n(g1an) + n(g1ra)

total_s2 = n(s2an) + n(s2g2)
total_g2 = n(g2an) + n(g2g2)

total_s3 = n(s3ni)
total_g3 = n(g3ni)

st.divider()
st.subheader("📊 آمار لحظه‌ای برداشت امروز (به تفکیک گلخانه)")

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown("**گلخانه ۱**")
    st.write(f"💎 سوپر: {total_s1}")
    st.write(f"🔸 درجه: {total_g1}")
    st.info(f"📦 جمع کل گ۱: {total_s1 + total_g1}")

with m2:
    st.markdown("**گلخانه ۲**")
    st.write(f"💎 سوپر: {total_s2}")
    st.write(f"🔸 درجه: {total_g2}")
    st.info(f"📦 جمع کل گ۲: {total_s2 + total_g2}")

with m3:
    st.markdown("**گلخانه ۳**")
    st.write(f"💎 سوپر: {total_s3}")
    st.write(f"🔸 درجه: {total_g3}")
    st.info(f"📦 جمع کل گ۳: {total_s3 + total_g3}")

st.divider()

# دکمه ثبت
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
        st.error("خطا در ثبت!")

st.subheader("📋 سوابق اخیر")
st.dataframe(conn.read(worksheet="Sheet1", ttl=0).dropna(how="all"), use_container_width=True)
