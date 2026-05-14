import streamlit as st
import requests
import json
import random

# 1. إعدادات الصفحة
st.set_page_config(page_title="BioHealth DZ", page_icon="💊", layout="wide")

# 2. التنسيق الجمالي مع الألوان والرموز
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
        background: linear-gradient(135deg, #0a4d2e 0%, #1b5e20 100%);
        color: white !important; padding: 30px; border-radius: 20px; text-align: center;
        margin-bottom: 25px; box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    .daily-tip {
        background-color: #e8f5e9; border-right: 5px solid #2e7d32;
        padding: 15px; border-radius: 10px; color: #1b5e20; font-weight: bold;
        margin-bottom: 20px; text-align: center;
    }
    .advice-box {
        background-color: white; border-right: 10px solid #2e7d32;
        padding: 25px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    div.stButton > button {
        background: #1b5e20; color: white; border-radius: 12px; height: 50px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. دالة النصيحة المتغيرة
def get_daily_tip(lang):
    tips = {
        "العربية": [
            "🩺 شرب الماء بانتظام يحسن من كفاءة الدورة الدموية.",
            "🍏 تفاحة في اليوم تغنيك عن زيارة الطبيب.",
            "🏃‍♂️ المشي لمدة 30 دقيقة يومياً يقلل من مخاطر أمراض القلب.",
            "😴 النوم الكافي (7-8 ساعات) ضروري لترميم خلايا الجسم."
        ],
        "English": [
            "🩺 Drinking water regularly improves blood circulation.",
            "🍏 An apple a day keeps the doctor away.",
            "🏃‍♂️ Walking 30 mins a day reduces heart disease risks.",
            "😴 Quality sleep is essential for body cell repair."
        ]
    }
    return random.choice(tips.get(lang, tips["العربية"]))

# 4. دالة الذكاء الاصطناعي (حل مشكلة الخطأ في الصورة)
def get_ai_response(prompt):
    if "GEMINI_API_KEY" not in st.secrets: return "Missing API Key"
    
    api_key = st.secrets["GEMINI_API_KEY"]
    # المحاولة مع موديلات مختلفة لتجنب خطأ الـ 404 أو الفشل
    models = ["gemini-1.5-flash", "gemini-pro"]
    
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
            if resp.status_code == 200:
                return resp.json()['candidates'][0]['content']['parts'][0]['text']
        except: continue
    return "⚠️ عذراً، لا يزال السيرفر يرفض الاتصال. تأكد من إعدادات الـ API في Streamlit Cloud."

# 5. اللغات
strings = {
    "العربية": {"welcome": "نظام BioHealth DZ الذكي 🏥", "name": "اسم المستخدم", "enter": "دخول"},
    "English": {"welcome": "BioHealth DZ Smart System 🏥", "name": "Username", "enter": "Login"}
}

# 6. منطق التطبيق
if 'logged' not in st.session_state: st.session_state.logged = False

if not st.session_state.logged:
    st.markdown("<h1 style='text-align:center;'>🧪 BioHealth DZ</h1>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 1.5, 1])
    with col_m:
        lang = st.selectbox("Language / اللغة", ["العربية", "English"])
        name = st.text_input(strings[lang]["name"])
        if st.button(strings[lang]["enter"]):
            if name: 
                st.session_state.logged, st.session_state.lang, st.session_state.user = True, lang, name
                st.rerun()
else:
    T = strings[st.session_state.lang]
    st.markdown(f'<div class="main-header"><h1>{T["welcome"]}</h1></div>', unsafe_allow_html=True)
    
    # عرض النصيحة المتغيرة
    st.markdown(f'<div class="daily-tip">{get_daily_tip(st.session_state.lang)}</div>', unsafe_allow_html=True)
    
    # واجهة الحاسبة (مبسطة للتأكد من العمل)
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("الوزن (kg) ⚖️", 30, 200, 70)
    with col2:
        height = st.number_input("الطول (cm) 📏", 100, 250, 170)
        
    if st.button("تحليل الحالة الذكي ✨"):
        bmi = weight / ((height/100)**2)
        st.write(f"### BMI: {bmi:.1f}")
        with st.spinner("جاري التحليل..."):
            res = get_ai_response(f"نصيحة طبية لمستخدم BMI الخاص به هو {bmi:.1f}")
            st.markdown(f'<div class="advice-box"><b>النتائج والتوصيات:</b><br>{res}</div>', unsafe_allow_html=True)
