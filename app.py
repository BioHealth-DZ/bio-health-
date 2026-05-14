
import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="BioHealth DZ", page_icon="🧪", layout="wide")

# 2. إخفاء شريط GitHub والتنسيق البصري (دمج شامل لتجنب أي NameError)
st.markdown("""
    <style>
    /* إخفاء شريط الأدوات العلوي */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display:none;}
    [data-testid="stHeader"] {display:none;}
    
    /* تنسيق الخلفية والألوان */
    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%) !important;
    }
    .login-box {
        background: white; padding: 40px; border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1); border: 2px solid #2e7d32; text-align: center;
    }
    .main-header {
        background: linear-gradient(90deg, #1b5e20, #43a047);
        color: white !important; padding: 25px; border-radius: 20px;
        text-align: center; margin-bottom: 30px; font-weight: bold;
    }
    .advice-box {
        background-color: #ffffff; border-left: 10px solid #1b5e20;
        padding: 20px; border-radius: 10px; color: #1b5e20;
        font-size: 1.1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    div.stButton > button {
        background: #1b5e20 !important; color: white !important;
        border-radius: 50px !important; font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. محرك الذكاء الاصطناعي
def get_ai_response(prompt):
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            return "⚠️ خطأ: مفتاح الـ API غير موجود في إعدادات Secrets."
        
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")
        return model.generate_content(prompt).text
    except Exception as e:
        if "429" in str(e):
            return "⚠️ انتهت كوتا الاستخدام المجاني حالياً. حاول بعد قليل."
        return f"حدث خطأ: {str(e)}"

# 4. قاعدة بيانات اللغات
strings = {
    "العربية": {
        "welcome": "مرحباً بك في BioHealth DZ", "enter": "دخول", "name": "الاسم الكامل",
        "menu_bmi": "📊 حاسبة الصحة والوزن", "menu_food": "🥘 تحليل الغذاء", "menu_lab": "🔬 الأسئلة المخبرية",
        "age": "العمر", "gender": "الجنس", "male": "ذكر", "female": "أنثى", "w": "الوزن (كغ)", "h": "الطول (سم)",
        "chronic": "الأمراض المزمنة", "sugar": "سكري", "press": "ضغط دم", "none": "لا يوجد",
        "lady": "حالات خاصة", "preg": "حامل", "nurse": "مرضعة", "btn": "تحليل الحالة", "res": "النتائج والنصائح:"
    },
    "Français": {
        "welcome": "Bienvenue sur BioHealth DZ", "enter": "Entrer", "name": "Nom Complet",
        "menu_bmi": "📊 IMC & Santé", "menu_food": "🥘 Analyse de Plats", "menu_lab": "🔬 Labo",
        "age": "Âge", "gender": "Sexe", "male": "Homme", "female": "Femme", "w": "Poids (kg)", "h": "Taille (cm)",
        "chronic": "Maladies", "sugar": "Diabète", "press": "Tension", "none": "Aucun",
        "lady": "États spéciaux", "preg": "Enceinte", "nurse": "Allaitante", "btn": "Analyser", "res": "Résultats:"
    }
}

# 5. منطق الدخول
if 'logged' not in st.session_state: st.session_state.logged = False

if not st.session_state.logged:
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.header("🧪 BioHealth DZ")
        sl = st.selectbox("Language / اللغة", ["العربية", "Français"])
        un = st.text_input(strings[sl]["name"])
        if st.button(strings[sl]["enter"]):
            if un:
                st.session_state.logged, st.session_state.user, st.session_state.lang = True, un, sl
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    T = strings[st.session_state.lang]
    st.sidebar.markdown(f"### 👤 {st.session_state.user}")
    choice = st.sidebar.radio("Navigate", [T["menu_bmi"], T["menu_food"], T["menu_lab"]])
    
    st.markdown(f'<div class="main-header"><h1>{T["welcome"]}</h1></div>', unsafe_allow_html=True)

    if choice == T["menu_bmi"]:
        c1, c2, c3 = st.columns(3)
        with c1: age = st.number_input(T["age"], 1, 100, 25)
        with c2: gender = st.selectbox(T["gender"], [T["male"], T["female"]])
        with c3: w = st.number_input(T["w"], 30.0, 200.0, 70.0)
        c4, c5 = st.columns(2)
        with c4: h = st.number_input(T["h"], 100.0, 250.0, 170.0)
        with c5: chronic = st.multiselect(T["chronic"], [T["sugar"], T["press"]])
        spec = T["none"]
        if gender == T["female"]:
            spec = st.radio(T["lady"], [T["none"], T["preg"], T["nurse"]], horizontal=True)

        if st.button(T["btn"]):
            bmi = w / ((h/100)**2)
            st.markdown(f"### BMI: **{bmi:.1f}**")
            with st.spinner("..."):
                p = f"حلل بيوكيمياياً: {gender}, {age} سنة, BMI {bmi:.1f}, أمراض: {chronic}, حالة خاصة: {spec}. بلغة {st.session_state.lang}."
                res = get_ai_response(p)
                st.markdown(f'<div class="advice-box"><b>{T["res"]}</b><br>{res}</div>', unsafe_allow_html=True)

    elif choice == T["menu_food"]:
        st.subheader(T["menu_food"])
        dish = st.text_input("Dish Name / اسم الطبق")
        if st.button(T["btn"]):
            with st.spinner("..."):
                res = get_ai_response(f"حلل طبق {dish} بيوكيمياياً بالدراجة الجزائرية.")
                st.markdown(f'<div class="advice-box">{res}</div>', unsafe_allow_html=True)

    elif choice == T["menu_lab"]:
        st.subheader(T["menu_lab"])
        q = st.text_area("Question?")
        if st.button(T["btn"]):
            with st.spinner("..."):
                res = get_ai_response(q)
                st.markdown(f'<div class="advice-box">{res}</div>', unsafe_allow_html=True)

    if st.sidebar.button("Logout"):
        st.session_state.logged = False
        st.rerun()
