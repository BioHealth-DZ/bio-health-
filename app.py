import streamlit as st
import requests
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="BioHealth DZ", page_icon="🧪", layout="wide")

# 2. التنسيق الجمالي المتقدم (CSS)
st.markdown("""
    <style>
    /* إخفاء القوائم الافتراضية لزيادة الاحترافية */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* ضبط الخلفية العامة للتطبيق */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)), 
                    url("https://www.transparenttextures.com/patterns/clean-gray-paper.png"); /* نمط ورق نظيف */
        background-color: #f0f7f4;
    }

    /* تنسيق الهيدر الرئيسي */
    .main-header {
        background: linear-gradient(135deg, #1b5e20 0%, #43a047 100%);
        color: white !important;
        padding: 40px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(27, 94, 32, 0.2);
    }

    /* تنسيق الحاويات (Cards) */
    .stNumberInput, .stSelectbox, .stTextInput, .stMultiselect {
        background-color: white;
        border-radius: 12px;
        padding: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* تنسيق صندوق النتائج */
    .advice-box {
        background-color: #ffffff;
        border-right: 8px solid #2e7d32;
        padding: 25px;
        border-radius: 15px;
        color: #1b5e20;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        margin-top: 20px;
        font-size: 18px;
        line-height: 1.6;
    }

    /* تنسيق الأزرار لتكون جذابة */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #2e7d32, #4caf50);
        color: white;
        font-weight: bold;
        height: 50px;
        border: none;
        transition: 0.3s;
        font-size: 18px;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
        color: #e8f5e9;
    }
    
    /* تنسيق واجهة الدخول */
    .login-container {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. دالة الاتصال بالذكاء الاصطناعي (تجاوز الأخطاء)
def get_ai_response(prompt):
    if "GEMINI_API_KEY" not in st.secrets:
        return "Error: API Key missing"
    
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    try:
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}),
            timeout=10
        )
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            # محاولة بديلة بموديل آخر إذا فشل الأول
            url_alt = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
            response = requests.post(url_alt, headers={'Content-Type': 'application/json'}, data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}))
            return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "عذراً، لم نتمكن من الحصول على تحليل الآن. يرجى المحاولة لاحقاً."

# 4. إدارة اللغات
strings = {
    "العربية": {
        "welcome": "مرحباً بك في BioHealth DZ", "enter": "دخول للنظام", "name": "الاسم الكامل",
        "menu_bmi": "📊 حاسبة الصحة", "menu_food": "🥘 تحليل الأطباق", "menu_lab": "🔬 الأسئلة المخبرية",
        "age": "العمر", "gender": "الجنس", "male": "ذكر", "female": "أنثى", "w": "الوزن (كغ)", "h": "الطول (سم)",
        "chronic": "الأمراض المزمنة", "sugar": "سكري", "press": "ضغط دم", "none": "لا يوجد",
        "btn": "بدء التحليل الذكي", "res": "النتائج والتوصيات:"
    },
    "English": {
        "welcome": "Welcome to BioHealth DZ", "enter": "Login to System", "name": "Full Name",
        "menu_bmi": "📊 Health Calc", "menu_food": "🥘 Food Analysis", "menu_lab": "🔬 Lab Questions",
        "age": "Age", "gender": "Gender", "male": "Male", "female": "Female", "w": "Weight (kg)", "h": "Height (cm)",
        "chronic": "Chronic Diseases", "sugar": "Diabetes", "press": "BP", "none": "None",
        "btn": "Start AI Analysis", "res": "Results & Recommendations:"
    }
}

# 5. منطق الواجهة
if 'logged' not in st.session_state: st.session_state.logged = False
if 'page' not in st.session_state: st.session_state.page = "bmi"

if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 1.5, 1])
    with col_m:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#1b5e20;'>🧪 BioHealth DZ</h2>", unsafe_allow_html=True)
        lang = st.selectbox("Select Language / اختر اللغة", ["العربية", "English"])
        name = st.text_input(strings[lang]["name"])
        if st.button(strings[lang]["enter"]):
            if name:
                st.session_state.logged, st.session_state.lang, st.session_state.user = True, lang, name
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    T = strings[st.session_state.lang]
    st.markdown(f'<div class="main-header"><h1>{T["welcome"]}</h1><p>مرحباً، {st.session_state.user}</p></div>', unsafe_allow_html=True)
    
    # قائمة التنقل
    n1, n2, n3 = st.columns(3)
    if n1.button(T["menu_bmi"]): st.session_state.page = "bmi"
    if n2.button(T["menu_food"]): st.session_state.page = "food"
    if n3.button(T["menu_lab"]): st.session_state.page = "lab"
    
    st.divider()

    if st.session_state.page == "bmi":
        st.markdown(f"### {T['menu_bmi']}")
        c1, c2, c3 = st.columns(3)
        with c1: age = st.number_input(T["age"], 1, 100, 25)
        with c2: gender = st.selectbox(T["gender"], [T["male"], T["female"]])
        with c3: weight = st.number_input(T["w"], 30.0, 200.0, 70.0)
        
        c4, c5 = st.columns(2)
        with c4: height = st.number_input(T["h"], 100.0, 250.0, 170.0)
        with c5: chronic = st.multiselect(T["chronic"], [T["sugar"], T["press"], T["none"]])
        
        if st.button(T["btn"]):
            bmi = weight / ((height/100)**2)
            st.markdown(f"<h3 style='color:#1b5e20;'>BMI: {bmi:.1f}</h3>", unsafe_allow_html=True)
            with st.spinner("جاري التواصل مع الخبير الرقمي..."):
                res = get_ai_response(f"Analyze for {gender}, Age {age}, BMI {bmi:.1f}, Conditions: {chronic}")
                st.markdown(f'<div class="advice-box"><b>{T["res"]}</b><br>{res}</div>', unsafe_allow_html=True)

    elif st.session_state.page == "food":
        st.subheader(T["menu_food"])
        dish = st.text_input("اسم الطبق الجزائري المراد تحليله")
        if st.button(T["btn"]):
            with st.spinner("تحليل المكونات..."):
                res = get_ai_response(f"تحليل غذائي وكيميائي لطبق {dish}")
                st.markdown(f'<div class="advice-box">{res}</div>', unsafe_allow_html=True)
