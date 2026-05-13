import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والتصميم الفاخر (إعادة كل الميزات البصرية)
st.set_page_config(page_title="منصة البيوكيمياء والصحة الجزائرية", page_icon="🧪", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)), 
                    url('https://images.unsplash.com/photo-1576086213369-97a306d36557?q=80&w=2000');
        background-size: cover;
    }
    .main-title { color: #1b5e20; text-align: center; font-size: 2.8rem; font-weight: bold; margin-bottom: 20px; }
    .result-card {
        background-color: white; padding: 25px; border-radius: 15px;
        border-right: 10px solid #2e7d32; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    .info-box { background-color: #e8f5e9; border-radius: 10px; padding: 15px; margin-top: 15px; border: 1px solid #2e7d32; }
    .stButton>button { background: #2e7d32; color: white; border-radius: 25px; width: 100%; font-weight: bold; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# 2. جلب المفتاح من Secrets (الخزانة السرية)
API_KEY = st.secrets.get("GEMINI_API_KEY")

def get_ai_response(prompt):
    if not API_KEY:
        return "⚠️ يرجى التأكد من وضع GEMINI_API_KEY في إعدادات Secrets."
    try:
        genai.configure(api_key=API_KEY)
        
        # حل مشكلة 404: البحث عن الموديل المتاح في حسابك آلياً
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if not available_models:
            return "❌ لم يتم العثور على موديل متاح."
        
        # نختار 'gemini-pro' إذا وجد، وإلا نختار أول موديل متاح
        selected_model = 'models/gemini-pro' if 'models/gemini-pro' in available_models else available_models[0]
        
        model = genai.GenerativeModel(selected_model)
        return model.generate_content(prompt).text
    except Exception as e:
        return f"❌ خطأ فني: {str(e)}"

# 3. واجهة المستخدم الرئيسية
st.markdown('<p class="main-title">🧪 منصة البيوكيمياء والصحة الجزائرية</p>', unsafe_allow_html=True)

menu = st.sidebar.selectbox("القائمة الرئيسية", ["📊 حاسبة الصحة والوزن", "🔬 المحلل البيوكيميائي", "🥘 كيمياء المطبخ"])

if menu == "📊 حاسبة الصحة والوزن":
    st.header("⚖️ تقييم الحالة الجسدية")
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("الوزن (كغ)", 30, 200, 75)
        height = st.number_input("الطول (سم)", 100, 250, 170)
        age = st.number_input("العمر", 5, 100, 25)
    with col2:
        gender = st.radio("الجنس", ["ذكر", "أنثى"])
        status = st.selectbox("الحالة الصحية", ["طبيعي", "سكري", "ضغط دم", "حامل", "مرضعة"])
    
    if st.button("إجراء التحليل البيوكيميائي"):
        bmi = weight / ((height/100)**2)
        
        # تحديد لون وحالة النتيجة
        if bmi < 18.5: meaning, color = "نقص في الوزن: جسمك يحتاج لزيادة المغذيات الأساسية.", "#fbc02d"
        elif 18.5 <= bmi < 25: meaning, color = "وزن مثالي: تبارك الله، أنت في النطاق الصحي.", "#2e7d32"
        elif 25 <= bmi < 30: meaning, color = "زيادة في الوزن: بداية خروج عن التوازن البيوكيميائي.", "#ef6c00"
        else: meaning, color = "سمنة: قد تؤثر على الوظائف الحيوية، ينصح بالمتابعة.", "#c62828"

        st.markdown(f"""
        <div class="result-card">
            <h3 style="color:{color};">مؤشر كتلة الجسم (BMI): {bmi:.1f}</h3>
            <div class="info-box">
                <b>💡 ماذا تعني هذه النتيجة؟</b><br>
                {meaning}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("جاري جلب نصيحة الخبير الذكي..."):
            res = get_ai_response(f"أنا {gender} عمري {age} وحالتي {status} بكتلة جسم {bmi:.1f}. انصحني بالجزائرية نصيحة صحية.")
            st.info(res)

elif menu == "🔬 المحلل البيوكيميائي":
    st.header("🔬 المختبر الافتراضي")
    query = st.text_area("اطرح سؤالك العلمي (مثلاً: تأثير السكر على الدم):")
    if st.button("تحليل الآن"):
        with st.spinner("جاري التحليل..."):
            st.write(get_ai_response(f"اشرح لي بالجزائرية وببساطة: {query}"))

elif menu == "🥘 كيمياء المطبخ":
    st.header("🥘 التحليل الغذائي للأطباق")
    dish = st.text_input("اسم الطبق الجزائري (مثلاً: كسكس، محاجب):")
    if st.button("كشف الأسرار"):
        with st.spinner("جاري فحص المكونات..."):
            st.write(get_ai_response(f"حلل طبق {dish} كيميائياً وغذائياً بالجزائرية"))
