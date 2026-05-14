import streamlit as st
import requests
import json

# 1. إعداد الصفحة
st.set_page_config(page_title="BioHealth DZ", page_icon="🧪", layout="wide")

# 2. التنسيق (كامل الواجهة)
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
        color: white !important; padding: 25px; border-radius: 20px; text-align: center; margin-bottom: 20px;
    }
    .advice-box {
        background-color: #ffffff; border-left: 10px solid #1b5e20;
        padding: 20px; border-radius: 10px; color: #1b5e20; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    div.stButton > button { width: 100%; border-radius: 10px; height: 50px; font-weight: bold; background-color: #1b5e20; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. دالة الذكاء الاصطناعي - تجاوز خطأ 404 نهائياً عبر HTTP
def get_ai_response(prompt):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        # استخدام رابط الـ API المباشر (تجاوز المكتبة المصابة بالخطأ)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        res_json = response.json()
        
        if response.status_code == 200:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"خطأ من جوجل: {res_json.get('error', {}).get('message', 'Unknown Error')}"
    except Exception as e:
        return f"فشل الاتصال المباشر: {str(e)}"

# 4. اللغات والواجهة (كما صممناها سابقاً)
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
    }
}

# (باقي كود إدارة الحالة والواجهة - نفس الذي نملكه)
if 'logged' not in st.session_state: st.session_state.logged = False
if 'history' not in st.session_state: st.session_state.history = []
if 'page' not in st.session_state: st.session_state.page = "bmi"

if not st.session_state.logged:
    st.markdown("<h1 style='text-align:center;'>🧪 BioHealth DZ</h1>", unsafe_allow_html=True)
    sl = st.selectbox("اللغة", ["العربية", "English"])
    un = st.text_input(strings[sl]["name"])
    if st.button(strings[sl]["enter"]):
        if un:
            st.session_state.logged, st.session_state.lang = True, sl
            st.rerun()
else:
    T = strings[st.session_state.lang]
    st.markdown(f'<div class="main-header"><h1>{T["welcome"]}</h1></div>', unsafe_allow_html=True)
    
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
        c4, h_in = st.columns([1,1])
        height = h_in.number_input(T["h"], 100.0, 250.0, 170.0)
        
        if st.button(T["btn"]):
            bmi = weight / ((height/100)**2)
            with st.spinner("جاري التحليل..."):
                res = get_ai_response(f"نصيحة لمستخدم: {gender}, BMI {bmi:.1f}")
                st.markdown(f'<div class="advice-box"><b>{T["res"]}</b><br>{res}</div>', unsafe_allow_html=True)
