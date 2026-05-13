import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="BioHealth DZ", page_icon="🧪", layout="wide")

# 2. التنسيق الإجباري (Force Styling)
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f4f8 !important; /* خلفية رمادية فاتحة جداً */
    }
    .main-header {
        background-color: #1b5e20;
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .info-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-right: 10px solid #2e7d32;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    label { font-weight: bold !important; color: #1b5e20 !important; font-size: 1.1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. دالة المحرك (AI Engine) - حل مشكلة 404
def call_ai(prompt):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # كشف الموديل المتاح تلقائياً
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        m_name = next((m for m in models if "flash" in m or "pro" in m), models[0])
        model = genai.GenerativeModel(m_name)
        return model.generate_content(prompt).text
    except Exception as e:
        return f"Error: {str(e)}"

# 4. نظام اللغات
translations = {
    "العربية": {
        "title": "🧪 منصة BioHealth DZ للبيوكيمياء",
        "bmi": "📊 حاسبة كتلة الجسم", "food": "🥘 تحليل الأطباق", "ask": "🔬 الأسئلة العلمية",
        "w": "الوزن (كغ)", "h": "الطول (سم)", "btn": "تحليل الآن",
        "food_p": "حلل طبق {} بيوكيمياياً. اذكر الإيجابيات والسلبيات (50/50) بالدراجة الجزائرية."
    },
    "Français": {
        "title": "🧪 Plateforme BioHealth DZ",
        "bmi": "📊 Calcul de l'IMC", "food": "🥘 Nutrition", "ask": "🔬 Questions Labo",
        "w": "Poids (kg)", "h": "Taille (cm)", "btn": "Analyser",
        "food_p": "Analysez le plat {} (biochimie). Points positifs et négatifs (50/50) en français."
    },
    "English": {
        "title": "🧪 BioHealth DZ Platform",
        "bmi": "📊 BMI Calculator", "food": "🥘 Food Science", "ask": "🔬 Science Questions",
        "w": "Weight (kg)", "h": "Height (cm)", "btn": "Analyze",
        "food_p": "Analyze {} biochemically. Pros and cons (50/50) in English."
    }
}

# 5. منطق الدخول
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="main-header"><h1>BioHealth DZ</h1></div>', unsafe_allow_html=True)
    with st.container():
        lang = st.selectbox("Language / اللغة", ["العربية", "Français", "English"])
        name = st.text_input("Name / الاسم")
        if st.button("Enter / دخول"):
            if name:
                st.session_state.auth, st.session_state.lang, st.session_state.user = True, lang, name
                st.rerun()
else:
    T = translations[st.session_state.lang]
    st.sidebar.markdown(f"### 👤 {st.session_state.user}")
    
    # استرجاع كل الخانات في القائمة الجانبية
    menu = st.sidebar.radio("القائمة الرئيسية", [T["bmi"], T["food"], T["ask"]])
    
    st.markdown(f'<div class="main-header"><h1>{T["title"]}</h1></div>', unsafe_allow_html=True)

    if menu == T["bmi"]:
        with st.container():
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1: weight = st.number_input(T["w"], 30.0, 200.0, 75.0)
            with c2: height = st.number_input(T["h"], 100.0, 250.0, 170.0)
            if st.button(T["btn"]):
                bmi = weight / ((height/100)**2)
                st.success(f"BMI: {bmi:.1f}")
                st.info(call_ai(f"Advice for BMI {bmi:.1f} in {st.session_state.lang}"))
            st.markdown('</div>', unsafe_allow_html=True)

    elif menu == T["food"]:
        with st.container():
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            dish = st.text_input("Dish Name / اسم الطبق")
            if st.button(T["btn"]):
                with st.spinner("..."):
                    res = call_ai(T["food_p"].format(dish))
                    st.write(res)
            st.markdown('</div>', unsafe_allow_html=True)

    elif menu == T["ask"]:
        with st.container():
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.subheader("🔬 " + T["ask"])
            query = st.text_area("Question?")
            if st.button(T["btn"]):
                with st.spinner("..."):
                    st.write(call_ai(f"Explain scientifically in {st.session_state.lang}: {query}"))
            st.markdown('</div>', unsafe_allow_html=True)

    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()
