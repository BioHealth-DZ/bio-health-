import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="منصة البيوكيمياء والصحة الجزائرية", page_icon="🧪", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                    url('https://images.unsplash.com/photo-1576086213369-97a306d36557?q=80&w=2000');
        background-size: cover;
    }
    .main-title { color: #1b5e20; text-align: center; font-size: 2.8rem; font-weight: bold; }
    .result-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border-right: 10px solid #2e7d32; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .info-box { background-color: #e8f5e9; border-radius: 10px; padding: 15px; margin-top: 10px; border: 1px solid #2e7d32; }
    .stButton>button { background: #2e7d32; color: white; border-radius: 25px; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 🔑 ضع مفتاحك الجديد هنا (تأكد أنه جديد وغير محظور) ---
API_KEY = "AIzaSyBKvFfji6lkjNNYxraI9OS0pZK5_bIt-Ew"
# -------------------------------------------------------

def get_ai_response(prompt):
    if "الجـديد" in API_KEY or not API_KEY:
        return "⚠️ يرجى وضع مفتاح API الجديد في الكود."
    try:
        genai.configure(api_key=API_KEY.strip())
        
        # محاولة ذكية لتجربة الموديلات المتاحة لتجنب خطأ 404
        try:
            model = genai.GenerativeModel('gemini-pro') # جرب البرو أولاً لأنه الأكثر استقراراً في المكتبات القديمة
        except:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ عذراً، هناك مشكلة في الاتصال. تأكد من المفتاح. (الخطأ: {str(e)})"

# واجهة المستخدم
st.markdown('<p class="main-title">🧪 منصة البيوكيمياء والصحة الجزائرية</p>', unsafe_allow_html=True)

menu = st.sidebar.selectbox("القائمة الرئيسية", ["📊 حاسبة الصحة والوزن", "🔬 المحلل البيوكيميائي", "🥘 كيمياء المطبخ"])

if menu == "📊 حاسبة الصحة والوزن":
    st.header("⚖️ تقييم الحالة الجسدية")
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("الوزن (كغ)", 30, 200, 75)
        height = st.number_input("الطول (سم)", 100, 250, 170)
        age = st.number_input("العمر", 5, 100, 25)
    with col2:
        gender = st.radio("الجنس", ["ذكر", "أنثى"])
        status = st.selectbox("الحالة الصحية", ["طبيعي", "سكري", "ضغط دم", "حامل", "مرضعة"])
    
    if st.button("إجراء التحليل البيوكيميائي"):
        bmi = weight / ((height/100)**2)
        
        # تحديد لون وحالة النتيجة
        if bmi < 18.5:
            meaning, color = "نقص في الوزن: جسمك يحتاج لتغذية أكثر.", "#fbc02d"
        elif 18.5 <= bmi < 25:
            meaning, color = "وزن مثالي: تبارك الله، أنت في النطاق الصحي تماماً.", "#2e7d32"
        elif 25 <= bmi < 30:
            meaning, color = "زيادة في الوزن: انتبه، بدأت تدخل في نطاق الوزن الزائد.", "#ef6c00"
        else:
            meaning, color = "سمنة: وزنك قد يرهق قلبك ومفاصلك، ينصح بنظام غذائي.", "#c62828"

        st.markdown(f"""
        <div class="result-card">
            <h3 style="color:{color};">كتلة الجسم (BMI): {bmi:.1f}</h3>
            <div class="info-box">
                <b>💡 ماذا تعني هذه النتيجة؟</b><br>
                هذا الرقم يخبرنا بمدى تناسق وزنك مع طولك. حالتك حالياً: <b>{meaning}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("جاري تحليل بياناتك..."):
            res = get_ai_response(f"أنا {gender} عمري {age} وحالتي {status} بكتلة جسم {bmi:.1f}. انصحني بالجزائرية.")
            st.info(res)

elif menu == "🔬 المحلل البيوكيميائي":
    query = st.text_area("اطرح سؤالك العلمي:")
    if st.button("تحليل الآن"):
        st.write(get_ai_response(f"اشرح لي بالجزائرية: {query}"))

elif menu == "🥘 كيمياء المطبخ":
    dish = st.text_input("اسم الطبق الجزائري:")
    if st.button("كشف الأسرار"):
        st.write(get_ai_response(f"حلل طبق {dish} كيميائياً بالجزائرية"))
