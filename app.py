import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="BioHealth DZ", page_icon="🧪", layout="wide")

# 2. التنسيق وإخفاء أشرطة GitHub
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display:none;}
    [data-testid="stHeader"] {display:none;}
    .stApp { background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%) !important; }
    .main-header {
        background: linear-gradient(90deg, #1b5e20, #43a047);
        color: white !important; padding: 25px; border-radius: 20px; text-align: center; margin-bottom: 20px;
    }
    .advice-box {
        background-color: #ffffff; border-left: 10px solid #1b5e20;
        padding: 20px; border-radius: 10px; color: #1b5e20; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    /* تنسيق أزرار التنقل العلوي */
    div.stButton > button { width: 100%; border-radius: 10px; height: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. محرك الذكاء الاصطناعي
model = genai.GenerativeModel("gemini-pro")
    try:
        if "GEMINI_API_KEY" not in st.secrets: return "Error: API Key missing"
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # هذا هو السطر الذي يتم استبداله
        model = genai.GenerativeModel("gemini-1.5-flash-latest") 
        
        return model.generate_content(prompt).text
    except Exception as e: return f"Error: {str(e)}"
    try:
        if "GEMINI_API_KEY" not in st.secrets: return "Error: API Key missing"
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")
        return model.generate_content(prompt).text
    except Exception as e: return f"Error: {str(e)}"

# 4. قاعدة بيانات اللغات
strings = {
    "العربية": {
        "welcome": "BioHealth DZ مرحباً بك في", "enter": "دخول", "name": "الاسم الكامل",
        "menu_bmi": "📊 حاسبة الصحة", "menu_food": "🥘 تحليل الأطباق", "menu_lab": "🔬 الأسئلة المخبرية",
        "age": "العمر", "gender": "الجنس", "male": "ذكر", "female": "أنثى", "w": "الوزن (كغ)", "h": "الطول (سم)",
        "chronic": "الأمراض المزمنة", "sugar": "سكري", "press": "ضغط دم", "none": "لا يوجد",
        "lady": "حالات خاصة", "preg": "حامل", "nurse": "مرضعة", "btn": "تحليل", "res": "النتائج:",
        "history": "📜 السجل", "no_history": "لا توجد نتائج"
    },
    "English": {
        "welcome": "Welcome to BioHealth DZ", "enter": "Login", "name": "Full Name",
        "menu_bmi": "📊 Health Calc", "menu_food": "🥘 Food Analysis", "menu_lab": "🔬 Lab Questions",
        "age": "Age", "gender": "Gender", "male": "Male", "female": "Female", "w": "Weight (kg)", "h": "Height (cm)",
        "chronic": "Chronic Diseases", "sugar": "Diabetes", "press": "Blood Pressure", "none": "None",
        "lady": "Special Cases", "preg": "Pregnant", "nurse": "Breastfeeding", "btn": "Analyze", "res": "Results:",
        "history": "📜 History", "no_history": "No results"
    },
    "Français": {
        "welcome": "Bienvenue sur BioHealth DZ", "enter": "Entrer", "name": "Nom Complet",
        "menu_bmi": "📊 Santé & IMC", "menu_food": "🥘 Analyse Plats", "menu_lab": "🔬 Questions Labo",
        "age": "Âge", "gender": "Sexe", "male": "Homme", "female": "Femme", "w": "Poids (kg)", "h": "Taille (cm)",
        "chronic": "Maladies", "sugar": "Diabète", "press": "Tension", "none": "Aucun",
        "lady": "États spéciaux", "preg": "Enceinte", "nurse": "Allaitante", "btn": "Analyser", "res": "Résultats:",
        "history": "📜 Historique", "no_history": "Aucun résultat"
    }
}

if 'logged' not in st.session_state: st.session_state.logged = False
if 'history' not in st.session_state: st.session_state.history = []
if 'page' not in st.session_state: st.session_state.page = "bmi" # الصفحة الافتراضية

if not st.session_state.logged:
    st.markdown("<h1 style='text-align:center;'>🧪 BioHealth DZ</h1>", unsafe_allow_html=True)
    sl = st.selectbox("Language / اللغة", ["العربية", "English", "Français"])
    un = st.text_input(strings[sl]["name"])
    if st.button(strings[sl]["enter"]):
        if un:
            st.session_state.logged, st.session_state.user, st.session_state.lang = True, un, sl
            st.rerun()
else:
    T = strings[st.session_state.lang]
    st.markdown(f'<div class="main-header"><h1>{T["welcome"]}</h1></div>', unsafe_allow_html=True)
    
    # أزرار التنقل العلوية لتسهيل الوصول (عوض القائمة الجانبية)
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    if col_nav1.button(T["menu_bmi"]): st.session_state.page = "bmi"
    if col_nav2.button(T["menu_food"]): st.session_state.page = "food"
    if col_nav3.button(T["menu_lab"]): st.session_state.page = "lab"
    
    st.divider()

    # --- القسم الأول: حاسبة الصحة ---
    if st.session_state.page == "bmi":
        st.subheader(T["menu_bmi"])
        c1, c2, c3 = st.columns(3)
        with c1: age = st.number_input(T["age"], 1, 100, 25)
        with c2: gender = st.selectbox(T["gender"], [T["male"], T["female"]])
        with c3: w = st.number_input(T["w"], 30.0, 200.0, 70.0)
        c4, c5 = st.columns(2)
        with c4: h = st.number_input(T["h"], 100.0, 250.0, 170.0)
        with c5: chronic = st.multiselect(T["chronic"], [T["sugar"], T["press"]])
        spec = T["none"]
        if gender == T["female"]: spec = st.radio(T["lady"], [T["none"], T["preg"], T["nurse"]], horizontal=True)
        if st.button(T["btn"]):
            bmi = w / ((h/100)**2)
            st.markdown(f"### BMI: **{bmi:.1f}**")
            res = get_ai_response(f"Analyze: {gender}, {age}y, BMI {bmi:.1f}, Chronic: {chronic}. In {st.session_state.lang}")
            st.session_state.history.append({"type": T["menu_bmi"], "item": f"BMI:{bmi:.1f}", "result": res})
            st.markdown(f'<div class="advice-box">{res}</div>', unsafe_allow_html=True)

    # --- القسم الثاني: تحليل الغذاء (البحث عن الأطباق) ---
    elif st.session_state.page == "food":
        st.subheader(T["menu_food"])
        dish = st.text_input("Search Dish / ابحث عن طبق (مثلاً: كسكس، شربة)")
        if st.button(T["btn"]):
            with st.spinner("..."):
                res = get_ai_response(f"Analyze dish {dish} biochemically for health.")
                st.session_state.history.append({"type": T["menu_food"], "item": dish, "result": res})
                st.markdown(f'<div class="advice-box">{res}</div>', unsafe_allow_html=True)

    # --- القسم الثالث: الأسئلة المخبرية ---
    elif st.session_state.page == "lab":
        st.subheader(T["menu_lab"])
        q = st.text_area("Question?")
        if st.button(T["btn"]):
            res = get_ai_response(q)
            st.session_state.history.append({"type": T["menu_lab"], "item": q[:20], "result": res})
            st.markdown(f'<div class="advice-box">{res}</div>', unsafe_allow_html=True)

    # --- السجل ---
    st.divider()
    st.subheader(T["history"])
    if not st.session_state.history: st.write(T["no_history"])
    else:
        for entry in reversed(st.session_state.history):
            with st.expander(f"{entry['type']} - {entry['item']}"): st.write(entry['result'])

    if st.sidebar.button("Logout"):
        st.session_state.logged = False
        st.session_state.history = []
        st.rerun()
