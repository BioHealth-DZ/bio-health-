import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="منصة البيوكيمياء والصحة", page_icon="🧪", layout="wide")

# تصميم الواجهة
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #2e7d32; color: white; font-weight: bold; }
    .result-card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #333; }
    </style>
    """, unsafe_allow_html=True)

# --- ضع مفتاحك هنا ---
API_KEY = "AIzaSyD9WBNpqzGhS47RfFrw0YqPb40TbB8dX9M" 
# -----------------------

def get_ai_response(prompt):
    try:
        genai.configure(api_key=API_KEY)
        # هذا السطر هو التعديل السحري: نجرب الموديل الأحدث والأكثر توافقاً
        model = genai.GenerativeModel('gemini-1.5-flash-latest') 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # إذا فشل الأول، نجرب البديل الكلاسيكي
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
        except:
            return "عذراً، يبدو أن هناك ضغطاً على الخادم أو المفتاح يحتاج مراجعة. حاول مرة أخرى بعد لحظات."

st.title("🧪 منصة البيوكيمياء والصحة الجزائرية")

menu = st.sidebar.selectbox("القائمة الرئيسية", ["📊 حاسبة الصحة", "🔬 المحلل الذكي", "🥘 المطبخ الجزائري"])

if menu == "📊 حاسبة الصحة":
    st.header("⚖️ تقييم الحالة الجسدية")
    c1, c2 = st.columns(2)
    weight = c1.number_input("الوزن (كغ)", 30, 200, 70)
    height = c2.number_input("الطول (سم)", 100, 250, 170)
    status = st.selectbox("الحالة الصحية", ["طبيعي", "سكري", "ضغط دم", "حامل"])
    
    if st.button("تحليل حالتي"):
        bmi = weight / ((height/100)**2)
        st.markdown(f'<div class="result-card"><h3>كتلة الجسم: {bmi:.1f}</h3></div>', unsafe_allow_html=True)
        with st.spinner("جاري استشارة الذكاء الاصطناعي..."):
            res = get_ai_response(f"أنا {status} وكتلة جسمي {bmi:.1f}. اعطني نصيحة غذائية جزائرية قصيرة.")
            st.info(res)

elif menu == "🔬 المحلل الذكي":
    query = st.text_input("عن ماذا تبحث؟")
    if st.button("تحليل"):
        with st.spinner("انتظر قليلاً..."):
            st.success(get_ai_response(f"اشرح لي بلهجة جزائرية: {query}"))

elif menu == "🥘 المطبخ الجزائري":
    dish = st.text_input("اسم الطبق الجزائري")
    if st.button("تحليل الطبق"):
        with st.spinner("جاري تحليل المكونات..."):
            st.warning(get_ai_response(f"حلل فوائد طبق {dish} كيميائياً بالجزائرية"))
