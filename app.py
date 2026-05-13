import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="BioHealth DZ", page_icon="🧪", layout="wide")

# 2. حقن التصميم بطريقة إجبارية (Force CSS) لضمان الوضوح
st.markdown("""
    <style>
    /* خلفية التطبيق كاملة */
    .stApp {
        background: #f0f2f6 !important;
    }
    
    /* تصحيح العنوان الرئيسي ليصبح كبيراً وواضحاً */
    .big-title {
        font-size: 50px !important;
        color: #1b5e20 !important;
        text-align: center !important;
        font-weight: bold !important;
        padding: 30px !important;
        background: white !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        margin-bottom: 30px !important;
    }

    /* جعل البطاقات بيضاء وواضحة جداً للقراءة */
    .custom-card {
        background-color: white !important;
        padding: 30px !important;
        border-radius: 15px !important;
        border-right: 12px solid #2e7d32 !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
        color: #212529 !important;
        margin-bottom: 20px !important;
    }

    /* تحسين شكل الأزرار */
    div.stButton > button:first-child {
        background-color: #2e7d32 !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        height: 3em !important;
        width: 100% !important;
        border: none !important;
    }

    /* وضوح النصوص في القائمة الجانبية */
    .css-17l2qt2 { 
        background-color: #e8f5e9 !important; 
    }
    
    label p {
        font-size: 1.2rem !important;
        color: #1b5e20 !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. نظام اللغات
translations = {
    "العربية": {
        "title": "🧪 منصة BioHealth DZ للبيوكيمياء", "name": "الاسم الكامل", "start": "دخول للمنصة",
        "bmi": "📊 حاسبة كتلة الجسم", "food": "🥘 تحليل الأطباق", "w": "الوزن (كغ)", "h": "الطول (سم)",
        "btn": "إجراء التحليل الآن", "prompt": "حلل طبق {} بيوكيمياياً. اذكر الإيجابيات والسلبيات (50/50) بالدراجة الجزائرية."
    },
    "Français": {
        "title": "🧪 Plateforme BioHealth DZ", "name": "Nom Complet", "start": "Entrer",
        "bmi": "📊 Calcul de l'IMC", "food": "🥘 Analyse Nutritionnelle", "w": "Poids (kg)", "h": "Taille (cm)",
        "btn": "Lancer l'analyse", "prompt": "Analysez le plat {} (biochimie). Points positifs et négatifs (50/50) en français."
    },
    "English": {
        "title": "🧪 BioHealth DZ Platform", "name": "Full Name", "start": "Enter",
        "bmi": "📊 BMI Calculator", "food": "🥘 Food Analysis", "w": "Weight (kg)", "h": "Height (cm)",
        "btn": "Run Analysis", "prompt": "Analyze {} biochemically. Pros and cons (50/50) in English."
    }
}

# 4. دالة الذكاء الاصطناعي مع حل مشكلة الـ 404
def ask_ai(prompt):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = next((m for m in models if "flash" in m or "pro" in m), models[0])
        model = genai.GenerativeModel(model_name)
        return model.generate_content(prompt).text
    except Exception as e:
        return f"Error: {str(e)}"

# 5. منطق الواجهة
if 'login' not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    # نافذة الدخول
    st.markdown('<div class="big-title">BioHealth DZ</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        lang = st.selectbox("Language / اللغة", ["العربية", "Français", "English"])
        T = translations[lang]
        name = st.text_input(T["name"])
        if st.button(T["start"]):
            if name:
                st.session_state.login, st.session_state.lang, st.session_state.user = True, lang, name
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    T = translations[st.session_state.lang]
    st.sidebar.markdown(f"### 👤 {st.session_state.user}")
    menu = st.sidebar.radio("Navigate", [T["bmi"], T["food"]])
    
    # العنوان الرئيسي الكبير
    st.markdown(f'<div class="big-title">{T["title"]}</div>', unsafe_allow_html=True)

    if menu == T["bmi"]:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: weight = st.number_input(T["w"], 30.0, 200.0, 75.0)
        with c2: height = st.number_input(T["h"], 100.0, 250.0, 170.0)
        
        if st.button(T["btn"]):
            bmi = weight / ((height/100)**2)
            st.success(f"BMI: {bmi:.1f}")
            advice = ask_ai(f"Advice for BMI {bmi:.1f} in {st.session_state.lang}")
            st.info(advice)
        st.markdown('</div>', unsafe_allow_html=True)

    elif menu == T["food"]:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        dish = st.text_input("Dish Name / اسم الطبق")
        if st.button(T["btn"]):
            with st.spinner("..."):
                res = ask_ai(T["prompt"].format(dish))
                st.markdown(f"<div style='font-size:1.2rem;'>{res}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.rerun()
