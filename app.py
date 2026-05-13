import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="BioHealth DZ", page_icon="🧪", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6 !important; }
    .header-box {
        background: linear-gradient(135deg, #1b5e20, #2e7d32);
        color: white; padding: 30px; border-radius: 20px;
        text-align: center; margin-bottom: 25px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .card {
        background: white; padding: 25px; border-radius: 15px;
        border-right: 10px solid #2e7d32; box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    label { font-weight: bold !important; color: #1b5e20 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. دالة الذكاء الاصطناعي
def ask_ai(prompt):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        m_name = next((m for m in models if "flash" in m or "pro" in m), models[0])
        model = genai.GenerativeModel(m_name)
        return model.generate_content(prompt).text
    except Exception as e:
        return f"Error: {str(e)}"

# 3. القاموس واللغات
translations = {
    "العربية": {
        "title": "منصة BioHealth DZ للبيوكيمياء",
        "bmi_tab": "📊 حاسبة الوزن والحالة الصحية", "food_tab": "🥘 تحليل الأطباق", "lab_tab": "🔬 المختبر العلمي",
        "age": "العمر", "gender": "الجنس", "male": "ذكر", "female": "أنثى",
        "weight": "الوزن (كغ)", "height": "الطول (سم)",
        "chronic": "الأمراض المزمنة", "diabetes": "سكري", "pressure": "ضغط دم", "none": "لا يوجد",
        "special": "حالات خاصة (للنساء)", "pregnant": "حامل", "nursing": "مرضعة",
        "btn": "تحليل الحالة الآن", "logout": "خروج"
    },
    "Français": {
        "title": "Plateforme BioHealth DZ",
        "bmi_tab": "📊 IMC & État de Santé", "food_tab": "🥘 Nutrition", "lab_tab": "🔬 Labo",
        "age": "Âge", "gender": "Sexe", "male": "Homme", "female": "Femme",
        "weight": "Poids (kg)", "height": "Taille (cm)",
        "chronic": "Maladies Chroniques", "diabetes": "Diabète", "pressure": "Tension", "none": "Aucun",
        "special": "États Spéciaux (Femmes)", "pregnant": "Enceinte", "nursing": "Allaitante",
        "btn": "Analyser l'état", "logout": "Déconnexion"
    }
}

# 4. منطق الدخول
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="header-box"><h1>🧪 BioHealth DZ</h1></div>', unsafe_allow_html=True)
    lang = st.selectbox("Language / اللغة", ["العربية", "Français"])
    name = st.text_input("Name / الاسم")
    if st.button("Start / دخول"):
        if name:
            st.session_state.auth, st.session_state.lang, st.session_state.user = True, lang, name
            st.rerun()
else:
    T = translations[st.session_state.lang]
    st.sidebar.markdown(f"### 👤 {st.session_state.user}")
    menu = st.sidebar.radio("Menu", [T["bmi_tab"], T["food_tab"], T["lab_tab"]])
    
    st.markdown(f'<div class="header-box"><h1>{T["title"]}</h1></div>', unsafe_allow_html=True)

    if menu == T["bmi_tab"]:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1: age = st.number_input(T["age"], 1, 100, 25)
            with col2: gender = st.selectbox(T["gender"], [T["male"], T["female"]])
            with col3: weight = st.number_input(T["weight"], 30.0, 200.0, 70.0)
            
            col4, col5 = st.columns(2)
            with col4: height = st.number_input(T["height"], 100.0, 250.0, 170.0)
            with col5: chronic = st.multiselect(T["chronic"], [T["diabetes"], T["pressure"]], default=[])
            
            # خيارات خاصة للنساء فقط
            special_status = T["none"]
            if gender == T["female"]:
                special_status = st.radio(T["special"], [T["none"], T["pregnant"], T["nursing"]], horizontal=True)

            if st.button(T["btn"]):
                bmi = weight / ((height/100)**2)
                st.subheader(f"BMI: {bmi:.1f}")
                # صياغة الطلب للذكاء الاصطناعي بناءً على كل البيانات
                prompt = f"""
                المريض: {gender}، العمر: {age}، BMI: {bmi:.1f}.
                الأمراض: {chronic}. الحالة الخاصة: {special_status}.
                قدم نصيحة طبية بيوكيميائية دقيقة باللغة {st.session_state.lang}.
                """
                st.info(ask_ai(prompt))
            st.markdown('</div>', unsafe_allow_html=True)

    elif menu == T["food_tab"]:
        # (جزء تحليل الأطباق كما في السابق)
        dish = st.text_input("Dish Name")
        if st.button(T["btn"]):
            st.write(ask_ai(f"حلل طبق {dish} بيوكيمياياً بالدراجة الجزائرية."))

    elif menu == T["lab_tab"]:
        # (جزء الأسئلة العلمية)
        q = st.text_area("Question?")
        if st.button(T["btn"]):
            st.write(ask_ai(q))

    if st.sidebar.button(T["logout"]):
        st.session_state.auth = False
        st.rerun()
