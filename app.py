import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات صفحه
st.set_page_config(page_title="مدیریت سداد فدک", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: white !important;
        border-radius: 15px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
        padding: 20px !important;
    }
    .gh-header {
        font-size: 18px; font-weight: bold; padding: 8px; 
        border-radius: 8px; text-align: center; color: white; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 مدیریت هوشمند برداشت - سداد فدک")

conn = st.connection("gsheets", type=GSheetsConnection)

# مقداردهی اولیه به session_state برای جلوگیری از خطا
keys = ["s1an", "g1an", "s1ra", "g1ra", "s2an", "g2an", "s2g2", "g2g2", "s3ni", "g3ni"]
for k in keys:
    if k not in st.session_state:
        st.session_state[k] = ""

def n(v):
    try: return float(v) if v.strip() else 0.0
    except: return 0.0

# --- بخش انتخاب تاریخ ---
now = jdatetime.datetime.now()
c_y, c_m, c_d = st.columns(3)
year = c_y.selectbox("سال", [1403, 1404, 1405], index=1)
m_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
month = c_m.selectbox("ماه", range(1, 13), format_func=lambda x: m_names[x-1], index=now.month-1)
day = c_d.selectbox("روز", range(1, 32), index=now.day-1)

shamsi_str = jdatetime.date(year, month, day).strftime('%Y/%m/%d')
st.success(f"🗓️ تاریخ: {shamsi_str}")

st.divider()

# --- بخش ورودی‌ها ---
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #e74c3c;">🏘️ گلخانه ۱</div>', unsafe_allow_html=True)
        st.markdown("🔴 **اندرومدا**")
        s1an = st.text_input("سوپر", key="s1an")
        g1an = st.text_input("درجه", key="g1an")
        st.write(f"جمع: {n(s1an) + n(g1an) if n(s1an) + n(g1an) > 0 else ''}")
        st.markdown("---")
        st.markdown("🟡 **راگاراک**")
        s1ra = st.text_input("سوپر ", key="s1ra")
        g1ra = st.text_input("درجه ", key="g1ra")
        st.write(f"جمع: {n(s1ra) + n(g1ra) if n(s1ra) + n(g1ra) > 0 else ''}")
        st.markdown("---")
        st.write(f"**جمع کل گ۱:** {n(s1an) + n(s1ra) + n(g1an) + n(g1ra)}")

with col2:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #3498db;">🏘️ گلخانه ۲</div>', unsafe_allow_html=True)
        st.markdown("🔴 **اندرومدا**")
        s2an = st.text_input("سوپر  ", key="s2an")
        g2an = st.text_input("درجه  ", key="g2an")
        st.write(f"جمع: {n(s2an) + n(g2an) if n(s2an) + n(g2an) > 0 else ''}")
        st.markdown("---")
        st.markdown("🔴 **G20**")
        s2g2 = st.text_input("سوپر   ", key="s2g2")
        g2g2 = st.text_input("درجه   ", key="g2g2")
        st.write(f"جمع: {n(s2g2) + n(g2g2) if n(s2g2) + n(g2g2) > 0 else ''}")
        st.markdown("---")
        st.write(f"**جمع کل گ۲:** {n(s2an) + n(s2g2) + n(g2an) + n(g2g2)}")

with col3:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #27ae60;">🏘️ گلخانه ۳</div>', unsafe_allow_html=True)
        st.markdown("🔴 **نیروین**")
        s3ni = st.text_input("سوپر    ", key="s3ni")
        g3ni = st.text_input("درجه    ", key="g3ni")
        st.write(f"جمع: {n(s3ni) + n(g3ni) if n(s3ni) + n(g3ni) > 0 else ''}")
        st.markdown("---")
        st.write(f"**جمع کل گ۳:** {n(s3ni) + n(g3ni)}")

st.divider()

# --- محاسبات آمار بذرها ---
an_s = n(s1an) + n(s2an)
an_g = n(g1an) + n(g2an)
total_s_all = an_s + n(s1ra) + n(s2g2) + n(s3ni)
total_g_all = an_g + n(g1ra) + n(g2g2) + n(g3ni)

st.subheader("📊 آمار تولید بر اساس نوع بذر")
f1, f2, f3 = st.columns(3)
f1.metric("کل سوپر", total_s_all)
f2.metric("کل درجه", total_g_all)
f3.metric("جمع نهایی", total_s_all + total_g_all)

# --- دکمه ثبت و خالی کردن فرم ---
if st.button("🚀 ثبت نهایی و تخلیه فرم", use_container_width=True):
    try:
        # شبیه‌سازی ثبت (کد گوگل‌شیت شما اینجا قرار می‌گیرد)
        # updated_df = pd.concat([existing_data, new_data])
        # conn.update(data=updated_df)
        
        # خالی کردن فیلدها در session_state
        for k in keys:
            st.session_state[k] = ""
            
        st.success("✅ اطلاعات با موفقیت ثبت شد.")
        st.rerun() # بازنشانی صفحه
    except Exception as e:
        st.error(f"خطا در ثبت: {e}")
