import streamlit as st
import requests
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="BioHealth DZ", page_icon="🧪", layout="wide")

# 2. التنسيق الاحترافي (الخلفية والألوان)
st.markdown("""
    <style>
    header {visibility: hidden;}
    .stApp {
        background-image: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), 
                          url("https://raw.githubusercontent.com/your-username/your-repo/main/watermarked_img_11248709154786756656.png");
        background-size: cover; background-attachment: fixed;
    }
    .main-header {
        background: linear-gradient(90deg, #1b5e20, #43a047);
        color: white !important; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;
    }
    .advice-box {
        background-color: #ffffff; border-right: 10px solid #1b5e20;
        padding: 20px; border-radius: 10px; color: #1b5e20; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div.stButton > button { width: 100%; border-radius: 10px; background-color: #1b5e20; color: white; font-weight: bold; height: 45px;}
    </style>
    """, unsafe_allow_html=True)

# 3. دالة الذكاء الاصطناعي المطورة (تجاوز الـ 404 وتعدد الإصدارات)
def get_ai_response(prompt):
    if "GEMINI_API_KEY" not in st.secrets:
        return "Error: API Key missing in Secrets"
    
    api_key = st.secrets["GEMINI_API_KEY"]
    # محاولة الاتصال عبر عدة مسارات لضمان التوافق
    endpoints = [
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    ]
    
    for url in endpoints:
        try:
            response = requests.post(
                url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}),
                timeout=10
            )
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            continue
    return "عذراً، حدث خطأ في الاتصال. يرجى التأكد من تشغيل الإنترنت وصلاحية مفتاح API."

# 4. قاعدة بيانات اللغات (إعادة تفعيل اللغات الثلاث)
strings = {
    "العربية": {
        "welcome": "مرحباً بك في BioHealth DZ", "enter": "دخول", "name": "الاسم الكامل",
        "menu_bmi": "📊 حاسبة الصحة", "menu_food": "🥘 تحليل الأطباق", "menu_lab": "🔬 الأسئلة المخبرية",
        "age": "العمر", "gender": "الجنس", "male": "ذكر", "female": "أنثى", "w": "الوزن (كغ)", "h": "الطول (سم)",
        "chronic": "الأمراض المزمنة", "sugar": "سكري", "press": "ضغط دم", "none": "لا يوجد",
        "btn": "تحليل", "res": "النتائج:", "history": "📜 السجل"
    },
    "English": {
        "welcome": "Welcome to BioHealth DZ", "enter": "Login", "name": "Full Name",
        "menu_bmi": "📊 Health Calc", "menu_food": "🥘 Food Analysis", "menu_lab": "🔬 Lab Questions",
        "age": "Age", "gender": "Gender", "male": "Male", "female": "Female", "w": "Weight (kg)", "h": "Height (cm)",
        "chronic": "Chronic Diseases", "sugar": "Diabetes", "press": "Blood Pressure", "none": "None",
        "btn": "Analyze", "res": "Results:", "history": "📜 History"
    },
    "Français": {
        "welcome": "Bienvenue sur BioHealth DZ", "enter": "Entrer", "name": "Nom Complet",
        "menu_bmi": "📊 Santé & IMC", "menu_food": "🥘 Analyse Plats", "menu_lab": "🔬 Questions Labo",
        "age": "Âge", "gender": "Sexe", "male": "Homme", "female": "Femme", "w": "Poids (kg)", "h": "Taille (cm)",
        "chronic": "Maladies", "sugar": "Diabète", "press": "Tension", "none": "Aucun",
        "btn": "Analyser", "res": "Résultats:", "history": "📜 Historique"
    }
}

# 5. إدارة التنقل والحالة
if 'logged' not in st.session_state: st.session_state.logged = False
if 'page' not in st.session_state: st.session_state.page = "bmi"
if 'history' not in st.session_state: st.session_state.history = []

# 6. واجهة تسجيل الدخول واختيار اللغة
if not st.session_state.logged:
    st.markdown("<h1 style='text-align:center;'>🧪 BioHealth DZ</h1>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        lang_choice = st.selectbox("Choose Language / اختر اللغة", ["العربية", "English", "Français"])
        user_name = st.text_input(strings[lang_choice]["name"])
        if st.button(strings[lang_choice]["enter"]):
            if user_name:
                st.session_state.logged = True
                st.session_state.lang = lang_choice
                st.session_state.user = user_name
                st.rerun()
else:
    T = strings[st.session_state.lang]
    st.markdown(f'<div class="main-header"><h1>{T["welcome"]}</h1></div>', unsafe_allow_html=True)
    
    # قائمة التنقل العلوية
    n1, n2, n3 = st.columns(3)
    if n1.button(T["menu_bmi"]): st.session_state.page = "bmi"
    if n2.button(T["menu_food"]): st.session_state.page = "food"
    if n3.button(T["menu_lab"]): st.session_state.page = "lab"
    
    st.divider()

    # --- قسم حاسبة الصحة ---
    if st.session_state.page == "bmi":
        st.subheader(T["menu_bmi"])
        c1, c2, c3 = st.columns(3)
        with c1: age = st.number_input(T["age"], 1, 100, 25)
        with c2: gender = st.selectbox(T["gender"], [T["male"], T["female"]])
        with c3: weight = st.number_input(T["w"], 30.0, 200.0, 70.0)
        
        c4, c5 = st.columns(2)
        with c4: height = st.number_input(T["h"], 100.0, 250.0, 170.0)
        with c5: chronic = st.multiselect(T["chronic"], [T["sugar"], T["press"], T["none"]])
        
        if st.button(T["btn"]):
            bmi = weight / ((height/100)**2)
            st.markdown(f"### BMI: **{bmi:.1f}**")
            with st.spinner("..."):
                res = get_ai_response(f"نصيحة لشخص عمره {age} وجنسه {gender} ولديه BMI {bmi:.1f} وأمراض {chronic}")
                st.session_state.history.append({"t": T["menu_bmi"], "v": f"BMI:{bmi:.1f}", "r": res})
                st.markdown(f'<div class="advice-box"><b>{T["res"]}</b><br>{res}</div>', unsafe_allow_html=True)

    # --- قسم تحليل الأطباق ---
    elif st.session_state.page == "food":
        st.subheader(T["menu_food"])
        dish = st.text_input("اسم الطبق / Dish Name")
        if st.button(T["btn"]):
            with st.spinner("..."):
                res = get_ai_response(f"تحليل غذائي لطبق: {dish}")
                st.session_state.history.append({"t": T["menu_food"], "v": dish, "r": res})
                st.markdown(f'<div class="advice-box">{res}</div>', unsafe_allow_html=True)

    # --- قسم الأسئلة المخبرية ---
    elif st.session_state.page == "lab":
        st.subheader(T["menu_lab"])
        lab_q = st.text_area("سؤالك المخبري / Lab Question")
        if st.button(T["btn"]):
            with st.spinner("..."):
                res = get_ai_response(lab_q)
                st.session_state.history.append({"t": T["menu_lab"], "v": lab_q[:20], "r": res})
                st.markdown(f'<div class="advice-box">{res}</div>', unsafe_allow_html=True)

    # السجل التاريخي
    st.divider()
    with st.expander(T["history"]):
        for entry in reversed(st.session_state.history):
            st.write(f"**{entry['t']} ({entry['v']}):** {entry['r']}")
