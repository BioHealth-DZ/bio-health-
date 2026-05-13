import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة والتصميم
st.set_page_config(page_title="منصة البيوكيمياء والصحة الجزائرية", page_icon="🧪", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), 
                    url('https://images.unsplash.com/photo-1576086213369-97a306d36557?q=80&w=2000'); background-size: cover; }
    .main-title { color: #1b5e20; text-align: center; font-size: 2.5rem; font-weight: bold; border-bottom: 2px solid #2e7d32; }
    .result-card { background-color: white; padding: 20px; border-radius: 15px; border-right: 10px solid #2e7d32; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    .stButton>button { background-color: #2e7d32; color: white; border-radius: 20px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 🔑 ضع مفتاحك في السطر 22 بالأسفل ---
API_KEY = "AIzaSyD9WBNpqzGhS47RfFrw0YqPb40TbB8dX9M"
# ---------------------------------------

def get_ai_response(prompt):
    if "ضع_مفتاحك" in API_KEY or not API_KEY:
        return "⚠️ يرجى وضع مفتاح API Key في السطر 22 أولاً."
    try:
        genai.configure(api_key=API_KEY.strip())
        
        # --- تعديل سحري: البحث عن أي موديل متاح في حسابك ---
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # محاولة اختيار أفضل موديل متاح
        if 'models/gemini-1.5-flash' in available_models:
            model_name = 'gemini-1.5-flash'
        elif 'models/gemini-pro' in available_models:
            model_name = 'gemini-pro'
        else:
            model_name = available_models[0] # اختر أول واحد متاح إذا لم يجد الأسماء المعروفة
            
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ خطأ فني: {str(e)}. تأكد من تفعيل Gemini API في حسابك."

# واجهة المستخدم
st.markdown('<p class="main-title">🧪 منصة البيوكيمياء والصحة الجزائرية</p>', unsafe_allow_html=True)

menu = st.sidebar.selectbox("القائمة الرئيسية", ["📊 حاسبة الصحة", "🔬 المحلل البيوكيميائي", "🥘 كيمياء المطبخ"])

if menu == "📊 حاسبة الصحة":
    st.header("⚖️ تقييم الحالة الجسدية")
    c1, c2 = st.columns(2)
    with c1:
        weight = st.number_input("الوزن (كغ)", 30, 200, 75)
        height = st.number_input("الطول (سم)", 100, 250, 170)
        age = st.number_input("العمر", 5, 100, 25)
    with c2:
        gender = st.radio("الجنس", ["ذكر", "أنثى"])
        status = st.selectbox("الحالة الصحية", ["طبيعي", "سكري", "ضغط دم", "حامل", "مرضعة"])
    
    if st.button("إجراء التحليل"):
        bmi = weight / ((height/100)**2)
        st.markdown(f'<div class="result-card"><h3>كتلة الجسم: {bmi:.1f}</h3></div>', unsafe_allow_html=True)
        with st.spinner("جاري استشارة الذكاء الاصطناعي..."):
            res = get_ai_response(f"أنا {gender} عمري {age} وحالتي {status} بكتلة جسم {bmi:.1f}. انصحني بالجزائرية.")
            st.info(res)

elif menu == "🔬 المحلل البيوكيميائي":
    query = st.text_area("اطرح سؤالك العلمي:")
    if st.button("تحليل الآن"):
        st.write(get_ai_response(f"اشرح لي بالجزائرية: {query}"))

elif menu == "🥘 كيمياء المطبخ":
    dish = st.text_input("اسم الطبق الجزائري:")
    if st.button("كشف الأسرار"):
        st.write(get_ai_response(f"حلل طبق {dish} كيميائياً بالجزائرية"))
