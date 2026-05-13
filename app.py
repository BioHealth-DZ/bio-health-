import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والتصميم الفاخر
st.set_page_config(page_title="BioHealth DZ | منصة الصحة", page_icon="🧪", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.92)), 
                    url('https://www.transparenttextures.com/patterns/cubes.png');
        background-color: #f0f4f8;
    }
    .main-title { 
        color: #1b5e20; text-align: center; font-size: 3rem; font-weight: bold; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1); padding: 20px;
    }
    .result-card {
        background-color: white; padding: 25px; border-radius: 20px;
        border-right: 10px solid #2e7d32; box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        color: #212529; line-height: 1.6;
    }
    .stButton>button {
        background: linear-gradient(45deg, #2e7d32, #43a047); color: white;
        border-radius: 30px; border: none; font-weight: bold; width: 100%; height: 3.5em;
    }
    .sidebar-user { text-align: center; padding: 10px; background: #e8f5e9; border-radius: 15px; margin-bottom: 20px; }
    label { color: #1b5e20 !important; font-weight: bold !important; font-size: 1.1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام اللغات المتكامل
translations = {
    "العربية": {
        "welcome": "مرحباً بك في منصة BioHealth DZ", "name": "الاسم الكامل", "email": "البريد الإلكتروني",
        "start": "دخول للمنصة", "bmi_tab": "📊 حاسبة كتلة الجسم", "food_tab": "🥘 تحليل الأطباق",
        "weight": "الوزن (كغ)", "height": "الطول (سم)", "analyze": "إجراء التحليل الآن",
        "food_prompt": "حلل طبق {} بيوكيمياياً. اذكر الإيجابيات والسلبيات الصحية بكل حياد ونقد علمي (50/50) بالدراجة الجزائرية.",
        "logout": "تسجيل الخروج"
    },
    "Français": {
        "welcome": "Bienvenue sur BioHealth DZ", "name": "Nom Complet", "email": "E-mail",
        "start": "Entrer", "bmi_tab": "📊 Calcul de l'IMC", "food_tab": "🥘 Analyse Nutritionnelle",
        "weight": "Poids (kg)", "height": "Taille (cm)", "analyze": "Lancer l'analyse",
        "food_prompt": "Analysez le plat {} (biochimie). Points positifs et négatifs avec neutralité (50/50) en français.",
        "logout": "Déconnexion"
    },
    "English": {
        "welcome": "Welcome to BioHealth DZ", "name": "Full Name", "email": "Email Address",
        "start": "Enter Platform", "bmi_tab": "📊 BMI Calculator", "food_tab": "🥘 Food Analysis",
        "weight": "Weight (kg)", "height": "Height (cm)", "analyze": "Run Analysis",
        "food_prompt": "Analyze {} biochemically. Pros and cons with scientific neutrality (50/50) in English.",
        "logout": "Logout"
    }
}

# 3. دالة الذكاء الاصطناعي الذكية (حل مشكلة 404 نهائياً)
def get_ai_response(prompt):
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key: return "⚠️ Missing API Key"
    try:
        genai.configure(api_key=api_key)
        # البحث عن أي موديل متاح
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        selected_model = next((m for m in available_models if "1.5-flash" in m or "pro" in m), available_models[0])
        model = genai.GenerativeModel(selected_model)
        return model.generate_content(prompt).text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# 4. إدارة الجلسة والترحيب
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<h1 class="main-title">🧪 BioHealth DZ</h1>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div style="max-width:600px; margin:auto; background:white; padding:30px; border-radius:20px; box-shadow:0 10px 30px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
        lang = st.selectbox("اختر اللغة / Language", ["العربية", "Français", "English"])
        T = translations[lang]
        u_name = st.text_input(T["name"])
        u_email = st.text_input(T["email"])
        if st.button(T["start"]):
            if u_name:
                st.session_state.auth, st.session_state.lang, st.session_state.user = True, lang, u_name
                st.rerun()
            else: st.warning("يرجى إدخال الاسم")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    T = translations[st.session_state.lang]
    # القائمة الجانبية الأنيقة
    st.sidebar.markdown(f'<div class="sidebar-user"><h3>👤 {st.session_state.user}</h3></div>', unsafe_allow_html=True)
    menu = st.sidebar.radio("Navigate", [T["bmi_tab"], T["food_tab"]])
    if st.sidebar.button(T["logout"]):
        st.session_state.auth = False
        st.rerun()

    st.markdown(f'<p class="main-title">{T["welcome"]}</p>', unsafe_allow_html=True)

    if menu == T["bmi_tab"]:
        st.subheader("⚖️ " + T["bmi_tab"])
        col1, col2 = st.columns(2)
        with col1: w = st.number_input(T["weight"], 30.0, 200.0, 75.0)
        with col2: h = st.number_input(T["height"], 100.0, 250.0, 170.0)
        
        if st.button(T["analyze"]):
            bmi = w / ((h/100)**2)
            st.markdown(f'<div class="result-card"><h2>BMI: {bmi:.1f}</h2>', unsafe_allow_html=True)
            with st.spinner("..."):
                advice = get_ai_response(f"Advice for BMI {bmi:.1f} in {st.session_state.lang}")
                st.write(advice)
            st.markdown('</div>', unsafe_allow_html=True)

    elif menu == T["food_tab"]:
        st.subheader("🥘 " + T["food_tab"])
        dish = st.text_input("Dish Name / اسم الطبق")
        if st.button(T["analyze"]):
            with st.spinner("Analyzing..."):
                res = get_ai_response(T["food_prompt"].format(dish))
                st.markdown(f'<div class="result-card">{res}</div>', unsafe_allow_html=True)
