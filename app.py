import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة والتصميم
st.set_page_config(page_title="منصة البيوكيمياء والصحة", page_icon="🧪", layout="wide")

# تصميم CSS لجعل الواجهة احترافية
st.markdown("""
    <style>
    .main {
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
    }
    </style>
    """, unsafe_allow_html=True)

# --- ضع مفتاحك هنا ---
API_KEY = "AIzaSyD9WBNpqzGhS47RfFrw0YqPb40TbB8dX9M" 
# -----------------------

# إعداد الذكاء الاصطناعي
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("تأكد من وضع مفتاح API Key بشكل صحيح في الكود.")

st.title("🧪 منصة البيوكيمياء والصحة الجزائرية")
st.write("دليلك العلمي للصحة والغذاء بلمسة جزائرية ذكية")

menu = st.sidebar.selectbox("القائمة الرئيسية", 
    ["📊 حاسبة الصحة والوزن", "🔬 المحلل البيوكيميائي الذكي", "🥘 كيمياء المطبخ الجزائري"])

if menu == "📊 حاسبة الصحة والوزن":
    st.header("⚖️ تقييم الحالة الجسدية")
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("الوزن (كغ)", 30, 200, 70)
            height = st.number_input("الطول (سم)", 100, 250, 170)
        with col2:
            age = st.number_input("العمر", 10, 100, 25)
            health_status = st.selectbox("الحالة الصحية (اختياري)", 
                ["طبيعي", "سكري", "ضغط دم مرتفع", "حامل", "مرضع"])

    if st.button("تحليل حالتي"):
        bmi = weight / ((height/100)**2)
        status = ""
        tips = ""
        
        if bmi < 18.5:
            status = "نقص في الوزن"
            tips = "تحتاج لأطعمة غنية بالطاقة مثل: الروينة، التمر، زيت الزيتون، والمكسرات."
        elif 18.5 <= bmi < 25:
            status = "وزن مثالي"
            tips = "حافظ على نظامك الغذائي مع شرب الكثير من الماء."
        else:
            status = "زيادة في الوزن"
            tips = "قلل من الخبز الأبيض والسكريات، وركز على الشربة والسلطات الجزائرية الغنية بالألياف."

        st.markdown(f"""
        <div class="result-card">
            <h3>نتيجتك: {bmi:.1f} - {status}</h3>
            <p>💡 <b>نصيحة سريعة:</b> {tips}</p>
        </div>
        """, unsafe_allow_html=True)

        if health_status != "طبيعي":
            with st.spinner("جاري جلب نصيحة طبية مخصصة..."):
                prompt = f"أنا شخص عمري {age} ووزني {weight} وطولي {height} وحالتي {health_status}. قدم لي نصيحة غذائية بيوكيمائية قصيرة جداً بلهجة جزائرية."
                res = model.generate_content(prompt)
                st.warning(f"🔔 نصيحة خاصة لـ {health_status}:")
                st.write(res.text)

elif menu == "🔬 المحلل البيوكيميائي الذكي":
    st.header("🔍 استشارة ذكية فورية")
    query = st.text_area("عن ماذا تبحث؟ (مثلاً: تأثير شرب الشاي بعد الأكل مباشرة كيميائياً)")
    
    if st.button("تحليل المادة"):
        with st.spinner("الذكاء الاصطناعي يحلل الآن..."):
            prompt = f"اشرح لي بلهجة جزائرية وبأسلوب علمي مبسط جداً: {query}"
            res = model.generate_content(prompt)
            st.success("التحليل الكيميائي الحيوي:")
            st.write(res.text)

elif menu == "🥘 كيمياء المطبخ الجزائري":
    st.header("🍽️ ماذا يوجد في طبقك؟")
    dish = st.text_input("اكتب اسم الطبق الجزائري (مثال: طعام، شربة فريك، محاجب)")
    
    if st.button("تحليل الطبق"):
        with st.spinner("تحليل المكونات..."):
            prompt = f"حلل طبق {dish} من ناحية السعرات، الفوائد، وتأثيره الكيميائي على الجسم. تحدث بلهجة جزائرية."
            res = model.generate_content(prompt)
            st.info(f"تقرير عن {dish}:")
            st.write(res.text)

st.sidebar.markdown("---")
st.sidebar.info("💡 نصيحة اليوم: استبدل السكر الأبيض بالتمر الجزائري لتحسين تفاعلات الأنسولين في جسمك!")
