import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="BioHealth DZ", page_icon="🧪", layout="wide")

# 2. حقن التصميم الاحترافي (خلفية ملونة + صناديق واضحة)
st.markdown("""
    <style>
    /* الخلفية الأساسية للموقع */
    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%) !important;
    }
    
    /* تصميم الصفحة الأولى وصناديق الدخول */
    .login-box {
        background: white;
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 2px solid #2e7d32;
        text-align: center;
    }

    /* العنوان الرئيسي الملون */
    .main-header {
        background: linear-gradient(90deg, #1b5e20, #43a047);
        color: white !important;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    /* نصائح الحالة الصحية */
    .advice-box {
        background-color: #ffffff;
        border-left: 10px solid #1b5e20;
        padding: 20px;
        border-radius: 10px;
        color: #1b5e20;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* الأزرار الملفتة */
    div.stButton > button {
        background: #1b5e20 !important;
        color: white !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        padding: 10px 25px !important;
        border: none !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        background: #2e7d32 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. محرك الذكاء الاصطناعي
def get_ai_response(prompt):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target = next((m for m in models if "flash" in m or "pro" in m), models[0])
        model = genai.GenerativeModel(target)
        return model.generate_content(prompt).text
    except Exception as e:
        return f"حدث خطأ في الاتصال: {str(e)}"

# 4. قاعدة بيانات اللغات
strings = {
    "العربية": {
        "welcome": "مرحباً بك في BioHealth DZ", "enter": "دخول للمنصة",
        "name": "الاسم الكامل", "lang_sel": "اختر اللغة",
        "menu_bmi": "📊 حاسبة الصحة والوزن", "menu_food": "🥘 تحليل الغذاء", "menu_lab": "🔬 الأسئلة المخبرية",
        "age": "العمر", "gender": "الجنس", "male": "ذكر", "female": "أنثى",
        "w": "الوزن (كغ)", "h": "الطول (سم)", "chronic": "هل تعاني من أمراض مزمنة؟",
        "sugar": "سكري", "press": "ضغط دم", "none": "لا يوجد",
        "lady": "حالات خاصة", "preg": "حامل", "nurse": "مرضعة",
        "btn_calc": "إجراء التحليل البيوكيميائي", "result": "نتائج الحالة والنصائح:"
    },
    "Français": {
        "welcome": "Bienvenue sur BioHealth DZ", "enter": "Entrer dans la plateforme",
        "name": "Nom Complet", "lang_sel": "Choisir la langue",
        "menu_bmi": "📊 IMC & Santé", "menu_food": "🥘 Analyse de Plats", "menu_lab": "🔬 Questions Labo",
        "age": "Âge", "gender": "Sexe", "male": "Homme", "female": "Femme",
        "w": "Poids (kg)", "h": "Taille (cm)", "chronic": "Maladies chroniques?",
        "sugar": "Diabète", "press": "Tension", "none": "Aucun",
        "lady": "États spéciaux", "preg": "Enceinte", "nurse": "Allaitante",
        "btn_calc": "Lancer l'analyse biochimique", "result": "Résultats et Conseils:"
    }
}

# 5. إدارة حالة الدخول واللغة
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- الصفحة الأولى (الدخول) ---
if not st.session_state.logged_in:
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.header("🧪 BioHealth DZ")
        selected_lang = st.selectbox("Language / اللغة", ["العربية", "Français"])
        user_name = st.text_input(strings[selected_lang]["name"])
        if st.button(strings[selected_lang]["enter"]):
            if user_name:
                st.session_state.logged_in = True
                st.session_state.user = user_name
                st.session_state.lang = selected_lang
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- واجهة التطبيق الرئيسية ---
else:
    T = strings[st.session_state.lang]
    
    # القائمة الجانبية
    st.sidebar.markdown(f"### 👤 {st.session_state.user}")
    choice = st.sidebar.radio("Navigate", [T["menu_bmi"], T["menu_food"], T["menu_lab"]])
    if st.sidebar.button("Logout / خروج"):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown(f'<div class="main-header"><h1>{T["welcome"]}</h1></div>', unsafe_allow_html=True)

    if choice == T["menu_bmi"]:
        # خانات البيانات الكاملة
        with st.expander(T["menu_bmi"], expanded=True):
            c1, c2, c3 = st.columns(3)
            with c1: u_age = st.number_input(T["age"], 1, 100, 25)
            with c2: u_gender = st.selectbox(T["gender"], [T["male"], T["female"]])
            with c3: u_w = st.number_input(T["w"], 30.0, 200.0, 70.0)
            
            c4, c5 = st.columns(2)
            with c4: u_h = st.number_input(T["h"], 100.0, 250.0, 170.0)
            with c5: u_chronic = st.multiselect(T["chronic"], [T["sugar"], T["press"]])
            
            u_special = T["none"]
            if u_gender == T["female"]:
                u_special = st.radio(T["lady"], [T["none"], T["preg"], T["nurse"]], horizontal=True)

            if st.button(T["btn_calc"]):
                bmi = u_w / ((u_h/100)**2)
                st.markdown(f"### BMI: **{bmi:.1f}**")
                
                # فقرة النصائح التي اختفت
                with st.spinner("جاري تحليل حالتك بيوكيمياياً..."):
                    prompt = f"""
                    أنت خبير بيوكيمياء. حلل الحالة التالية:
                    الجنس: {u_gender}، العمر: {u_age}، BMI: {bmi:.1f}.
                    الأمراض المزمنة: {u_chronic}. الحالة الخاصة: {u_special}.
                    قدم نصائح غذائية وحيوية دقيقة باللغة {st.session_state.lang} وبلهجة جزائرية خفيفة إذا كانت اللغة عربية.
                    """
                    advice = get_ai_response(prompt)
                    st.markdown(f'<h3>{T["result"]}</h3>', unsafe_allow_html=True)
                    st.markdown(f'<div class="advice-box">{advice}</div>', unsafe_allow_html=True)

    elif choice == T["menu_food"]:
        st.subheader(T["menu_food"])
        dish = st.text_input("اسم الطبق / Nom du plat")
        if st.button("Analyze"):
            st.info(get_ai_response(f"حلل طبق {dish} بيوكيمياياً بالدراجة الجزائرية."))

    elif choice == T["menu_lab"]:
        st.subheader(T["menu_lab"])
        q = st.text_area("Question?")
        if st.button("Ask"):
            st.write(get_ai_response(q))
