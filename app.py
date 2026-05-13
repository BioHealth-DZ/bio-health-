import streamlit as st
import google.generativeai as genai

# جلب المفتاح بأمان من خزانة الأسرار
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("⚠️ يرجى إضافة المفتاح في قسم Secrets أولاً!")
    st.stop()

# إعدادات الموديل
def get_ai_response(prompt):
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(prompt).text
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

# واجهة الموقع
st.set_page_config(page_title="منصة البيوكيمياء والصحة", page_icon="🧪")
st.markdown('<h1 style="color: #2e7d32; text-align: center;">🧪 منصة البيوكيمياء والصحة الجزائرية</h1>', unsafe_allow_html=True)

menu = st.sidebar.selectbox("القائمة", ["📊 حاسبة الصحة", "🔬 المحلل البيوكيميائي"])

if menu == "📊 حاسبة الصحة":
    weight = st.number_input("الوزن (كغ)", 30, 200, 75)
    height = st.number_input("الطول (سم)", 100, 250, 170)
    if st.button("تحليل"):
        bmi = weight / ((height/100)**2)
        st.write(f"### مؤشر كتلة جسمك هو: {bmi:.1f}")
        # شرح النتيجة
        if bmi < 18.5: st.warning("نقص وزن")
        elif 18.5 <= bmi < 25: st.success("وزن مثالي")
        else: st.error("زيادة وزن")
        
        with st.spinner("جاري جلب نصيحة الذكاء الاصطناعي..."):
            st.info(get_ai_response(f"نصيحة بيوكيميائية قصيرة بالجزائرية لشخص كتلة جسمه {bmi:.1f}"))

elif menu == "🔬 المحلل البيوكيميائي":
    query = st.text_area("اطرح سؤالك العلمي:")
    if st.button("تحليل"):
        st.write(get_ai_response(query))
