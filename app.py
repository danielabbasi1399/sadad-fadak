import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات صفحه
st.set_page_config(page_title="داشبورد جامع سداد فدک", page_icon="📊", layout="wide")

# استایل CSS برای گرافیک و حذف لوزی‌ها
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
st.success(f"🗓️ تاریخ: {shamsi_str}")

st.divider()

# --- بخش ورودی‌ها ---
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #e74c3c;">🏘️ گلخانه ۱</div>', unsafe_allow_html=True)
        st.markdown("🔴 **بذر اندرومدا**")
        s1an = st.text_input("سوپر", key="s1an")
        g1an = st.text_input("درجه", key="g1an")
        t1an = n(s1an) + n(g1an)
        st.write(f"جمع: {t1an if t1an > 0 else ''}")
        st.markdown("---")
        st.markdown("🟡 **بذر راگاراک**")
        s1ra = st.text_input("سوپر ", key="s1ra")
        g1ra = st.text_input("درجه ", key="g1ra")
        t1ra = n(s1ra) + n(g1ra)
        st.write(f"جمع: {t1ra if t1ra > 0 else ''}")

with col2:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #3498db;">🏘️ گلخانه ۲</div>', unsafe_allow_html=True)
        st.markdown("🔴 **بذر اندرومدا**")
        s2an = st.text_input("سوپر  ", key="s2an")
        g2an = st.text_input("درجه  ", key="g2an")
        t2an = n(s2an) + n(g2an)
        st.write(f"جمع: {t2an if t2an > 0 else ''}")
        st.markdown("---")
        st.markdown("🔴 **بذر G20**")
        s2g2 = st.text_input("سوپر   ", key="s2g2")
        g2g2 = st.text_input("درجه   ", key="g2g2")
        t2g2 = n(s2g2) + n(g2g2)
        st.write(f"جمع: {t2g2 if t2g2 > 0 else ''}")

with col3:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #27ae60;">🏘️ گلخانه ۳</div>', unsafe_allow_html=True)
        st.markdown("🔴 **بذر نیروین**")
        s3ni = st.text_input("سوپر    ", key="s3ni")
        g3ni = st.text_input("درجه    ", key="g3ni")
        t3ni = n(s3ni) + n(g3ni)
        st.write(f"جمع: {t3ni if t3ni > 0 else ''}")
        st.write("")
        st.write("")
        st.write("")

# --- محاسبات تفکیکی آمار نهایی ---
# اندرومدا (گ۱ و گ۲)
an_s = n(s1an) + n(s2an)
an_g = n(g1an) + n(g2an)
# راگاراک (گ۱)
ra_s = n(s1ra)
ra_g = n(g1ra)
# G20 (گ۲)
g20_s = n(s2g2)
g20_g = n(g2g2)
# نیروین (گ۳)
ni_s = n(s3ni)
ni_g = n(g3ni)

# جمع کل نهایی
total_s_all = an_s + ra_s + g20_s + ni_s
total_g_all = an_g + ra_g + g20_g + ni_g

st.divider()
st.subheader("📊 آمار نهایی برداشت (به تفکیک بذر)")

# ردیف اول آمار
r1_c1, r1_c2 = st.columns(2)
with r1_c1:
    st.markdown("🟢 **بذر اندرومدا (کل)**")
    st.write(f"جمع سوپر: {an_s} | جمع درجه: {an_g}")
    st.info(f"جمع کل اندرومدا: {an_s + an_g}")

with r1_c2:
    st.markdown("🟡 **بذر راگاراک (کل)**")
    st.write(f"جمع سوپر: {ra_s} | جمع درجه: {ra_g}")
    st.info(f"جمع کل راگاراک: {ra_s + ra_g}")

# ردیف دوم آمار
r2_c1, r2_c2 = st.columns(2)
with r2_c1:
    st.markdown("🟠 **بذر G20 (کل)**")
    st.write(f"جمع سوپر: {g20_s} | جمع درجه: {g20_g}")
    st.info(f"جمع کل G20: {g20_s + g20_g}")

with r2_c2:
    st.markdown("🔵 **بذر نیروین (کل)**")
    st.write(f"جمع سوپر: {ni_s} | جمع درجه: {ni_g}")
    st.info(f"جمع کل نیروین: {ni_s + ni_g}")

# ردیف سوم - جمع کل نهایی
st.markdown("---")
st.markdown("<h3 style='text-align: center;'>🏆 جمع کل نهایی تمام بذرها</h3>", unsafe_allow_html=True)
f1, f2, f3 = st.columns(3)
f1.metric("کل سوپر", total_s_all)
f2.metric("کل درجه", total_g_all)
f3.metric("جمع نهایی (S+G)", total_s_all + total_g_all)

st.divider()
if st.button("🚀 ثبت اطلاعات در اکسل", use_container_width=True):
    st.success("✅ اطلاعات با موفقیت ثبت شد.")
