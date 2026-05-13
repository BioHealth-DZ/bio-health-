import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="BioHealth DZ", page_icon="🧪", layout="wide")

# 2. تصميم الواجهة الواضح (خلفية بيضاء مريحة)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-title { color: #1b5e20; text-align: center; font-size: 2.5rem; font-weight: bold; padding: 20px; }
    .result-card { background-color: #f8f9fa; padding: 20px; border-radius: 15px; border: 1px solid #e0e0e0; color: #212529; }
    label { color: #1b5e20 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. نظام اللغات
translations = {
    "العربية": {
        "welcome": "مرحباً بك في BioHealth DZ", "name": "الاسم", "start": "دخول",
        "bmi_tab": "📊 حاسبة الوزن", "food_tab": "🥘 تحليل الأطباق",
        "weight": "الوزن (كغ)", "height": "الطول (سم)", "analyze": "تحليل",
        "food_prompt": "حلل طبق {} بيوكيمياياً. اذكر الإيجابيات والسلبيات (50/50) بالدراجة الجزائرية."
    },
    "Français": {
        "welcome": "Bienvenue sur BioHealth DZ", "name": "Nom", "start": "Entrer",
        "bmi_tab": "📊 IMC", "food_tab": "🥘 Nutrition",
        "weight": "Poids (kg)", "height": "Taille (cm)", "analyze": "Analyser",
        "food_prompt": "Analysez le plat {} (biochimie). Points positifs et négatifs (50/50) en français."
    },
    "English": {
        "welcome": "Welcome to BioHealth DZ", "name": "Name", "start": "Enter",
        "bmi_tab": "📊 BMI", "food_tab": "🥘 Food",
        "weight": "Weight (kg)", "height": "Height (cm)", "analyze": "Analyze",
        "food_prompt": "Analyze {} biochemically. Pros and cons (50/50) in English."
    }
}

# 4. دالة الذكاء الاصطناعي مع "الكاشف الآلي" لحل مشكلة NotFound
def get_ai_response(prompt):
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key: return "⚠️ Missing API Key"
    try:
        genai.configure(api_key=api_key)
        # كشف الموديلات المتاحة آلياً لتفادي خطأ 404
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # محاولة استخدام الموديلات الأكثر استقراراً أولاً
        target_model = next((m for m in models if "1.5-flash" in m or "pro" in m), models[0])
        
        model = genai.GenerativeModel(target_model)
        return model.generate_content(prompt).text
    except Exception as e:
        return f"❌ Connection Error: {str(e)}"

# 5. منطق الدخول
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="main-title">🧪 BioHealth DZ</div>', unsafe_allow_html=True)
    with st.form("login"):
        lang = st.selectbox("Language / اللغة", ["العربية", "Français", "English"])
        name = st.text_input("Name / الاسم")
        if st.form_submit_button("Start"):
            st.session_state.auth, st.session_state.lang, st.session_state.user = True, lang, name
            st.rerun()
else:
    T = translations[st.session_state.lang]
    st.sidebar.title(f"👤 {st.session_state.user}")
    menu = st.sidebar.radio("Menu", [T["bmi_tab"], T["food_tab"]])
    st.markdown(f'<h1 class="main-title">{T["welcome"]}</h1>', unsafe_allow_html=True)

    if menu == T["bmi_tab"]:
        w = st.number_input(T["weight"], 30.0, 200.0, 75.0)
        h = st.number_input(T["height"], 100.0, 250.0, 170.0)
        if st.button(T["analyze"]):
            bmi = w / ((h/100)**2)
            st.markdown(f'<div class="result-card"><h3>BMI: {bmi:.1f}</h3></div>', unsafe_allow_html=True)
            st.info(get_ai_response(f"Health advice for BMI {bmi:.1f} in {st.session_state.lang}"))

    elif menu == T["food_tab"]:
        dish = st.text_input("Dish Name")
        if st.button(T["analyze"]):
            with st.spinner("..."):
                res = get_ai_response(T["food_prompt"].format(dish))
                st.markdown(f'<div class="result-card">{res}</div>', unsafe_allow_html=True)

    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()
