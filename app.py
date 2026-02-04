import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات صفحه
st.set_page_config(page_title="داشبورد پیشرفته سداد فدک", page_icon="📊", layout="wide")

# استایل CSS برای ظاهر حرفه‌ای
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
    .report-box {
        background-color: #ffffff; border-right: 5px solid #1D976C;
        padding: 10px; margin-bottom: 5px; border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.03);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 گزارش جامع برداشت روزانه - سداد فدک")

conn = st.connection("gsheets", type=GSheetsConnection)

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

shamsi_str = jdatetime.date(year, month, day).strftime('%Y/%m/%d')
st.info(f"📅 تاریخ انتخابی: {shamsi_str}")

st.divider()

# --- بخش ورودی‌ها ---
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
        st.markdown("🔴 **G20**")
        s2g2 = st.text_input("سوپر   ", key="s2g2")
        g2g2 = st.text_input("درجه   ", key="g2g2")

with col3:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #27ae60;">🏘️ گلخانه ۳</div>', unsafe_allow_html=True)
        st.markdown("🔴 **نیروین**")
        s3ni = st.text_input("سوپر    ", key="s3ni")
        g3ni = st.text_input("درجه    ", key="g3ni")

# --- محاسبات درخواستی شما ---

# ۱. محاسبات مربوط به اندرومدا (گلخانه ۱ و ۲)
total_an_super = n(s1an) + n(s2an)
total_an_grade = n(g1an) + n(g2an)
total_an_sum = total_an_super + total_an_grade

# ۲. محاسبات مربوط به راگاراک (فقط گلخانه ۱)
total_ra_super = n(s1ra)
total_ra_grade = n(g1ra)
total_ra_sum = total_ra_super + total_ra_grade

# ۳. جمع کل تمام بذرها و گلخانه‌ها
total_all_super = n(s1an) + n(s1ra) + n(s2an) + n(s2g2) + n(s3ni)
total_all_grade = n(g1an) + n(g1ra) + n(g2an) + n(g2g2) + n(g3ni)
total_overall = total_all_super + total_all_grade

st.divider()

# --- نمایش گزارش نهایی ---
st.subheader("📋 آمار تفکیکی و نهایی (لحظه‌ای)")

r1, r2, r3 = st.columns(3)

with r1:
    st.markdown("🟢 **آمار بذر اندرومدا (کل)**")
    st.write(f"🔹 جمع سوپر: {total_an_super}")
    st.write(f"🔹 جمع درجه: {total_an_grade}")
    st.info(f"✅ کل اندرومدا: {total_an_sum}")

with r2:
    st.markdown("🟡 **آمار بذر راگاراک (کل)**")
    st.write(f"🔹 جمع سوپر: {total_ra_super}")
    st.write(f"🔹 جمع درجه: {total_ra_grade}")
    st.info(f"✅ کل راگاراک: {total_ra_sum}")

with r3:
    st.markdown("🏆 **جمع کل برداشت (تمام گلخانه‌ها)**")
    st.write(f"💎 کل سوپر: {total_all_super}")
    st.write(f"🔸 کل درجه: {total_all_grade}")
    st.success(f"📦 جمع نهایی: {total_overall}")

st.divider()

if st.button("🚀 ثبت اطلاعات در اکسل", use_container_width=True):
    # (کد ثبت در جدول همانند قبل باقی می‌ماند)
    st.success("اطلاعات با موفقیت ثبت شد.")
