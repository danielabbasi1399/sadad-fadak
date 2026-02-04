import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات صفحه
st.set_page_config(page_title="مدیریت سداد فدک", page_icon="📊", layout="wide")

# استایل CSS برای گرافیک
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

# تابع کمکی برای تبدیل متن به عدد
def n(v):
    try: return float(v) if v.strip() else 0.0
    except: return 0.0

# تابع برای خالی کردن تمام فیلدها بعد از ثبت
def clear_form():
    for key in st.session_state.keys():
        if key not in ['year', 'month', 'day']: # تاریخ را ریست نمی‌کنیم
            st.session_state[key] = ""

# --- بخش انتخاب تاریخ ---
now = jdatetime.datetime.now()
c_y, c_m, c_d = st.columns(3)
with c_y: year = st.selectbox("سال", [1403, 1404, 1405], index=1, key='year')
with c_m: 
    m_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    month = st.selectbox("ماه", range(1, 13), format_func=lambda x: m_names[x-1], index=now.month-1, key='month')
with c_d: day = st.selectbox("روز", range(1, 32), index=now.day-1, key='day')

shamsi_str = jdatetime.date(year, month, day).strftime('%Y/%m/%d')
st.success(f"🗓️ تاریخ انتخابی: {shamsi_str}")

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
        
        st.markdown("---")
        st.markdown("**📋 خلاصه تولید گلخانه ۱**")
        sum_s1, sum_g1 = n(s1an) + n(s1ra), n(g1an) + n(g1ra)
        st.write(f"جمع سوپر: {sum_s1} | جمع درجه: {sum_g1}")
        st.write(f"جمع کل گ۱: {sum_s1 + sum_g1}")

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
        
        st.markdown("---")
        st.markdown("**📋 خلاصه تولید گلخانه ۲**")
        sum_s2, sum_g2 = n(s2an) + n(s2g2), n(g2an) + n(g2g2)
        st.write(f"جمع سوپر: {sum_s2} | جمع درجه: {sum_g2}")
        st.write(f"جمع کل گ۲: {sum_s2 + sum_g2}")

with col3:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #27ae60;">🏘️ گلخانه ۳</div>', unsafe_allow_html=True)
        st.markdown("🔴 **بذر نیروین**")
        s3ni = st.text_input("سوپر    ", key="s3ni")
        g3ni = st.text_input("درجه    ", key="g3ni")
        t3ni = n(s3ni) + n(g3ni)
        st.write(f"جمع: {t3ni if t3ni > 0 else ''}")
        
        st.markdown("---")
        st.markdown("**📋 خلاصه تولید گلخانه ۳**")
        sum_s3, sum_g3 = n(s3ni), n(g3ni)
        st.write(f"جمع سوپر: {sum_s3} | جمع درجه: {sum_g3}")
        st.write(f"جمع کل گ۳: {sum_s3 + sum_g3}")
        st.write("")

# --- محاسبات آمار نهایی پایین صفحه ---
an_s = n(s1an) + n(s2an)
an_g = n(g1an) + n(g2an)
ra_s, ra_g = n(s1ra), n(g1ra)
g20_s, g20_g = n(s2g2), n(g2g2)
ni_s, ni_g = n(s3ni), n(g3ni)
total_s_all = an_s + ra_s + g20_s + ni_s
total_g_all = an_g + ra_g + g20_g + ni_g

st.divider()
st.subheader("📊 آمار تولید بر اساس نوع بذر")
c1, c2 = st.columns(2)
with c1:
    st.info(f"🟢 اندرومدا | کل: {an_s + an_g}")
    st.warning(f"🟠 جی ۲۰ | کل: {g20_s + g20_g}")
with c2:
    st.info(f"🟡 راگاراک | کل: {ra_s + ra_g}")
    st.warning(f"🔵 نیروین | کل: {ni_s + ni_g}")

st.markdown("---")
f1, f2, f3 = st.columns(3)
f1.metric("کل سوپر", total_s_all)
f2.metric("کل درجه", total_g_all)
f3.metric("جمع نهایی کل", total_s_all + total_g_all)

st.divider()

# دکمه ثبت با قابلیت پاک‌سازی خودکار
if st.button("🚀 ثبت نهایی و تخلیه فرم", use_container_width=True):
    # در اینجا کد ثبت در گوگل شیت شما اجرا می‌شود
    # ... (کد اتصال و آپدیت شیت)
    
    st.success("✅ اطلاعات ثبت شد و فرم خالی گردید.")
    # فراخوانی تابع پاک‌سازی
    clear_form()
    # ریفرش صفحه برای اعمال تغییرات
    st.rerun()
