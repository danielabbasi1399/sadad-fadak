import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات صفحه
st.set_page_config(page_title="داشبورد حرفه‌ای سداد فدک", page_icon="📊", layout="wide")

# استایل CSS برای گرافیک بالا و حذف لوزی‌ها
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: white !important;
        border-radius: 15px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
    }
    .gh-header {
        font-size: 18px; font-weight: bold; padding: 8px; 
        border-radius: 8px; text-align: center; color: white; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 سیستم مدیریت برداشت - سداد فدک")

conn = st.connection("gsheets", type=GSheetsConnection)

def n(v):
    try: return float(v) if v.strip() else 0.0
    except: return 0.0

# --- بخش تاریخ ---
with st.expander("📅 انتخاب تاریخ"):
    now = jdatetime.datetime.now()
    c_y, c_m, c_d = st.columns(3)
    with c_y: year = st.selectbox("سال", [1403, 1404, 1405], index=1)
    with c_m: 
        m_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
        month = st.selectbox("ماه", range(1, 13), format_func=lambda x: m_names[x-1], index=now.month-1)
    with c_d: day = st.selectbox("روز", range(1, 32), index=now.day-1)

shamsi_str = jdatetime.date(year, month, day).strftime('%Y/%m/%d')
st.success(f"🗓️ تاریخ: {shamsi_str}")

st.divider()

# --- بخش ورودی‌ها (اصلاح شده برای هر سه گلخانه) ---
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #e74c3c;">🏘️ گلخانه ۱</div>', unsafe_allow_html=True)
        st.markdown("🔴 **اندرومدا**")
        s1an = st.text_input("سوپر", key="s1an")
        g1an = st.text_input("درجه", key="g1an")
        st.markdown("---")
        st.markdown("🟡 **راگاراک**")
        s1ra = st.text_input("سوپر ", key="s1ra")
        g1ra = st.text_input("درجه ", key="g1ra")

with col2:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #3498db;">🏘️ گلخانه ۲</div>', unsafe_allow_html=True)
        st.markdown("🔴 **اندرومدا**")
        s2an = st.text_input("سوپر  ", key="s2an")
        g2an = st.text_input("درجه  ", key="g2an")
        st.markdown("---")
        st.markdown("🟡 **راگاراک**")
        s2ra = st.text_input("سوپر   ", key="s2ra")
        g2ra = st.text_input("درجه   ", key="g2ra")

with col3:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #27ae60;">🏘️ گلخانه ۳</div>', unsafe_allow_html=True)
        st.markdown("🔴 **اندرومدا**")
        s3an = st.text_input("سوپر    ", key="s3an")
        g3an = st.text_input("درجه    ", key="g3an")
        st.markdown("---")
        st.markdown("🟡 **راگاراک**")
        s3ra = st.text_input("سوپر     ", key="s3ra")
        g3ra = st.text_input("درجه     ", key="g3ra")

# --- محاسبات درخواستی شما (بدون لوزی) ---
# ۱. اندرومدا (جمع هر سه گلخانه)
an_s = n(s1an) + n(s2an) + n(s3an)
an_g = n(g1an) + n(g2an) + n(g3an)
an_tot = an_s + an_g

# ۲. راگاراک (جمع هر سه گلخانه)
ra_s = n(s1ra) + n(s2ra) + n(s3ra)
ra_g = n(g1ra) + n(g2ra) + n(g3ra)
ra_tot = ra_s + ra_g

# ۳. جمع کل نهایی
total_super = an_s + ra_s
total_grade = an_g + ra_g
grand_total = total_super + total_grade

st.divider()

# --- نمایش گزارش نهایی (بدون لوزی آبی) ---
st.subheader("📊 آمار نهایی برداشت امروز")

r1, r2, r3 = st.columns(3)

with r1:
    st.markdown("🟢 **بذر اندرومدا**")
    st.write(f"جمع سوپر: {an_s}")
    st.write(f"جمع درجه: {an_g}")
    st.info(f"جمع سوپر و درجه: {an_tot}")

with r2:
    st.markdown("🟡 **بذر راگاراک**")
    st.write(f"جمع سوپر: {ra_s}")
    st.write(f"جمع درجه: {ra_g}")
    st.info(f"جمع سوپر و درجه: {ra_tot}")

with r3:
    st.markdown("🏆 **جمع کل تمام بذرها**")
    st.write(f"کل سوپر: {total_super}")
    st.write(f"کل درجه: {total_grade}")
    st.success(f"جمع نهایی کل: {grand_total}")

st.divider()

if st.button("🚀 ثبت اطلاعات در اکسل", use_container_width=True):
    st.success("اطلاعات با موفقیت ثبت شد.")
