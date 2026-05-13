import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="BioHealth DZ", page_icon="🧪", layout="wide")

# 2. تحسين الرؤية (خلفية واضحة جداً ونصوص حادة)
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f7f6; /* خلفية رمادية هادئة جداً تريح العين */
    }
    .main-title { 
        color: #1b5e20; text-align: center; font-size: 2.8rem; font-weight: bold; 
        padding: 20px; margin-bottom: 20px;
    }
    .welcome-card {
        background-color: white; padding: 40px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border: 1px solid #e0e0e0;
        max-width: 700px; margin: auto;
    }
    .result-card {
        background-color: white; padding: 25px; border-radius: 15px;
        border-left: 10px solid #2e7d32; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        color: #212529; font-size: 1.1rem;
    }
    /* جعل النصوص في الخانات غامقة وواضحة */
    .stNumberInput label, .stTextInput label, .stSelectbox label {
        color: #1b5e20 !important; font-weight: bold !important; font-size: 1.1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. نظام اللغات (Translations)
translations = {
    "العربية": {
        "welcome": "مرحباً بك في منصة البيوكيمياء والصحة",
        "enter_info": "يرجى إدخال بياناتك للدخول",
        "name": "الاسم الكامل", "email": "البريد الإلكتروني", "start": "دخول للمنصة",
        "bmi_tab": "📊 حاسبة كتلة الجسم", "food_tab": "🥘 تحليل الأطباق", "lab_tab": "🔬 المختبر العلمي",
        "weight": "الوزن (كغ)", "height": "الطول (سم)", "analyze": "تحليل الآن",
        "food_prompt": "قم بتحليل طبق {} بيوكيمياياً. اذكر الإيجابيات والسلبيات الصحية بكل حياد ونقد علمي (نصف بنصف) دون مبالغة في المديح، باللغة العربية الدارجة الجزائرية.",
        "lang_label": "اختر اللغة"
    },
    "Français": {
        "welcome": "Bienvenue sur BioHealth DZ",
        "enter_info": "Veuillez entrer vos informations",
        "name": "Nom Complet", "email": "E-mail", "start": "Entrer",
        "bmi_tab": "📊 Calcul de l'IMC", "food_tab": "🥘 Nutrition", "lab_tab": "🔬 Labo Scientifique",
        "weight": "Poids (kg)", "height": "Taille (cm)", "analyze": "Analyser",
        "food_prompt": "Analysez le plat {} de manière biochimique. Citez les points positifs et négatifs avec neutralité scientifique (50/50) en français.",
        "lang_label": "Langue"
    },
    "English": {
        "welcome": "Welcome to BioHealth DZ",
        "enter_info": "Please enter your details to proceed",
        "name": "Full Name", "email": "Email Address", "start": "Enter Platform",
        "bmi_tab": "📊 BMI Calculator", "food_tab": "🥘 Food Analysis", "lab_tab": "🔬 Science Lab",
        "weight": "Weight (kg)", "height": "Height (cm)", "analyze": "Analyze Now",
        "food_prompt": "Analyze the dish {} biochemically. Mention health pros and cons with scientific neutrality (50/50) in English.",
        "lang_label": "Language"
    }
}

# 4. منطق الدخول والترحيب (Session State)
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<br><br>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="welcome-card">', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align:center; color:#1b5e20;">🧪 BioHealth DZ</h1>', unsafe_allow_html=True)
        
        sel_lang = st.selectbox("اختر اللغة / Langue / Language", ["العربية", "Français", "English"])
        T = translations[sel_lang]
        
        st.subheader(T["welcome"])
        u_name = st.text_input(T["name"])
        u_email = st.text_input(T["email"])
        
        if st.button(T["start"]):
            if u_name:
                st.session_state.auth = True
                st.session_state.user = u_name
                st.session_state.lang = sel_lang
                st.rerun()
            else:
                st.error("يرجى إدخال الاسم على الأقل!")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # القائمة الرئيسية بعد الدخول
    T = translations[st.session_state.lang]
    st.sidebar.title(f"👤 {st.session_state.user}")
    
    # جلب المفتاح والتعامل مع الموديل
    API_KEY = st.secrets.get("GEMINI_API_KEY")
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    menu = st.sidebar.radio("Navigate", [T["bmi_tab"], T["food_tab"], T["lab_tab"]])

    st.markdown(f'<h1 class="main-title">{T["welcome"]}</h1>', unsafe_allow_html=True)

    if menu == T["bmi_tab"]:
        with st.container():
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1: w = st.number_input(T["weight"], 30.0, 200.0, 75.0)
            with c2: h = st.number_input(T["height"], 100.0, 250.0, 170.0)
            
            if st.button(T["analyze"]):
                bmi = w / ((h/100)**2)
                st.write(f"### BMI: {bmi:.1f}")
                with st.spinner("..."):
                    advice_prompt = f"Give medical advice for BMI {bmi:.1f} in {st.session_state.lang}"
                    st.info(model.generate_content(advice_prompt).text)
            st.markdown('</div>', unsafe_allow_html=True)

    elif menu == T["food_tab"]:
        dish = st.text_input("Dish Name / اسم الطبق")
        if st.button(T["analyze"]):
            with st.spinner("Analyzing..."):
                response = model.generate_content(T["food_prompt"].format(dish))
                st.markdown(f'<div class="result-card">{response.text}</div>', unsafe_allow_html=True)

    elif menu == T["lab_tab"]:
        query = st.text_area("Ask Science / سؤال علمي")
        if st.button(T["analyze"]):
            with st.spinner("..."):
                response = model.generate_content(f"Explain this in {st.session_state.lang}: {query}")
                st.write(response.text)

    if st.sidebar.button("Logout / خروج"):
        st.session_state.auth = False
        st.rerun()
