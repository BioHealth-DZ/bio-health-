import streamlit as st
import requests
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="BioHealth DZ", page_icon="🧪", layout="wide")

# 2. التنسيق الكامل (إعادة الخلفية والألوان التي اختفت)
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
    div.stButton > button { width: 100%; border-radius: 10px; background-color: #1b5e20; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. دالة الاتصال (تعديل جذري لتجاوز 404 وتجربة كل الموديلات المتاحة)
def get_ai_response(prompt):
    api_key = st.secrets["GEMINI_API_KEY"]
    # سنحاول تجربة الموديلات بالترتيب، بدءاً من flash وصولاً إلى pro القديم
    model_names = ["gemini-1.5-flash", "gemini-pro"]
    
    for name in model_names:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{name}:generateContent?key={api_key}"
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
            
    return "عذراً، يبدو أن هناك مشكلة في إصدار الـ API الخاص بجوجل حالياً. يرجى التأكد من صلاحية المفتاح."

# 4. إدارة اللغات
strings = {
    "العربية": {
        "welcome": "مرحباً بك في BioHealth DZ", "enter": "دخول", "name": "الاسم الكامل",
        "menu_bmi": "📊 حاسبة الصحة", "menu_food": "🥘 تحليل الأطباق", "menu_lab": "🔬 الأسئلة المخبرية",
        "age": "العمر", "gender": "الجنس", "male": "ذكر", "female": "أنثى", "w": "الوزن (كغ)", "h": "الطول (سم)",
        "chronic": "الأمراض المزمنة", "sugar": "سكري", "press": "ضغط دم", "none": "لا يوجد",
        "btn": "تحليل", "res": "النتائج:"
    }
}

# 5. إدارة الحالة والتنقل
if 'logged' not in st.session_state: st.session_state.logged = False
if 'page' not in st.session_state: st.session_state.page = "bmi"

if not st.session_state.logged:
    st.markdown("<h1 style='text-align:center;'>🧪 BioHealth DZ</h1>", unsafe_allow_html=True)
    un = st.text_input("الاسم الكامل")
    if st.button("دخول"):
        if un: st.session_state.logged, st.session_state.lang = True, "العربية"; st.rerun()
else:
    T = strings[st.session_state.lang]
    st.markdown(f'<div class="main-header"><h1>{T["welcome"]}</h1></div>', unsafe_allow_html=True)
    
    # قائمة التنقل كما في الصورة Capture d'écran 2026-05-14 171122.png
    nav1, nav2, nav3 = st.columns(3)
    if nav1.button(T["menu_bmi"]): st.session_state.page = "bmi"
    if nav2.button(T["menu_food"]): st.session_state.page = "food"
    if nav3.button(T["menu_lab"]): st.session_state.page = "lab"
    
    st.divider()

    if st.session_state.page == "bmi":
        st.markdown(f"### {T['menu_bmi']}")
        # استعادة تقسيم الأعمدة الثلاثة الذي ظهر في صورتك
        col1, col2, col3 = st.columns(3)
        with col1: age = st.number_input(T["age"], 1, 100, 25)
        with col2: gender = st.selectbox(T["gender"], [T["male"], T["female"]])
        with col3: weight = st.number_input(T["w"], 30.0, 200.0, 70.0)
        
        # استعادة خانة الطول والأمراض المزمنة التي فُقدت
        col4, col5 = st.columns(2)
        with col4: height = st.number_input(T["h"], 100.0, 250.0, 170.0)
        with col5: chronic = st.multiselect(T["chronic"], [T["sugar"], T["press"], T["none"]])
        
        if st.button(T["btn"]):
            bmi = weight / ((height/100)**2)
            st.markdown(f"### BMI: **{bmi:.1f}**")
            with st.spinner("جاري التحليل..."):
                prompt = f"قدم نصيحة طبية لشخص عمره {age} وجنسه {gender} ولديه BMI {bmi:.1f} وأمراض {chronic}"
                res = get_ai_response(prompt)
                st.markdown(f'<div class="advice-box"><b>{T["res"]}</b><br>{res}</div>', unsafe_allow_html=True)
