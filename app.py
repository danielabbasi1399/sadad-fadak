import streamlit as st
import jdatetime

# تنظیمات اصلی
st.set_page_config(page_title="مدیریت سداد فدک", layout="wide")

# تابع تبدیل متن به عدد (برای محاسبات)
def n(v):
    try: return float(v.strip()) if v.strip() else 0.0
    except: return 0.0

# مدیریت ریست شدن فرم بعد از ثبت
if "reset_key" not in st.session_state:
    st.session_state.reset_key = 0

rk = st.session_state.reset_key

st.title("📊 مدیریت هوشمند برداشت - سداد فدک")

# --- بخش تاریخ ---
c_y, c_m, c_d = st.columns(3)
with c_y: year = st.selectbox("سال", [1403, 1404, 1405], index=1)
with c_m: month = st.selectbox("ماه", range(1, 13), index=10) # بهمن
with c_d: day = st.selectbox("روز", range(1, 32), index=13) # ۱۴ بهمن

st.divider()

# --- بخش ورودی‌ها ---
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("🏘️ گلخانه ۱")
        st.write("🔴 **بذر اندرومدا**")
        s1an = st.text_input("سوپر", key=f"s1an_{rk}")
        g1an = st.text_input("درجه", key=f"g1an_{rk}")
        st.write(f"جمع: {n(s1an) + n(g1an)}")
        
        st.divider()
        
        st.write("🟡 **بذر راگاراک**")
        s1ra = st.text_input("سوپر ", key=f"s1ra_{rk}")
        g1ra = st.text_input("درجه ", key=f"g1ra_{rk}")
        st.write(f"جمع: {n(s1ra) + n(g1ra)}")
        
        st.divider()
        st.info(f"جمع کل گ۱: {n(s1an)+n(g1an)+n(s1ra)+n(g1ra)}")

with col2:
    with st.container(border=True):
        st.subheader("🏘️ گلخانه ۲")
        st.write("🔴 **بذر اندرومدا**")
        s2an = st.text_input("سوپر  ", key=f"s2an_{rk}")
        g2an = st.text_input("درجه  ", key=f"g2an_{rk}")
        st.write(f"جمع: {n(s2an) + n(g2an)}")
        
        st.divider()
        
        st.write("🔴 **بذر G20**")
        s2g2 = st.text_input("سوپر   ", key=f"s2g2_{rk}")
        g2g2 = st.text_input("درجه   ", key=f"g2g2_{rk}")
        st.write(f"جمع: {n(s2g2) + n(g2g2)}")
        
        st.divider()
        st.info(f"جمع کل گ۲: {n(s2an)+n(g2an)+n(s2g2)+n(g2g2)}")

with col3:
    with st.container(border=True):
        st.subheader("🏘️ گلخانه ۳")
        st.write("🔴 **بذر نیروین**")
        s3ni = st.text_input("سوپر    ", key=f"s3ni_{rk}")
        g3ni = st.text_input("درجه    ", key=f"g3ni_{rk}")
        st.write(f"جمع: {n(s3ni) + n(g3ni)}")
        
        # --- تراز دستی گلخانه ۳ ---
        # اگر دیدی کادر ۳ کوتاه است، تعداد دفعات st.write("") را کم یا زیاد کن
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        # -----------------------
        
        st.divider()
        st.info(f"جمع کل گ۳: {n(s3ni)+n(g3ni)}")

# --- آمار تولید بر اساس نوع بذر ---
st.divider()
st.subheader("📊 آمار تولید بر اساس نوع بذر")
total_s = n(s1an) + n(s1ra) + n(s2an) + n(s2g2) + n(s3ni)
total_g = n(g1an) + n(g1ra) + n(g2an) + n(g2g2) + n(g3ni)

f1, f2, f3 = st.columns(3)
f1.metric("کل سوپر", total_s)
f2.metric("کل درجه", total_g)
f3.metric("جمع نهایی کل", total_s + total_g)

st.divider()

# دکمه ثبت و تخلیه فرم
if st.button("🚀 ثبت اطلاعات و تخلیه فرم", use_container_width=True):
    # اینجا می‌توانی کد ثبت در گوگل‌شیت را اضافه کنی
    st.success("✅ اطلاعات با موفقیت ثبت شد.")
    st.session_state.reset_key += 1 # تخلیه فرم
    st.rerun()
