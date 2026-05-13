import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="منصة البيوكيمياء والصحة الجزائرية", page_icon="🧪", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                    url('https://images.unsplash.com/photo-1576086213369-97a306d36557?q=80&w=2000');
        background-size: cover;
    }
    .main-title { color: #1b5e20; text-align: center; font-size: 2.8rem; font-weight: bold; }
    .result-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border-right: 10px solid #2e7d32; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .info-box { background-color: #e8f5e9; border-radius: 10px; padding: 15px; margin-top: 10px; border: 1px solid #2e7d32; }
    .stButton>button { background: #2e7d32; color: white; border-radius: 25px; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 🔑 تنبيه: يجب وضع مفتاح جديد تماماً هنا ---
API_KEY = "AIzaSyBKvFfji6lkjNNYxraI9OS0pZK5_bIt-Ew"
# ----------------------------------------------

def get_ai_response(prompt):
    if "الجـديد" in API_KEY or not API_KEY:
        return "⚠️ تنبيه: مفتاحك القديم معطل. يرجى إصدار مفتاح جديد من Google AI Studio ووضعه في السطر 25."
    try:
        genai.configure(api_key=API_KEY.strip())
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(prompt).text
    except Exception as e:
        return f"❌ خطأ فني: {str(e)}. يرجى مراجعة مفتاح API الخاص بك."

# واجهة المستخدم
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
        
        # تحليل النتيجة وشرحها
        if bmi < 18.5:
            meaning = "نقص في الوزن: جسمك يحتاج لتغذية مكثفة وغنية بالبروتينات."
            color = "#fbc02d"
        elif 18.5 <= bmi < 25:
            meaning = "وزن مثالي: أنت في النطاق الصحي، حافظ على هذا التوازن."
            color = "#2e7d32"
        elif 25 <= bmi < 30:
            meaning = "زيادة في الوزن: بداية الخروج عن النطاق الصحي، ينصح بممارسة الرياضة."
            color = "#ef6c00"
        else:
            meaning = "سمنة: قد تؤثر على وظائفك الحيوية، ينصح باستشارة مختص."
            color = "#c62828"

        st.markdown(f"""
        <div class="result-card">
            <h3 style="color:{color};">كتلة الجسم (BMI): {bmi:.1f}</h3>
            <div class="info-box">
                <b>ماذا تعني هذه النتيجة؟</b><br>
                {meaning}
            </div>
            <p style="font-size: 0.9rem; margin-top: 10px; color: #555;">
            * مؤشر كتلة الجسم هو مقياس عالمي يربط بين الوزن والطول لتحديد كمية الدهون التقريبية في الجسم.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("جاري جلب نصائح الخبير..."):
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
