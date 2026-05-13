import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="دليلك الصحي الجزائري", page_icon="🧪")

# --- ضع مفتاحك هنا ---
API_KEY = "ضـع_كـود_AIza_الخـاص_بـك_هنـا" 
# -----------------------

if API_KEY != "ضـع_كـود_AIza_الخـاص_بـك_هنـا":
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')

st.title("🧪 منصة البيوكيمياء والصحة الجزائرية")
st.markdown("---")

menu = st.sidebar.selectbox("اختر الخدمة", ["حاسبة الوزن والماكروز", "تحليل المكونات (ذكاء اصطناعي)", "كيمياء الأكل الجزائري"])

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
        calories = weight * 24 * 1.2
        st.info(f"احتياجك اليومي: {calories:.0f} سعرة")

elif menu == "تحليل المكونات (ذكاء اصطناعي)":
    st.header("🔬 المحلل البيوكيميائي الذكي")
    user_input = st.text_input("اسأل عن تأثير أي مادة كيميائية أو دواء:")
    if st.button("حلل الآن"):
        if "AIza" not in API_KEY:
            st.error("لم تضع مفتاح الـ API بشكل صحيح!")
        else:
            with st.spinner("جاري التحليل..."):
                prompt = f"أنت خبير بيوكيمياء. اشرح بلهجة جزائرية بسيطة التأثير العلمي لـ {user_input}"
                response = model.generate_content(prompt)
                st.success("النتيجة العلمية:")
                st.write(response.text)

elif menu == "كيمياء الأكل الجزائري":
    st.header("🥘 تحليل المطبخ الجزائري")
    st.write("هذا القسم سيخبرك بمكونات أطباقنا كيميائياً قريباً!")

st.markdown("---")
st.caption("تم التطوير بمساعدة الذكاء الاصطناعي - متخصص بيوكيمياء جزائري 🇩🇿")
