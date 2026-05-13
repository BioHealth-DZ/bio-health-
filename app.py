import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة المتقدمة
st.set_page_config(page_title="منصة البيوكيمياء والصحة الجزائرية", page_icon="🧪", layout="wide")

# 2. تصميم CSS احترافي (خلفية، ألوان، وتنسيق)
st.markdown("""
    <style>
    /* خلفية متدرجة وتصميم عصري */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), 
                    url('https://images.unsplash.com/photo-1532187875605-2fe3587b1598?q=80&w=2070');
        background-size: cover;
        background-attachment: fixed;
    }
    
    .main-title { color: #1b5e20; text-align: center; font-size: 3rem; font-weight: bold; text-shadow: 2px 2px 4px #ccc; }
    
    /* تنسيق الكروت والنتائج */
    .result-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 20px;
        border-right: 10px solid #2e7d32;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #2e7d32, #43a047);
        color: white;
        border-radius: 30px;
        padding: 10px 25px;
        font-size: 1.2rem;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
    </style>
    """, unsafe_allow_html=True)

# --- ضع مفتاحك هنا ---
API_KEY = "AIzaSyD9WBNpqzGhS47RfFrw0YqPb40TbB8dX9M" 
# -----------------------

# دالة ذكية للاتصال بجوجل (تجرب عدة موديلات لضمان العمل)
def get_ai_response(prompt):
    try:
        genai.configure(api_key=API_KEY)
        # محاولة استخدام أحدث موديل
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except:
        try:
            # محاولة الموديل البديل إذا فشل الأول
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
        except:
            return "❌ خطأ في الاتصال: تأكد من لصق مفتاح API بشكل صحيح أو جرب تحديث الصفحة."

# الواجهة الرئيسية
st.markdown('<h1 class="main-title">🧪 منصة البيوكيمياء والصحة الجزائرية</h1>', unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>دليلك العلمي للصحة والغذاء بلمسة جزائرية أصيلة 🇩🇿</h3>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("القائمة الرئيسية", 
    ["📊 حاسبة الصحة والوزن", "🔬 المحلل البيوكيميائي الذكي", "🥘 كيمياء المطبخ الجزائري"])

if menu == "📊 حاسبة الصحة والوزن":
    st.header("⚖️ تقييم الحالة الجسدية الشامل")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        weight = st.number_input("الوزن (كغ)", 30, 200, 75)
        age = st.number_input("العمر", 5, 100, 25)
    with col2:
        height = st.number_input("الطول (سم)", 100, 250, 170)
        gender = st.radio("الجنس", ["ذكر", "أنثى"])
    with col3:
        activity = st.selectbox("مستوى النشاط", ["خامل", "نشاط متوسط", "رياضي جداً"])
        health_status = st.selectbox("الحالة الخاصة", ["طبيعي", "سكري", "ضغط دم", "مرأة حامل", "مرأة مرضعة", "حمية خاصة"])

    if st.button("إجراء التحليل البيوكيميائي"):
        bmi = weight / ((height/100)**2)
        
        # تصنيف الحالة
        if bmi < 18.5: status, color = "نقص في الوزن", "#ff9800"
        elif bmi < 25: status, color = "وزن مثالي ما شاء الله", "#4caf50"
        elif bmi < 30: status, color = "زيادة في الوزن", "#f44336"
        else: status, color = "سمنة - تنبيه صحي", "#b71c1c"
        
        st.markdown(f"""
        <div class="result-card">
            <h2 style="color:{color};">النتيجة: {status}</h2>
            <p><b>كتلة الجسم (BMI):</b> {bmi:.1f}</p>
            <hr>
            <h4>📋 نصيحة الخبير الذكي (بناءً على حالتك كـ {health_status}):</h4>
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("جاري تحليل بياناتك الحيوية..."):
            prompt = f"أنا {gender}، عمري {age}، وحالتي {health_status}. كتلة جسمي هي {bmi:.1f}. قدم لي نصائح غذائية ورياضية بلهجة جزائرية محببة وواضحة."
            advice = get_ai_response(prompt)
            st.write(advice)

elif menu == "🔬 المحلل البيوكيميائي الذكي":
    st.header("🔍 استشارة علمية فورية")
    query = st.text_area("اطرح سؤالك العلمي (مثلاً: ما تأثير المشروبات الغازية على العظام؟)", height=150)
    if st.button("تحليل المادة كيميائياً"):
        with st.spinner("جاري مراجعة المراجع العلمية..."):
            res = get_ai_response(f"اشرح لي من الناحية البيوكيميائية وبلهجة جزائرية بسيطة: {query}")
            st.markdown(f'<div class="result-card">{res}</div>', unsafe_allow_html=True)

elif menu == "🥘 كيمياء المطبخ الجزائري":
    st.header("🍽️ تحليل الأطباق التقليدية")
    dish = st.text_input("اسم الطبق (مثلاً: شربة فريك، طعام، شخشوخة)")
    if st.button("كشف أسرار الطبق"):
        with st.spinner("جاري تحليل المكونات..."):
            res = get_ai_response(f"حلل طبق {dish} الجزائري: مكوناته الأساسية، فوائده الكيميائية، وسعراته التقريبية بالجزائرية.")
            st.markdown(f'<div class="result-card">{res}</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.info("💡 **نصيحة اليوم:** اشرب الماء بكثرة، فالحياة تبدأ من خلية رطبة!")
