import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات صفحه
st.set_page_config(page_title="مدیریت سداد فدک", page_icon="🌿", layout="wide")

# استایل CSS برای قفل کردن ابعاد کادرها
st.markdown("""
    <style>
    /* قفل کردن ارتفاع کادرها برای برابری مطلق */
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: white !important;
        border-radius: 15px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
        padding: 20px !important;
        height: 600px !important; /* ارتفاع ثابت */
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
    }
    
    /* استایل تیتر گلخانه‌ها */
    .gh-header {
        font-size: 18px; font-weight: bold; padding: 10px; 
        border-radius: 8px; text-align: center; color: white; margin-bottom: 15px;
    }

    /* چسباندن بخش جمع کل به کف کادر */
    .bottom-section {
        margin-top: auto; /* این خط باعث می‌شود بخش جمع به پایین‌ترین نقطه کادر بچسبد */
        padding-top: 10px;
        border-top: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

if 'form_id' not in st.session_state:
    st.session_state.form_id = 0

def n(v):
    try: return float(v) if v.strip() else 0.0
    except: return 0.0

# --- انتخاب تاریخ ---
now = jdatetime.datetime.now()
c_y, c_m, c_d = st.columns(3)
year = c_y.selectbox("سال", [1403, 1404, 1405], index=1)
month = c_m.selectbox("ماه", range(1, 13), index=now.month-1)
day = c_d.selectbox("روز", range(1, 32), index=now.day-1)

st.divider()

# --- بخش ورودی‌ها ---
prefix = f"v{st.session_state.form_id}_"
col1, col2, col3 = st.columns(3)

# گلخانه ۱
with col1:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #e74c3c;">🏘️ گلخانه ۱</div>', unsafe_allow_html=True)
        st.markdown("🔴 **بذر اندرومدا**")
        s1an = st.text_input("سوپر", key=f"{prefix}s1an")
        g1an = st.text_input("درجه", key=f"{prefix}g1an")
        st.write(f"جمع: {n(s1an)+n(g1an) if n(s1an)+n(g1an)>0 else ''}")
        st.markdown("---")
        st.markdown("🟡 **بذر راگاراک**")
        s1ra = st.text_input("سوپر ", key=f"{prefix}s1ra")
        g1ra = st.text_input("درجه ", key=f"{prefix}g1ra")
        st.write(f"جمع: {n(s1ra)+n(g1ra) if n(s1ra)+n(g1ra)>0 else ''}")
        
        # بخش چسبیده به کف
        st.markdown('<div class="bottom-section">', unsafe_allow_html=True)
        st.write("**جمع کل گلخانه ۱:**")
        st.info(f"سوپر: {n(s1an)+n(s1ra)} | درجه: {n(g1an)+n(g1ra)}")
        st.markdown('</div>', unsafe_allow_html=True)

# گلخانه ۲
with col2:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #3498db;">🏘️ گلخانه ۲</div>', unsafe_allow_html=True)
        st.markdown("🔴 **بذر اندرومدا**")
        s2an = st.text_input("سوپر  ", key=f"{prefix}s2an")
        g2an = st.text_input("درجه  ", key=f"{prefix}g2an")
        st.write(f"جمع: {n(s2an)+n(g2an) if n(s2an)+n(g2an)>0 else ''}")
        st.markdown("---")
        st.markdown("🔴 **بذر G20**")
        s2g2 = st.text_input("سوپر   ", key=f"{prefix}s2g2")
        g2g2 = st.text_input("درجه   ", key=f"{prefix}g2g2")
        st.write(f"جمع: {n(s2g2)+n(g2g2) if n(s2g2)+n(g2g2)>0 else ''}")
        
        # بخش چسبیده به کف
        st.markdown('<div class="bottom-section">', unsafe_allow_html=True)
        st.write("**جمع کل گلخانه ۲:**")
        st.info(f"سوپر: {n(s2an)+n(s2g2)} | درجه: {n(g2an)+n(g2g2)}")
        st.markdown('</div>', unsafe_allow_html=True)

# گلخانه ۳
with col3:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #27ae60;">🏘️ گلخانه ۳</div>', unsafe_allow_html=True)
        st.markdown("🔴 **بذر نیروین**")
        s3ni = st.text_input("سوپر    ", key=f"{prefix}s3ni")
        g3ni = st.text_input("درجه    ", key=f"{prefix}g3ni")
        st.write(f"جمع: {n(s3ni)+n(g3ni) if n(s3ni)+n(g3ni)>0 else ''}")
        
        # بخش چسبیده به کف (در اینجا فاصله خالی خودکار ایجاد می‌شود)
        st.markdown('<div class="bottom-section">', unsafe_allow_html=True)
        st.write("**جمع کل گلخانه ۳:**")
        st.info(f"سوپر: {n(s3ni)} | درجه: {n(g3ni)}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- محاسبات نهایی پایین صفحه ---
total_s = n(s1an) + n(s1ra) + n(s2an) + n(s2g2) + n(s3ni)
total_g = n(g1an) + n(g1ra) + n(g2an) + n(g2g2) + n(g3ni)

st.divider()
st.subheader("📊 آمار تولید بر اساس نوع بذر")
f1, f2, f3 = st.columns(3)
f1.metric("کل فلفل سوپر", total_s)
f2.metric("کل فلفل درجه", total_g)
f3.metric("جمع نهایی کل", total_s + total_g)

if st.button("🚀 ثبت نهایی و تخلیه فرم", use_container_width=True):
    st.session_state.form_id += 1
    st.success("✅ اطلاعات ثبت و فرم خالی شد.")
    st.rerun()
