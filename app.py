import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="دليلك الصحي الجزائري", page_icon="🧪")

st.title("🧪 منصة البيوكيمياء والصحة الجزائرية")
st.markdown("---")

# القائمة الجانبية
menu = st.sidebar.selectbox("اختر الخدمة", ["حاسبة الوزن والماكروز", "تحليل المكونات (بيوكيمياء)", "نصيحة اليوم"])

if menu == "حاسبة الوزن والماكروز":
    st.header("📊 حساب الوزن المثالي والاحتياج الغذائي")
    
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("الوزن (كغ)", min_value=40, max_value=200, value=70)
        height = st.number_input("الطول (سم)", min_value=120, max_value=220, value=170)
    with col2:
        age = st.number_input("العمر", min_value=15, max_value=100, value=25)
        gender = st.radio("الجنس", ["ذكر", "أنثى"])

    if st.button("احسب النتائج"):
        bmi = weight / ((height/100)**2)
        st.subheader(f"مؤشر كتلة الجسم: {bmi:.2f}")
        if bmi < 18.5: st.warning("وزن ناقص - تحتاج لزيادة السعرات")
        elif 18.5 <= bmi < 25: st.success("وزن مثالي - حافظ عليه")
        else: st.error("زيادة في الوزن - تحتاج لبرنامج غذائي")
        
        calories = weight * 24 * 1.2
        st.info(f"احتياجك التقريبي للمحافظة على الوزن: {calories:.0f} سعرة")
        st.write(f"🥩 البروتين: {weight * 1.8:.1f} غرام")

elif menu == "تحليل المكونات (بيوكيمياء)":
    st.header("🔬 التحليل العلمي للمكونات")
    item = st.text_input("اكتب اسم المادة (مثلاً: الكرياتين)")
    if item:
        st.info(f"سيتم تحليل {item} كيميائياً في التحديث القادم!")

st.markdown("---")
st.caption("تم التطوير بمساعدة الذكاء الاصطناعي - متخصص بيوكيمياء جزائري")
