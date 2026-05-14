import streamlit as st
import requests
import json
import random

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="BioHealth DZ", page_icon="🔬", layout="wide")

# 2. التنسيق الجمالي الكامل (CSS) - إعادة الألوان والخلفية
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                    url("https://www.transparenttextures.com/patterns/clean-gray-paper.png");
        background-color: #f0f7f4;
    }
    .main-header {
        background: linear-gradient(135deg, #1b5e20 0%, #43a047 100%);
        color: white !important; padding: 30px; border-radius: 20px; text-align: center;
        margin-bottom: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .tip-card {
        background-color: #e8f5e9; border-right: 10px solid #1b5e20;
        padding: 20px; border-radius: 15px; color: #1b5e20; text-align: center;
        font-size: 1.2rem; margin-bottom: 25px; border-left: 1px solid #c8e6c9;
    }
    .advice-box {
        background-color: white; border-right: 12px solid #2e7d32;
        padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-top: 20px; font-size: 1.1rem;
    }
    div.stButton > button {
        width: 100%; border-radius: 12px; height: 50px; font-weight: bold;
        background-color: #1b5e20; color: white; border: none; font-size: 1.1rem;
    }
    .login-box {
        background: white; padding: 40px; border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1); border: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. دالة الذكاء الاصطناعي (حل مشكلة الاتصال النهائي)
def get_ai_response(prompt):
    if "GEMINI_API_KEY" not in st.secrets:
        return "⚠️ مفتاح API غير موجود في إعدادات Secrets."
    
    api_key = st.secrets["GEMINI_API_KEY"]
    # تجربة عدة روابط لضمان عمل الخدمة
    urls = [
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    ]
    
    for url in urls:
        try:
            res = requests.post(url, headers={'Content-Type': 'application/json'}, 
                                data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}), timeout=10)
            if res.status_code == 200:
                return res.json()['candidates'][0]['content']['parts'][0]['text']
        except: continue
    return "❌ فشل الاتصال. يرجى التأكد من أن مفتاح API في الإعدادات صحيح ونشط."

# 4. قاعدة بيانات اللغات
strings = {
    "العربية": {
        "welcome": "نظام BioHealth DZ الذكي 🏥", "enter": "دخول", "name": "الاسم الكامل",
        "menu_bmi": "📊 حاسبة الصحة", "menu_food": "🥘 تحليل الأطباق", "menu_lab": "🔬 الأسئلة المخبرية",
        "age": "العمر", "gender": "الجنس", "male": "ذكر", "female": "أنثى", "w": "الوزن (كغ)", "h": "الطول (سم)",
        "chronic": "الأمراض المزمنة", "sugar": "سكري", "press": "ضغط دم", "none": "لا يوجد",
        "btn": "تحليل الحالة ✨", "res": "النتائج والتوصيات:",
        "tips": ["🩺 شرب الماء يحسن الدورة الدموية.", "🍏 تفاحة يومياً تقوي المناعة.", "🏃‍♂️ المشي يقلل مخاطر السمنة."]
    },
    "English": {
        "welcome": "BioHealth DZ Smart System 🏥", "enter": "Login", "name": "Full Name",
        "menu_bmi": "📊 Health Calc", "menu_food": "🥘 Food Analysis", "menu_lab": "🔬 Lab Questions",
        "age": "Age", "gender": "Gender", "male": "Male", "female": "Female", "w": "Weight (kg)", "h": "Height (cm)",
        "chronic": "Chronic Diseases", "sugar": "Diabetes", "press": "Blood Pressure", "none": "None",
        "btn": "Analyze Now ✨", "res": "Results:",
        "tips": ["🩺 Water improves circulation.", "🍏 An apple a day keeps doctors away.", "🏃‍♂️ Walking burns fat."]
    },
    "Français": {
        "welcome": "Système BioHealth DZ 🏥", "enter": "Entrer", "name": "Nom Complet",
        "menu_bmi": "📊 Calcul de Santé", "menu_food": "🥘 Analyse Plats", "menu_lab": "🔬 Questions Labo",
        "age": "Âge", "gender": "Sexe", "male": "Homme", "female": "Femme", "w": "Poids (kg)", "h": "Taille (cm)",
        "chronic": "Maladies", "sugar": "Diabète", "press": "Tension", "none": "Aucun",
        "btn": "Analyser ✨", "res": "Résultats:",
        "tips": ["🩺 L'eau améliore la santé.", "🍏 Une pomme par jour est idéale.", "🏃‍♂️ La marche est vitale."]
    }
}

