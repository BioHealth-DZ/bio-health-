import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="منصة البيوكيمياء والصحة الجزائرية", page_icon="🧪", layout="wide")

# التصميم (CSS)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                    url('https://images.unsplash.com/photo-1576086213369-97a306d36557?q=80&w=2000'); background-size: cover; }
    .main-title { color: #1b5e20; text-align: center; font-size: 2.8rem; font-weight: bold; }
    .result-card { background-color: white; padding: 20px; border-radius: 15px; border-right: 10px solid #2e7d32; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .info-box { background-color: #e8f5e9; border-radius: 10px; padding: 15px; margin-top: 10px; border: 1px solid #2e7d32; }
    .stButton>button { background: #2e7d32; color: white; border-radius: 25px; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 🔑 ضع مفتاحك الجديد هنا ---
API_KEY = "AIzaSyBKvFfji6lkjNNYxraI9OS0pZK5_bIt-Ew"
# -----------------------------

def get_ai_response(prompt):
    if "الجـديد" in API_KEY or not API_KEY:
        return "⚠️ يرجى تحديث مفتاح API في السطر 22."
    try:
        genai.configure(api_key=API_KEY.strip())
        
        # --- السحر هنا: اكتشاف الموديل الشغال آلياً ---
        model_to_use = None
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model_to_use = m.name
                break # نأخذ أول موديل يدعم التوليد
        
        if not model_to_use:
            return "❌ لم يتم العثور على موديلات فعالة في حسابك."
            
        model = genai.GenerativeModel(model_to_use)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ خطأ في الاتصال: {str(e)}"

# واجهة المستخدم
st.markdown('<p class="main-title">🧪 منصة البيوكيمياء والصحة الجزائرية</p>', unsafe_allow_html=True)
menu = st.sidebar.selectbox("القائمة الرئيسية", ["📊 حاسبة الصحة والوزن", "🔬 المحلل البيوكيميائي", "🥘 كيمياء المطبخ"])

if menu == "📊 حاسبة الصحة والوزن":
    st.header("⚖️ تقييم الحالة الجسدية")
    c1, c2 = st.columns(2)
    with c1:
        weight = st.number_input("الوزن (كغ)", 30, 200, 75)
        height = st.number_input("الطول (سم)", 100, 250, 170)
        age = st.number_input("العمر", 5, 100, 25)
    with c2:
        gender = st.radio("الجنس", ["ذكر", "أنثى"])
        status = st.selectbox("الحالة الصحية", ["طبيعي", "سكري", "ضغط دم", "حامل", "مرضعة"])
    
    if st.button("إجراء التحليل البيوكيميائي"):
        bmi = weight / ((height/100)**2)
        if bmi < 18.5: meaning, color = "نقص في الوزن: تحتاج لتغذية مكثفة.", "#fbc02d"
        elif 18.5 <= bmi < 25: meaning, color = "وزن مثالي: صحتك في أمان، حافظ على التوازن.", "#2e7d32"
        elif 25 <= bmi < 30: meaning, color = "زيادة في الوزن: بداية الخطر، تحرك أكثر.", "#ef6c00"
        else: meaning, color = "سمنة: خطر على الصحة البيوكيمائية، استشر طبيباً.", "#c62828"

        st.markdown(f"""
        <div class="result-card">
            <h3 style="color:{color};">كتلة الجسم (BMI): {bmi:.1f}</h3>
            <div class="info-box">
                <b>💡 ماذا تعني هذه النتيجة؟</b><br>
                هذا المؤشر يربط وزنك بطولك. نتيجتك تشير إلى: <b>{meaning}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
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
