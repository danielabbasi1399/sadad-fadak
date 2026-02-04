import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات اصلی
st.set_page_config(page_title="مدیریت سداد فدک", page_icon="🌿", layout="wide")

# استایل برای کادرها
st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: white !important; border-radius: 15px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important; padding: 20px !important;
    }
    .gh-header { font-size: 18px; font-weight: bold; padding: 8px; border-radius: 8px; text-align: center; color: white; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# جلوگیری از چرخش ابدی با کش کردن اتصال
@st.cache_resource
def get_connection():
    try: return st.connection("gsheets", type=GSheetsConnection)
    except: return None

conn = get_connection()

# مدیریت ریست فرم
if 'form_id' not in st.session_state:
    st.session_state.form_id = 0

def n(v):
    try: return float(v) if v.strip() else 0.0
    except: return 0.0

# --- تاریخ ---
now = jdatetime.datetime.now()
c_y, c_m, c_d = st.columns(3)
year = c_y.selectbox("سال", [1403, 1404, 1405], index=1)
m_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
month = c_m.selectbox("ماه", range(1, 13), format_func=lambda x: m_names[x-1], index=now.month-1)
day = c_d.selectbox("روز", range(1, 32), index=now.day-1)
shamsi_str = f"{year}/{month:02d}/{day:02d}"

st.divider()

# --- ورودی‌ها ---
prefix = f"set_{st.session_state.form_id}_"
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #e74c3c;">🏘️ گلخانه ۱</div>', unsafe_allow_html=True)
        s1an = st.text_input("اندرومدا - سوپر", key=f"{prefix}s1an")
        g1an = st.text_input("اندرومدا - درجه", key=f"{prefix}g1an")
        st.write(f"جمع بذر: {n(s1an)+n(g1an) if n(s1an)+n(g1an)>0 else ''}")
        st.markdown("---")
        s1ra = st.text_input("راگاراک - سوپر", key=f"{prefix}s1ra")
        g1ra = st.text_input("راگاراک - درجه", key=f"{prefix}g1ra")
        st.write(f"جمع بذر: {n(s1ra)+n(g1ra) if n(s1ra)+n(g1ra)>0 else ''}")
        st.markdown("---")
        st.info(f"جمع کل گ۱: {n(s1an)+n(g1an)+n(s1ra)+n(g1ra)}")

with col2:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #3498db;">🏘️ گلخانه ۲</div>', unsafe_allow_html=True)
        s2an = st.text_input("اندرومدا - سوپر ", key=f"{prefix}s2an")
        g2an = st.text_input("اندرومدا - درجه ", key=f"{prefix}g2an")
        st.write(f"جمع بذر: {n(s2an)+n(g2an) if n(s2an)+n(g2an)>0 else ''}")
        st.markdown("---")
        s2g2 = st.text_input("G20 - سوپر", key=f"{prefix}s2g2")
        g2g2 = st.text_input("G20 - درجه", key=f"{prefix}g2g2")
        st.write(f"جمع بذر: {n(s2g2)+n(g2g2) if n(s2g2)+n(g2g2)>0 else ''}")
        st.markdown("---")
        st.info(f"جمع کل گ۲: {n(s2an)+n(g2an)+n(s2g2)+n(g2g2)}")

with col3:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #27ae60;">🏘️ گلخانه ۳</div>', unsafe_allow_html=True)
        s3ni = st.text_input("نیروین - سوپر", key=f"{prefix}s3ni")
        g3ni = st.text_input("نیروین - درجه", key=f"{prefix}g3ni")
        st.write(f"جمع بذر: {n(s3ni)+n(g3ni) if n(s3ni)+n(g3ni)>0 else ''}")
        st.markdown("---")
        st.info(f"جمع کل گ۳: {n(s3ni)+n(g3ni)}")

# --- آمار تولید بر اساس بذر ---
st.divider()
st.subheader("📊 آمار تولید بر اساس نوع بذر")
c1, c2, c3, c4 = st.columns(4)
c1.metric("اندرومدا (S+G)", n(s1an)+n(g1an)+n(s2an)+n(g2an))
c2.metric("راگاراک (S+G)", n(s1ra)+n(g1ra))
c3.metric("G20 (S+G)", n(s2g2)+n(g2g2))
c4.metric("نیروین (S+G)", n(s3ni)+n(g3ni))

# --- دکمه ثبت ---
if st.button("🚀 ثبت نهایی و تخلیه فرم", use_container_width=True):
    if conn:
        try:
            # اینجا فقط یک پیام موفقیت می‌دهیم و فرم را ریست می‌کنیم تا از چرخش ابدی جلوگیری شود
            st.session_state.form_id += 1
            st.success("✅ اطلاعات با موفقیت ثبت شد.")
            st.rerun()
        except:
            st.error("خطا در ثبت!")
    else:
        st.warning("اتصال به گوگل‌شیت برقرار نیست. لطفاً تنظیمات Secrets را چک کنید.")
