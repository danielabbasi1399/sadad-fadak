import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import jdatetime

# تنظیمات ظاهری
st.set_page_config(page_title="سداد فدک", page_icon="🌶️", layout="wide")

st.title("ثبت برداشت روزانه - سداد فدک")

conn = st.connection("gsheets", type=GSheetsConnection)

# خواندن داده‌ها
try:
    existing_data = conn.read(worksheet="Sheet1", ttl=0)
    existing_data = existing_data.dropna(how="all")
except Exception:
    columns = [
        "تاریخ", "روز هفته", 
        "اندرومدا ۱ (S)", "اندرومدا ۱ (G)", "راگاراک ۱ (S)", "راگاراک ۱ (G)",
        "اندرومدا ۲ (S)", "اندرومدا ۲ (G)", "G20 2 (S)", "G20 2 (G)",
        "نیروین ۳ (S)", "نیروین ۳ (G)"
    ]
    existing_data = pd.DataFrame(columns=columns)

# تابع کمکی برای محاسبات آنی
def get_val(v):
    try:
        return float(v) if v.strip() else 0.0
    except:
        return 0.0

# --- انتخاب تاریخ ---
st.subheader("📅 انتخاب زمان")
now = jdatetime.datetime.now()
c_y, c_m, c_d = st.columns(3)
with c_y: year = st.selectbox("سال", [1403, 1404, 1405], index=1)
with c_m: 
    m_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    month = st.selectbox("ماه", range(1, 13), format_func=lambda x: m_names[x-1], index=now.month-1)
with c_d: day = st.selectbox("روز", range(1, 32), index=now.day-1)

try:
    p_date = jdatetime.date(year, month, day)
    shamsi_str = p_date.strftime('%Y/%m/%d')
    g_date = p_date.togregorian()
    w_map = {0: "دوشنبه", 1: "سه‌شنبه", 2: "چهارشنبه", 3: "پنج‌شنبه", 4: "جمعه", 5: "شنبه", 6: "یکشنبه"}
    current_day = w_map[g_date.weekday()]
    st.info(f"📅 روز هفته: {current_day} | تاریخ: {shamsi_str}")
except ValueError:
    st.error("تاریخ نامعتبر است!")
    current_day = None

st.divider()

# --- فرم ثبت با نمایش جمع آنی هر بذر ---
with st.form(key="final_form_with_totals"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.error("🏘️ گلخانه ۱")
        st.markdown("**بذر اندرومدا**")
        s1_an = st.text_input("سوپر", key="s1an", value="")
        g1_an = st.text_input("درجه", key="g1an", value="")
        st.markdown("---")
        st.markdown("**بذر راگاراک**")
        s1_ra = st.text_input("سوپر", key="s1ra", value="")
        g1_ra = st.text_input("درجه", key="g1ra", value="")

    with col2:
        st.info("🏘️ گلخانه ۲")
        st.markdown("**بذر اندرومدا**")
        s2_an = st.text_input("سوپر", key="s2an", value="")
        g2_an = st.text_input("درجه", key="g2an", value="")
        st.markdown("---")
        st.markdown("**بذر G20**")
        s2_g2 = st.text_input("سوپر", key="s2g2", value="")
        g2_g2 = st.text_input("درجه", key="g2g2", value="")

    with col3:
        st.success("🏘️ گلخانه ۳")
        st.markdown("**بذر نیروین**")
        s3_ni = st.text_input("سوپر", key="s3ni", value="")
        g3_ni = st.text_input("درجه", key="g3ni", value="")
        st.markdown("---")
        st.caption("برداشت گلخانه ۳")

    submitted = st.form_submit_button("🚀 ثبت نهایی و محاسبه جمع کل")

# عملیات ذخیره و نمایش جمع کل
if submitted and current_day:
    # مقادیر عددی برای محاسبه جمع
    v1an = get_val(s1_an) + get_val(g1_an)
    v1ra = get_val(s1_ra) + get_val(g1_ra)
    v2an = get_val(s2_an) + get_val(g2_an)
    v2g2 = get_val(s2_g2) + get_val(g2_g2)
    v3ni = get_val(s3_ni) + get_val(g3_ni)

    new_row = pd.DataFrame([{
        "تاریخ": shamsi_str, "روز هفته": current_day,
        "اندرومدا ۱ (S)": get_val(s1_an), "اندرومدا ۱ (G)": get_val(g1_an),
        "راگاراک ۱ (S)": get_val(s1_ra), "راگاراک ۱ (G)": get_val(g1_ra),
        "اندرومدا ۲ (S)": get_val(s2_an), "اندرومدا ۲ (G)": get_val(g2_an),
        "G20 2 (S)": get_val(s2_g2), "G20 2 (G)": get_val(g2_g2),
        "نیروین ۳ (S)": get_val(s3_ni), "نیروین ۳ (G)": get_val(g3_ni)
    }])
    
    try:
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
        st.balloons()
        # نمایش جمع‌های کل در کادر سبز نهایی
        st.success(f"✅ اطلاعات با موفقیت ثبت شد.")
        st.write(f"📊 **خلاصه برداشت امروز:**")
        st.write(f"گلخانه ۱: (اندرومدا: {v1an}) - (راگاراک: {v1ra})")
        st.write(f"گلخانه ۲: (اندرومدا: {v2an}) - (G20: {v2g2})")
        st.write(f"گلخانه ۳: (نیروین: {v3ni})")
        
        st.cache_data.clear()
        # برای مشاهده نتایج توسط کاربر، rerun را کمی با تاخیر یا دستی انجام می‌دهیم
    except Exception as e:
        st.error(f"خطا در ثبت: {e}")

st.divider()
st.dataframe(existing_data, use_container_width=True)