# 5. إدارة الحالة والتنقل
if 'logged' not in st.session_state: st.session_state.logged = False
if 'page' not in st.session_state: st.session_state.page = "bmi"

# 6. واجهة الدخول (الواجهة الأولى)
if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#1b5e20;'>🧪 BioHealth DZ</h2>", unsafe_allow_html=True)
        sel_lang = st.selectbox("Choose Language / اختر اللغة", ["العربية", "English", "Français"])
        u_name = st.text_input(strings[sel_lang]["name"])
        if st.button(strings[sel_lang]["enter"]):
            if u_name:
                st.session_state.logged, st.session_state.lang, st.session_state.user = True, sel_lang, u_name
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    T = strings[st.session_state.lang]
    st.markdown(f'<div class="main-header"><h1>{T["welcome"]}</h1><p>مرحباً بك، {st.session_state.user}</p></div>', unsafe_allow_html=True)
    
    # عرض النصيحة المتغيرة بشكل جميل
    st.markdown(f'<div class="tip-card">{random.choice(T["tips"])}</div>', unsafe_allow_html=True)

    # أزرار التنقل
    nav1, nav2, nav3 = st.columns(3)
    if nav1.button(T["menu_bmi"]): st.session_state.page = "bmi"
    if nav2.button(T["menu_food"]): st.session_state.page = "food"
    if nav3.button(T["menu_lab"]): st.session_state.page = "lab"
    
    st.divider()

    if st.session_state.page == "bmi":
        st.subheader(T["menu_bmi"])
        col1, col2, col3 = st.columns(3)
        with col1: age = st.number_input(T["age"], 1, 100, 25)
        with col2: gender = st.selectbox(T["gender"], [T["male"], T["female"]])
        with col3: weight = st.number_input(T["w"]+" ⚖️", 30.0, 200.0, 70.0)
        
        col4, col5 = st.columns(2)
        with col4: height = st.number_input(T["h"]+" 📏", 100.0, 250.0, 170.0)
        with col5: chronic = st.multiselect(T["chronic"], [T["sugar"], T["press"], T["none"]])
        
        if st.button(T["btn"]):
            bmi = weight / ((height/100)**2)
            st.markdown(f"### BMI: **{bmi:.1f}**")
            with st.spinner("جاري التحليل..."):
                res = get_ai_response(f"نصيحة لمستخدم عمره {age}، جنسه {gender}، BMI {bmi:.1f} وأمراض {chronic}")
                st.markdown(f'<div class="advice-box"><b>{T["res"]}</b><br>{res}</div>', unsafe_allow_html=True)
    
    elif st.session_state.page == "food":
        st.subheader(T["menu_food"])
        dish = st.text_input("اسم الطبق / Dish Name 🍲")
        if st.button(T["btn"]):
            with st.spinner("..."):
                res = get_ai_response(f"تحليل غذائي لطبق {dish}")
                st.markdown(f'<div class="advice-box">{res}</div>', unsafe_allow_html=True)

    elif st.session_state.page == "lab":
        st.subheader(T["menu_lab"])
        q = st.text_area("سؤالك المخبري / Lab Question 🔬")
        if st.button(T["btn"]):
            with st.spinner("..."):
                res = get_ai_response(q)
                st.markdown(f'<div class="advice-box">{res}</div>', unsafe_allow_html=True)
