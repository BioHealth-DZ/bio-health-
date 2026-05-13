import streamlit as st
import google.generativeai as genai

# جلب المفتاح بأمان
API_KEY = st.secrets.get("GEMINI_API_KEY")

def get_ai_response(prompt):
    if not API_KEY: return "⚠️ يرجى إضافة المفتاح في Secrets"
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(prompt).text
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

# تصميم الواجهة (إعادة الألوان)
st.set_page_config(page_title="منصة البيوكيمياء الجزائرية", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .main-title { color: #2e7d32; text-align: center; font-size: 2.5rem; font-weight: bold; }
    .result-box { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🧪 منصة البيوكيمياء والصحة الجزائرية</p>', unsafe_allow_html=True)

weight = st.number_input("الوزن (كغ)", 30, 200, 75)
height = st.number_input("الطول (سم)", 100, 250, 170)

if st.button("تحليل الحالة"):
    bmi = weight / ((height/100)**2)
    st.markdown(f'<div class="result-box"><h3>مؤشر كتلة جسمك هو: {bmi:.1f}</h3>', unsafe_allow_html=True)
    
    if bmi < 18.5: st.warning("نقص في الوزن")
    elif 18.5 <= bmi < 25: st.success("وزن مثالي")
    else: st.error("زيادة في الوزن")
    
    with st.spinner("جاري جلب نصيحة الخبير..."):
        res = get_ai_response(f"نصيحة طبية بالجزائرية لشخص كتلة جسمه {bmi:.1f}")
        st.info(res)
