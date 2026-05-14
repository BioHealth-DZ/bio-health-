import streamlit as st
import google.generativeai as genai
import random
import time

# 1. إعداد الصفحة والتصميم
st.set_page_config(page_title="BioHealth DZ", page_icon="💊", layout="wide")

st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #f4fbf7; }
    .main-header {
        background: linear-gradient(135deg, #1b5e20 0%, #43a047 100%);
        color: white; padding: 30px; border-radius: 20px; text-align: center;
        margin-bottom: 20px;
    }
    .advice-box {
        background-color: white; border-right: 10px solid #2e7d32;
        padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    div.stButton > button {
        width: 100%; border-radius: 12px; height: 50px; font-weight: bold;
        background: linear-gradient(90deg, #1b5e20, #43a047); color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. إعداد الموديل (تم اختيار gemini-1.5-flash لأنه الأفضل في الحصة المجانية)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def get_ai_response(prompt):
    try:
        # قمنا بتثبيت هذا الموديل لأنه يدعم حتى 15 طلب في الدقيقة و1500 طلب في اليوم غالباً
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # إضافة تعليمات لتقليل حجم الرد (لتوفير الرصيد)
        full_prompt = f"أجب باللغة العربية باختصار مفيد ودقة طبية: {prompt}"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            return "❌ انتهت الحصة المجانية المتاحة حالياً. يرجى المحاولة بعد قليل (السيرفر تحت ضغط المستخدمين)."
        return f"⚠️ خطأ في الاتصال: {error_msg}"

# --- باقي الكود (بيانات اللغات والصفحات) كما هو تماماً دون تغيير ---
strings = {
    "العربية": {
        "welcome": "نظام BioHealth DZ الذكي 🏥", "enter": "دخول", "name": "الاسم الكامل",
        "menu_bmi": "📊 حاسبة الصحة", "menu_food": "🥘 تحليل الأطباق", "menu_lab": "🔬 الأسئلة المخبرية",
        "age": "العمر", "male": "ذكر", "female": "أنثى", "w": "الوزن (كغ)", "h": "الطول (سم)",
        "chronic": "الأمراض المزمنة", "sugar": "سكري", "press": "ضغط دم", "none": "لا يوجد",
        "btn": "تحليل الحالة الذكي ✨", "res": "النتائج والتوصيات:",
        "tips": ["🩺 شرب الماء بانتظام يحسن التركيز.", "🍏 الخضروات الورقية غنية بالحديد."]
    },
    "English": {
        "welcome": "BioHealth DZ Smart System 🏥", "enter": "Login", "name": "Full Name",
        "menu_bmi": "📊 Health Calc", "menu_food": "🥘 Food Analysis", "menu_lab": "🔬 Lab Questions",
        "age": "Age", "male": "Male", "female": "Female", "w": "Weight (kg)", "h": "Height (cm)",
        "chronic": "Chronic Diseases", "sugar": "Diabetes", "press": "BP", "none": "None",
        "btn": "Analyze Now ✨", "res": "Results:",
        "tips": ["🩺 Hydration is key to overall health.", "🍏 Fiber-rich foods aid digestion."]
    }
}

if 'logged' not in st.session_state: st.session_state.logged = False

if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown("<h2 style='text-align:center;'>🧪 BioHealth DZ</h2>", unsafe_allow_html=True)
        sel_lang = st.selectbox("Language / اللغة", ["العربية", "English"])
        u_name = st.text_input(strings[sel_lang]["name"])
        if st.button(strings[sel_lang]["enter"]):
            if u_name:
                st.session_state.logged, st.session_state.lang, st.session_state.user = True, sel_lang, u_name
                st.rerun()
else:
    T = strings[st.session_state.lang]
    st.markdown(f'<div class="main-header"><h1>{T["welcome"]}</h1><p>مرحباً، {st.session_state.user} 👋</p></div>', unsafe_allow_html=True)
    
    nav1, nav2, nav3 = st.columns(3)
    if 'page' not in st.session_state: st.session_state.page = "bmi"
    if nav1.button(T["menu_bmi"]): st.session_state.page = "bmi"
    if nav2.button(T["menu_food"]): st.session_state.page = "food"
    if nav3.button(T["menu_lab"]): st.session_state.page = "lab"
    
    st.divider()

    if st.session_state.page == "bmi":
        col1, col2, col3 = st.columns(3)
        with col1: age = st.number_input(T["age"], 1, 100, 25)
        with col2: weight = st.number_input(T["w"], 30.0, 200.0, 70.0)
        with col3: height = st.number_input(T["h"], 100.0, 250.0, 170.0)
        chronic = st.multiselect(T["chronic"], [T["sugar"], T["press"], T["none"]])
        
        if st.button(T["btn"]):
            bmi = weight / ((height/100)**2)
            st.markdown(f"### BMI: **{bmi:.1f}**")
            with st.spinner("جاري التحليل..."):
                res = get_ai_response(f"نصيحة لشخص عمره {age} وكتلة جسمه {bmi:.1f} وأمراضه {chronic}")
                st.markdown(f'<div class="advice-box"><b>{T["res"]}</b><br>{res}</div>', unsafe_allow_html=True)

    elif st.session_state.page == "food":
        food_query = st.text_input("إسم الطبق")
        if st.button("تحليل"):
            with st.spinner("..."):
                res = get_ai_response(f"حلل القيمة الغذائية لطبق {food_query}")
                st.markdown(f'<div class="advice-box">{res}</div>', unsafe_allow_html=True)

    elif st.session_state.page == "lab":
        lab_query = st.text_area("سؤالك المخبري")
        if st.button("بحث"):
            with st.spinner("..."):
                res = get_ai_response(f"اشرح مخبرياً: {lab_query}")
                st.markdown(f'<div class="advice-box">{res}</div>', unsafe_allow_html=True)
