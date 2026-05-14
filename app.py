import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="BioHealth DZ", page_icon="🧪", layout="wide")

# 2. التنسيق: الخلفية وتنسيق الأقسام
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {
        background-image: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), 
                          url("https://raw.githubusercontent.com/your-username/your-repo/main/watermarked_img_11248709154786756656.png");
        background-size: cover;
        background-attachment: fixed;
    }
    .main-header {
        background: linear-gradient(90deg, #1b5e20, #43a047);
        color: white !important; padding: 25px; border-radius: 20px; text-align: center; margin-bottom: 20px;
    }
    .advice-box {
        background-color: #ffffff; border-left: 10px solid #1b5e20;
        padding: 20px; border-radius: 10px; color: #1b5e20; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    div.stButton > button { width: 100%; border-radius: 10px; height: 50px; font-weight: bold; background-color: #1b5e20; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. دالة الذكاء الاصطناعي - الحل الذكي للقضاء على 404
def get_ai_response(prompt):
    if "GEMINI_API_KEY" not in st.secrets:
        return "خطأ: مفتاح API غير موجود في إعدادات Secrets"
    
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # قائمة بجميع الأسماء المحتملة للموديل حسب إصدار المكتبة
    possible_models = ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-pro", "models/gemini-pro"]
    
    last_error = ""
    for model_name in possible_models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = str(e)
            continue # تجربة الاسم التالي في القائمة
            
    return f"لم نتمكن من الاتصال بالموديل. الخطأ الأخير: {last_error}"

# 4. قاعدة بيانات اللغات
strings = {
    "العربية": {
        "welcome": "مرحباً بك في BioHealth DZ", "enter": "دخول", "name": "الاسم الكامل",
        "menu_bmi": "📊 حاسبة الصحة", "menu_food": "🥘 تحليل الأطباق", "menu_lab": "🔬 الأسئلة المخبرية",
        "age": "العمر", "gender": "الجنس", "male": "ذكر", "female": "أنثى", "w": "الوزن (كغ)", "h": "الطول (سم)",
        "chronic": "الأمراض المزمنة", "sugar": "سكري", "press": "ضغط دم", "none": "لا يوجد",
        "btn": "تحليل", "res": "النتائج:", "history": "📜 سجل النتائج"
    },
    "English": {
        "welcome": "Welcome to BioHealth DZ", "enter": "Login", "name": "Full Name",
        "menu_bmi": "📊 Health Calc", "menu_food": "🥘 Food Analysis", "menu_lab": "🔬 Lab Questions",
        "age": "Age", "gender": "Gender", "male": "Male", "female": "Female", "w": "Weight (kg)", "h": "Height (cm)",
        "chronic": "Chronic Diseases", "sugar": "Diabetes", "press": "Blood Pressure", "none": "None",
        "btn": "Analyze", "res": "Results:", "history": "📜 Result History"
    },
    "Français": {
        "welcome": "Bienvenue sur BioHealth DZ", "enter": "Entrer", "name": "Nom Complet",
        "menu_bmi": "📊 Santé & IMC", "menu_food": "🥘 Analyse Plats", "menu_lab": "🔬 Questions Labo",
        "age": "Âge", "gender": "Sexe", "male": "Homme", "female": "Femme", "w": "Poids (kg)", "h": "Taille (cm)",
        "chronic": "Maladies", "sugar": "Diabète", "press": "Tension", "none": "Aucun",
        "btn": "Analyser", "res": "Résultats:", "history": "📜 Historique"
    }
}

# 5. إدارة الحالة
if 'logged' not in st.session_state: st.session_state.logged = False
if 'history' not in st.session_state: st.session_state.history = []
if 'page' not in st.session_state: st.session_state.page = "bmi"

# 6. بناء الواجهة
if not st.session_state.logged:
    st.markdown("<h1 style='text-align:center;'>🧪 BioHealth DZ</h1>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        sl = st.selectbox("Language / اللغة", ["العربية", "English", "Français"])
        un = st.text_input(strings[sl]["name"])
        if st.button(strings[sl]["enter"]):
            if un:
                st.session_state.logged, st.session_state.user, st.session_state.lang = True, un, sl
                st.rerun()
else:
    T = strings[st.session_state.lang]
    st.markdown(f'<div class="main-header"><h1>{T["welcome"]}</h1></div>', unsafe_allow_html=True)
    
    # أزرار التنقل
    n1, n2, n3 = st.columns(3)
    if n1.button(T["menu_bmi"]): st.session_state.page = "bmi"
    if n2.button(T["menu_food"]): st.session_state.page = "food"
    if n3.button(T["menu_lab"]): st.session_state.page = "lab"
    
    st.divider()

    if st.session_state.page == "bmi":
        st.subheader(T["menu_bmi"])
        c1, c2, c3 = st.columns(3)
        with c1: age = st.number_input(T["age"], 1, 100, 25)
        with c2: gender = st.selectbox(T["gender"], [T["male"], T["female"]])
        with c3: weight = st.number_input(T["w"], 30.0, 200.0, 70.0)
        c4, c5 = st.columns(2)
        with c4: height = st.number_input(T["h"], 100.0, 250.0, 170.0)
        with c5: chronic = st.multiselect(T["chronic"], [T["sugar"], T["press"]])
        
        if st.button(T["btn"]):
            bmi = weight / ((height/100)**2)
            with st.spinner("..."):
                res = get_ai_response(f"Analyze: {gender}, BMI {bmi:.1f}, {chronic}")
                st.session_state.history.append({"type": T["menu_bmi"], "item": f"BMI:{bmi:.1f}", "result": res})
                st.markdown(f'<div class="advice-box"><b>{T["res"]}</b><br>{res}</div>', unsafe_allow_html=True)

    elif st.session_state.page == "food":
        st.subheader(T["menu_food"])
        dish = st.text_input("اسم الطبق / Dish Name")
        if st.button(T["btn"]):
            with st.spinner("..."):
                res = get_ai_response(f"Analyze food: {dish}")
                st.session_state.history.append({"type": T["menu_food"], "item": dish, "result": res})
                st.markdown(f'<div class="advice-box">{res}</div>', unsafe_allow_html=True)

    elif st.session_state.page == "lab":
        st.subheader(T["menu_lab"])
        q = st.text_area("سؤالك المخبري / Lab Question")
        if st.button(T["btn"]):
            with st.spinner("..."):
                res = get_ai_response(q)
                st.session_state.history.append({"type": T["menu_lab"], "item": q[:20], "result": res})
                st.markdown(f'<div class="advice-box">{res}</div>', unsafe_allow_html=True)

    # السجل
    st.divider()
    with st.expander(T["history"]):
        for entry in reversed(st.session_state.history):
            st.write(f"**{entry['type']}:** {entry['result']}")
