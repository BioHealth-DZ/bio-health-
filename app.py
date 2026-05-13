import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة البيوكيمياء والصحة الجزائرية", page_icon="🧪", layout="wide")

# 2. تصميم الواجهة (CSS)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                    url('https://images.unsplash.com/photo-1576086213369-97a306d36557?auto=format&fit=crop&q=80&w=2000');
        background-size: cover;
    }
    .main-title { color: #1b5e20; text-align: center; font-size: 2.8rem; font-weight: bold; }
    .result-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border-right: 8px solid #2e7d32; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stButton>button { background: #2e7d32; color: white; border-radius: 25px; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 🔑 ضع مفتاحك في السطر 28 بالأسفل ---
API_KEY = "AIzaSyD9WBNpqzGhS47RfFrw0YqPb40TbB8dX9M"
# ---------------------------------------

# دالة الاتصال بالذكاء الاصطناعي
def get_ai_response(prompt):
    if "ضـع_مفـتاحك" in API_KEY or not API_KEY:
        return "⚠️ يرجى لصق مفتاح API في السطر 28 أولاً."
    try:
        genai.configure(api_key=API_KEY.strip())
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(prompt).text
    except:
        try:
            model = genai.GenerativeModel('gemini-pro')
            return model.generate_content(prompt).text
        except Exception as e:
            return f"❌ خطأ في الاتصال. تأكد من صلاحية المفتاح. {str(e)}"

# واجهة المستخدم
st.markdown('<p class="main-title">🧪 منصة البيوكيمياء والصحة الجزائرية</p>', unsafe_allow_html=True)

menu = st.sidebar.selectbox("القائمة الرئيسية", ["📊 حاسبة الصحة", "🔬 المحلل البيوكيميائي", "🥘 كيمياء المطبخ"])

if menu == "📊 حاسبة الصحة":
    st.header("⚖️ تقييم الحالة الجسدية")
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("الوزن (كغ)", 30, 200, 75)
        height = st.number_input("الطول (سم)", 100, 250, 170)
        age = st.number_input("العمر", 5, 100, 25)
    with col2:
        gender = st.radio("الجنس", ["ذكر", "أنثى"])
        health_status = st.selectbox("الحالة الصحية", ["طبيعي", "سكري", "ضغط دم", "حامل", "مرضعة"])
    
    if st.button("إجراء التحليل"):
        bmi = weight / ((height/100)**2)
        st.markdown(f'<div class="result-card"><h3>كتلة الجسم: {bmi:.1f}</h3></div>', unsafe_allow_html=True)
        with st.spinner("جاري جلب النصيحة..."):
            res = get_ai_response(f"أنا {gender} عمري {age} وحالتي {health_status} بكتلة جسم {bmi:.1f}. انصحني بالجزائرية.")
            st.info(res)

elif menu == "🔬 المحلل البيوكيميائي":
    query = st.text_area("اطرح سؤالك العلمي:")
    if st.button("تحليل الآن"):
        st.write(get_ai_response(f"اشرح لي بالجزائرية: {query}"))

elif menu == "🥘 كيمياء المطبخ":
    dish = st.text_input("اسم الطبق الجزائري:")
    if st.button("كشف الأسرار"):
        st.write(get_ai_response(f"حلل طبق {dish} كيميائياً بالجزائرية"))
