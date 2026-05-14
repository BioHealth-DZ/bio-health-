import streamlit as st
import requests
import json
import random

# 1. إعداد الصفحة
st.set_page_config(page_title="BioHealth DZ", page_icon="💊", layout="wide")

# 2. التنسيق الجمالي (CSS) - إعادة الألوان والواجهة الاحترافية
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {
        background-color: #f4fbf7;
        background-image: radial-gradient(#d1e7dd 1px, transparent 1px);
        background-size: 20px 20px;
    }
    .main-header {
        background: linear-gradient(135deg, #1b5e20 0%, #43a047 100%);
        color: white !important; padding: 30px; border-radius: 20px; text-align: center;
        margin-bottom: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .tip-card {
        background-color: #e8f5e9; border-right: 10px solid #1b5e20;
        padding: 15px; border-radius: 12px; color: #1b5e20; text-align: center;
        font-weight: bold; margin-bottom: 25px;
    }
    .advice-box {
        background-color: white; border-right: 10px solid #2e7d32;
        padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    div.stButton > button {
        width: 100%; border-radius: 12px; height: 50px; font-weight: bold;
        background: linear-gradient(90deg, #1b5e20, #43a047); color: white; border: none;
    }
    .login-box {
        background: white; padding: 40px; border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1); border: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. دالة الذكاء الاصطناعي (تجاوز خطأ الاتصال في الصورة)
def get_ai_response(prompt):
    # 1. التحقق من وجود المفتاح في الإعدادات
    if "GEMINI_API_KEY" not in st.secrets:
        return "⚠️ خطأ: مفتاح API غير معرف في إعدادات Secrets."
    
    api_key = st.secrets["GEMINI_API_KEY"]
    
    # 2. الرابط الصحيح والمؤكد (v1beta)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    # 3. إعداد بيانات الطلب بشكل دقيق جداً
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    
    try:
        # 4. تنفيذ الطلب مع وقت انتظار كافٍ
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        # 5. معالجة الرد
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            # في حال استمر الخطأ، هذا النص سيخبرنا بالسبب الحقيقي (صلاحية المفتاح أو الرابط)
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'خطأ غير معروف')
            return f"❌ خطأ ({response.status_code}): {error_msg}"
            
    except Exception as e:
        return f"⚠️ فشل الاتصال بالسيرفر: {str(e)}"
    api_key = st.secrets["GEMINI_API_KEY"]
    # استخدام الإصدار المستقر v1 لضمان أعلى توافق وتجنب خطأ 404
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
    
    try:
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, json=payload, timeout=15)
        
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ Connection Error ({response.status_code}). Please check your API Key status."
    except Exception as e:
        return f"⚠️ Connection failed: {str(e)}"

# 4. بيانات اللغات والنصائح المتغيرة
strings = {
    "العربية": {
        "welcome": "نظام BioHealth DZ الذكي 🏥", "enter": "دخول", "name": "الاسم الكامل",
        "menu_bmi": "📊 حاسبة الصحة", "menu_food": "🥘 تحليل الأطباق", "menu_lab": "🔬 الأسئلة المخبرية",
        "age": "العمر", "gender": "الجنس", "male": "ذكر", "female": "أنثى", "w": "الوزن (كغ)", "h": "الطول (سم)",
        "chronic": "الأمراض المزمنة", "sugar": "سكري", "press": "ضغط دم", "none": "لا يوجد",
        "btn": "تحليل الحالة الذكي ✨", "res": "النتائج والتوصيات:",
        "tips": ["🩺 شرب الماء بانتظام يحسن التركيز.", "🍏 الخضروات الورقية غنية بالحديد الضروري.", "🏃‍♂️ 10 دقائق من التمدد صباحاً تحسن مرونة المفاصل."]
    },
    "English": {
        "welcome": "BioHealth DZ Smart System 🏥", "enter": "Login", "name": "Full Name",
        "menu_bmi": "📊 Health Calc", "menu_food": "🥘 Food Analysis", "menu_lab": "🔬 Lab Questions",
        "age": "Age", "gender": "Gender", "male": "Male", "female": "Female", "w": "Weight (kg)", "h": "Height (cm)",
        "chronic": "Chronic Diseases", "sugar": "Diabetes", "press": "BP", "none": "None",
        "btn": "Analyze Now ✨", "res": "Results:",
        "tips": ["🩺 Hydration is key to overall health.", "🍏 Fiber-rich foods aid digestion.", "🏃‍♂️ Daily movement boosts mood and energy."]
    }
}

# 5. منطق الدخول واختيار اللغة (الواجهة الأولى)
if 'logged' not in st.session_state: st.session_state.logged = False

if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#1b5e20;'>🧪 BioHealth DZ</h2>", unsafe_allow_html=True)
        sel_lang = st.selectbox("Language / اللغة", ["العربية", "English"])
        u_name = st.text_input(strings[sel_lang]["name"])
        if st.button(strings[sel_lang]["enter"]):
            if u_name:
                st.session_state.logged, st.session_state.lang, st.session_state.user = True, sel_lang, u_name
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    T = strings[st.session_state.lang]
    st.markdown(f'<div class="main-header"><h1>{T["welcome"]}</h1><p>مرحباً، {st.session_state.user} 👋</p></div>', unsafe_allow_html=True)
    
    # النصيحة المتغيرة (تتغير عند كل دخول أو تحديث)
    st.markdown(f'<div class="tip-card">{random.choice(T["tips"])}</div>', unsafe_allow_html=True)

    # أزرار التنقل بين الأقسام
    nav1, nav2, nav3 = st.columns(3)
    if 'page' not in st.session_state: st.session_state.page = "bmi"
    
    if nav1.button(T["menu_bmi"]): st.session_state.page = "bmi"
    if nav2.button(T["menu_food"]): st.session_state.page = "food"
    if nav3.button(T["menu_lab"]): st.session_state.page = "lab"
    
    st.divider()

    # --- حاسبة الصحة ---
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
            with st.spinner("Analyzing..."):
                prompt = f"Provide health advice for a {age} years old {gender}, BMI: {bmi:.1f}, chronic: {chronic}."
                res = get_ai_response(prompt)
                st.markdown(f'<div class="advice-box"><b>{T["res"]}</b><br>{res}</div>', unsafe_allow_html=True)
