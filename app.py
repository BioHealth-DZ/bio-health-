import streamlit as st
import google.generativeai as genai

# 1. إعداد الصفحة
st.set_page_config(page_title="BioHealth DZ", page_icon="🧪", layout="wide")

# 2. التنسيق وإضافة الخلفية (تأكدي من وضع رابط الصورة الصحيح هنا)
# ملاحظة: استبدلي 'YOUR_IMAGE_URL' برابط الصورة المباشر لتظهر
st.markdown("""
    <style>
    header {visibility: hidden;}
    .stApp {
        background-image: linear-gradient(rgba(255,255,255,0.8), rgba(255,255,255,0.8)), 
                          url("https://raw.githubusercontent.com/your-username/your-repo/main/watermarked_img_11248709154786756656.png");
        background-size: cover;
        background-attachment: fixed;
    }
    .main-header {
        background: linear-gradient(90deg, #1b5e20, #43a047);
        color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;
    }
    .advice-box {
        background-color: white; border-right: 5px solid #1b5e20;
        padding: 15px; border-radius: 10px; color: #1b5e20; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    div.stButton > button { background-color: #1b5e20; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. دالة الذكاء الاصطناعي - الحل النهائي لخطأ 404 (إجبار نسخة الموديل)
def get_ai_response(prompt):
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            return "Error: API Key missing in Secrets"
        
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # الحل لخطأ 404: نستخدم الاسم الكامل للموديل مع تحديد النسخة يدوياً
        # جربي هذا الاسم فهو الأكثر توافقاً مع v1beta المذكورة في صورتك
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        
        # محاولة توليد المحتوى
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # إذا فشل الأول، نجرب الاسم البديل
        try:
            model = genai.GenerativeModel(model_name="gemini-pro")
            return model.generate_content(prompt).text
        except:
            return f"خطأ في الاتصال بالموديل: {str(e)}"

# 4. واجهة التطبيق (بناءً على صورتك الأخيرة)
st.markdown('<div class="main-header"><h1>حاسبة الصحة 🧪</h1></div>', unsafe_allow_html=True)

# المدخلات كما في الصورة Capture d'écran 2026-05-14 165605.png
col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("العمر", 1, 100, 25)
with col2:
    gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
with col3:
    weight = st.number_input("الوزن (كغ)", 30.0, 200.0, 70.0)

col4, col5 = st.columns(2)
with col4:
    height = st.number_input("الطول (سم)", 100.0, 250.0, 170.0)
with col5:
    chronic = st.multiselect("الأمراض المزمنة", ["سكري", "ضغط دم", "لا يوجد"])

if st.button("تحليل"):
    bmi = weight / ((height/100)**2)
    st.markdown(f"### BMI: **{bmi:.1f}**")
    
    with st.spinner("جاري التحليل..."):
        # إرسال البيانات للموديل
        user_info = f"العمر: {age}, الجنس: {gender}, BMI: {bmi:.1f}, الأمراض: {chronic}"
        advice = get_ai_response(f"حلل هذه البيانات الصحية وقدم نصائح طبية مختصرة باللغة العربية: {user_info}")
        
        st.markdown(f'<div class="advice-box"><b>النتائج:</b><br>{advice}</div>', unsafe_allow_html=True)

# إضافة سجل بسيط أسفل الصفحة
st.divider()
st.caption("BioHealth DZ - تطوير طالب علوم بيولوجية")
