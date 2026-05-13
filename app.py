import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة والتصميم
st.set_page_config(page_title="منصة البيوكيمياء والصحة", page_icon="🧪", layout="wide")

# تصميم الواجهة الاحترافية
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #2e7d32;
        color: white;
        height: 3em;
        font-weight: bold;
    }
    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ضع مفتاحك هنا ---
API_KEY = "AIzaSyD9WBNpqzGhS47RfFrw0YqPb40TbB8dX9M" 
# -----------------------

# دالة لتشغيل الذكاء الاصطناعي بأمان
def get_ai_response(prompt):
    try:
        genai.configure(api_key=API_KEY)
        # جربنا هنا اسم الموديل الأكثر استقراراً
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"عذراً، حدث خطأ تقني بسيط. تأكد من صحة مفتاح API Key. الخطأ: {str(e)}"

st.title("🧪 منصة البيوكيمياء والصحة الجزائرية")
st.write("دليلك العلمي للصحة والغذاء بلمسة جزائرية ذكية")

menu = st.sidebar.selectbox("القائمة الرئيسية", 
    ["📊 حاسبة الصحة والوزن", "🔬 المحلل البيوكيميائي الذكي", "🥘 كيمياء المطبخ الجزائري"])

if menu == "📊 حاسبة الصحة والوزن":
    st.header("⚖️ تقييم الحالة الجسدية")
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("الوزن (كغ)", 30, 200, 70)
        height = st.number_input("الطول (سم)", 100, 250, 170)
    with col2:
        age = st.number_input("العمر", 10, 100, 25)
        health_status = st.selectbox("الحالة الصحية", ["طبيعي", "سكري", "ضغط دم مرتفع", "حامل", "مرضع"])

    if st.button("تحليل حالتي"):
        bmi = weight / ((height/100)**2)
        status = "نقص وزن" if bmi < 18.5 else "وزن مثالي" if bmi < 25 else "زيادة وزن"
        
        st.markdown(f"""<div class="result-card"><h3>نتيجتك: {bmi:.1f} - {status}</h3></div>""", unsafe_allow_html=True)
        
        with st.spinner("جاري جلب نصيحة مخصصة..."):
            prompt = f"أنا {health_status}، عمري {age}، طولي {height} ووزني {weight}. اعطني نصيحة غذائية قصيرة بلهجة جزائرية."
            text = get_ai_response(prompt)
            st.info(text)

elif menu == "🔬 المحلل البيوكيميائي الذكي":
    st.header("🔍 استشارة ذكية فورية")
    query = st.text_input("عن ماذا تبحث؟ (مثلاً: أضرار السكر الأبيض)")
    if st.button("تحليل الآن"):
        with st.spinner("جاري التحليل..."):
            res = get_ai_response(f"اشرح لي بلهجة جزائرية بسيطة: {query}")
            st.success(res)

elif menu == "🥘 كيمياء المطبخ الجزائري":
    st.header("🍽️ ماذا يوجد في طبقك؟")
    dish = st.text_input("اسم الطبق (مثلاً: كسكسي، محاجب)")
    if st.button("تحليل المكونات"):
        with st.spinner("تحليل الطبق..."):
            res = get_ai_response(f"حلل طبق {dish} كيميائياً وفوائده بلهجة جزائرية")
            st.warning(res)

st.sidebar.markdown("---")
st.sidebar.caption("🇩🇿 صنع بفخر لمساعدة الجزائريين")
