import streamlit as st
import jdatetime

# تنظیمات صفحه
st.set_page_config(page_title="سداد فدک", layout="wide")

# استایل حداقلی فقط برای رنگ (بدون دستکاری ابعاد کادرها)
st.markdown("""
    <style>
    .gh-header { padding: 10px; border-radius: 10px; text-align: center; color: white; font-weight: bold; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# تابع تبدیل متن به عدد
def n(v):
    try: return float(v) if v else 0.0
    except: return 0.0

# مدیریت وضعیت فرم برای خالی کردن آن
if "reset_key" not in st.session_state:
    st.session_state.reset_key = 0

def clear_form():
    st.session_state.reset_key += 1

# --- هدر تاریخ ---
c1, c2, c3 = st.columns(3)
with c1: year = st.selectbox("سال", [1403, 1404, 1405])
with c2: month = st.selectbox("ماه", range(1, 13))
with c3: day = st.selectbox("روز", range(1, 32))

st.divider()

# کلید داینامیک برای ریست کردن تمام ورودی‌ها
rk = st.session_state.reset_key

# --- بخش اصلی گلخانه‌ها ---
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #e74c3c;">🏘️ گلخانه ۱</div>', unsafe_allow_html=True)
        st.write("🔴 **بذر اندرومدا**")
        s1an = st.text_input("سوپر", key=f"s1an_{rk}")
        g1an = st.text_input("درجه", key=f"g1an_{rk}")
        st.write(f"جمع بذر: {n(s1an) + n(g1an)}")
        st.divider()
        st.write("🟡 **بذر راگاراک**")
        s1ra = st.text_input("سوپر ", key=f"s1ra_{rk}")
        g1ra = st.text_input("درجه ", key=f"g1ra_{rk}")
        st.write(f"جمع بذر: {n(s1ra) + n(g1ra)}")
        st.divider()
        st.info(f"جمع کل گ۱: {n(s1an)+n(g1an)+n(s1ra)+n(g1ra)}")

with col2:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #3498db;">🏘️ گلخانه ۲</div>', unsafe_allow_html=True)
        st.write("🔴 **بذر اندرومدا**")
        s2an = st.text_input("سوپر  ", key=f"s2an_{rk}")
        g2an = st.text_input("درجه  ", key=f"g2an_{rk}")
        st.write(f"جمع بذر: {n(s2an) + n(g2an)}")
        st.divider()
        st.write("🔴 **بذر G20**")
        s2g2 = st.text_input("سوپر   ", key=f"s2g2_{rk}")
        g2g2 = st.text_input("درجه   ", key=f"g2g2_{rk}")
        st.write(f"جمع بذر: {n(s2g2) + n(g2g2)}")
        st.divider()
        st.info(f"جمع کل گ۲: {n(s2an)+n(g2an)+n(s2g2)+n(g2g2)}")

with col3:
    with st.container(border=True):
        st.markdown('<div class="gh-header" style="background-color: #27ae60;">🏘️ گلخانه ۳</div>', unsafe_allow_html=True)
        st.write("🔴 **بذر نیروین**")
        s3ni = st.text_input("سوپر    ", key=f"s3ni_{rk}")
        g3ni = st.text_input("درجه    ", key=f"g3ni_{rk}")
        st.write(f"جمع بذر: {n(s3ni) + n(g3ni)}")
        
        # ایجاد فاصله برای هم‌تراز شدن با بقیه (بدون کدهای مخرب)
        for _ in range(10): st.write("") 
        
        st.divider()
        st.info(f"جمع کل گ۳: {n(s3ni)+n(g3ni)}")

# --- محاسبات نهایی ---
st.divider()
total_s = n(s1an) + n(s1ra) + n(s2an) + n(s2g2) + n(s3ni)
total_g = n(g1an) + n(g1ra) + n(g2an) + n(g2g2) + n(g3ni)

f1, f2, f3 = st.columns(3)
f1.metric("کل سوپر", total_s)
f2.metric("کل درجه", total_g)
f3.metric("جمع نهایی", total_s + total_g)

# --- دکمه ثبت ---
if st.button("🚀 ثبت نهایی و تخلیه فرم", use_container_width=True):
    # اینجا فقط پیام موفقیت و ریست فرم را انجام می‌دهیم
    st.success("✅ اطلاعات با موفقیت ثبت شد.")
    clear_form()
    st.rerun()
