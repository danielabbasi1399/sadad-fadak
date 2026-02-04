import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات اصلی
st.set_page_config(page_title="مدیریت سداد فدک", page_icon="🌿", layout="wide")

# استایل CSS بهینه شده (فقط برای رنگ و فونت)
st.markdown("""
    <style>
    [data-testid="stVerticalBlock"] > div > div > div > div {
        /* این کد باعث می‌شود تمام ستون‌ها در یک ردیف هم‌قد شوند */
        height: 100%;
    }
    .main-card {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        height: 750px; /* ارتفاع ثابت و بلند برای هر سه */
        display: flex;
        flex-direction: column;
    }
    .gh-header {
        font-size: 18px; font-weight: bold; padding: 10px; 
        border-radius: 8px; text-align: center; color: white; margin-bottom: 15px;
    }
    .bottom-info {
        margin-top: auto; /* چسباندن اطلاعات جمع به کف کادر */
        background-color: #f0f8ff;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'form_id' not in st.session_state:
    st.session_state.form_id = 0

def n(v):
    try: return float(v) if v.strip() else 0.0
    except: return 0.0

# --- بخش تاریخ ---
now = jdatetime.datetime.now()
c_y, c_m, c_d = st.columns(3)
year = c_y.selectbox("سال", [1403, 1404, 1405], index=1)
month = c_m.selectbox("ماه", range(1, 13), index=now.month-1)
day = c_d.selectbox("روز", range(1, 32), index=now.day-1)

st.divider()

# --- بخش اصلی ورودی‌ها ---
prefix = f"v{st.session_state.form_id}_"
col1, col2, col3 = st.columns(3, gap="medium")

# گلخانه ۱
with col1:
    st.markdown(f"""
    <div class="main-card">
        <div class="gh-header" style="background-color: #e74c3c;">🏘️ گلخانه ۱</div>
        <p style="color:red; font-weight:bold;">🔴 بذر اندرومدا</p>
    </div>
    """, unsafe_allow_html=True)
    s1an = st.text_input("سوپر", key=f"{prefix}s1an")
    g1an = st.text_input("درجه", key=f"{prefix}g1an")
    st.write(f"جمع بذر: {n(s1an)+n(g1an)}")
    
    st.markdown('<p style="color:orange; font-weight:bold;">🟡 بذر راگاراک</p>', unsafe_allow_html=True)
    s1ra = st.text_input("سوپر ", key=f"{prefix}s1ra")
    g1ra = st.text_input("درجه ", key=f"{prefix}g1ra")
    st.write(f"جمع بذر: {n(s1ra)+n(g1ra)}")
    
    st.info(f"جمع کل گ۱: {n(s1an)+n(s1ra)+n(g1an)+n(g1ra)}")

# گلخانه ۲
with col2:
    st.markdown(f"""
    <div class="main-card">
        <div class="gh-header" style="background-color: #3498db;">🏘️ گلخانه ۲</div>
        <p style="color:red; font-weight:bold;">🔴 بذر اندرومدا</p>
    </div>
    """, unsafe_allow_html=True)
    s2an = st.text_input("سوپر  ", key=f"{prefix}s2an")
    g2an = st.text_input("درجه  ", key=f"{prefix}g2an")
    st.write(f"جمع بذر: {n(s2an)+n(g2an)}")
    
    st.markdown('<p style="color:red; font-weight:bold;">🔴 بذر G20</p>', unsafe_allow_html=True)
    s2g2 = st.text_input("سوپر   ", key=f"{prefix}s2g2")
    g2g2 = st.text_input("درجه   ", key=f"{prefix}g2g2")
    st.write(f"جمع بذر: {n(s2g2)+n(g2g2)}")
    
    st.info(f"جمع کل گ۲: {n(s2an)+n(s2g2)+n(g2an)+n(g2g2)}")

# گلخانه ۳
with col3:
    st.markdown(f"""
    <div class="main-card">
        <div class="gh-header" style="background-color: #27ae60;">🏘️ گلخانه ۳</div>
        <p style="color:red; font-weight:bold;">🔴 بذر نیروین</p>
    </div>
    """, unsafe_allow_html=True)
    s3ni = st.text_input("سوپر    ", key=f"{prefix}s3ni")
    g3ni = st.text_input("درجه    ", key=f"{prefix}g3ni")
    st.write(f"جمع بذر: {n(s3ni)+n(g3ni)}")
    
    # ایجاد فاصله بصری برای هم‌تراز شدن با بقیه
    for _ in range(7): st.write("") 
    
    st.info(f"جمع کل گ۳: {n(s3ni)+n(g3ni)}")

# --- آمار تولید ---
st.divider()
total_s = n(s1an) + n(s1ra) + n(s2an) + n(s2g2) + n(s3ni)
total_g = n(g1an) + n(g1ra) + n(g2an) + n(g2g2) + n(g3ni)

st.subheader("📊 آمار تولید بر اساس نوع بذر")
f1, f2, f3 = st.columns(3)
f1.metric("کل فلفل سوپر", total_s)
f2.metric("کل فلفل درجه", total_g)
f3.metric("جمع نهایی کل", total_s + total_g)

if st.button("🚀 ثبت نهایی و تخلیه فرم", use_container_width=True):
    st.session_state.form_id += 1
    st.rerun()
