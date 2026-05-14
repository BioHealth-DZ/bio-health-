import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والتنسيق (CSS)
st.set_page_config(page_title="BioHealth DZ", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-header {
        background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
        color: white; padding: 2rem; border-radius: 15px; text-align: center;
        margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .advice-box {
        background-color: white; padding: 20px; border-radius: 10px;
        border-right: 5px solid #2e7d32; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. إعداد الاتصال بجوجل (تأكدي من وضع المفتاح في Secrets)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ يرجى إضافة GEMINI_API_KEY في إعدادات Secrets")

def get_ai_response(prompt):
    try:
        # استخدام نسخة 'latest' لضمان التوافق مع v1beta وتجاوز خطأ 404
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        response = model.generate_content(
            f"أجب باللغة العربية باختصار ودقة طبية: {prompt}",
            generation_config=genai.types.GenerationConfig(temperature=0.7)
        )
        return response.text
    except Exception as e:
        err = str(e)
        if "429" in err:
            return "❌ عذراً، انتهت حصة الأسئلة المجانية لهذا اليوم (20 طلب). يرجى العودة غداً."
        elif "404" in err:
            return "⚠️ الموديل غير متوفر حالياً، جاري تحديث الاتصال..."
        return f"⚠️ خطأ فني: {err}"

# 3. نظام تسجيل الدخول البسيط
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<div class='main-header'><h1>BioHealth DZ 🏥</h1><p>مرحباً بك في نظام التحليل الصحي</p></div>", unsafe_allow_html=True)
    with st.container():
        name = st.text_input("الاسم الكامل")
        if st.button("دخول النظام"):
            if name:
                st.session_state.logged_in = True
                st.session_state.user_name = name
                st.rerun()
else:
    # 4. الواجهة الرئيسية بعد الدخول
    st.markdown(f"<div class='main-header'><h1>BioHealth DZ</h1><p>مرحباً دكتور(ة) {st.session_state.user_name}</p></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 حاسبة BMI", "🧪 استفسار مخبري", "🥘 تحليل غذائي"])

    with tab1:
        st.subheader("حساب مؤشر كتلة الجسم")
        col1, col2 = st.columns(2)
        w = col1.number_input("الوزن (كجم)", 30.0, 200.0, 70.0)
        h = col2.number_input("الطول (سم)", 100.0, 250.0, 170.0)
        if st.button("احسب وحلل"):
            bmi = w / ((h/100)**2)
            st.info(f"مؤشر كتلة جسمك هو: {bmi:.1f}")
            with st.spinner("جاري استشارة الذكاء الاصطناعي..."):
                ans = get_ai_response(f"قدم نصيحة قصيرة لشخص مؤشر كتلة جسمه {bmi:.1f}")
                st.markdown(f"<div class='advice-box'>{ans}</div>", unsafe_allow_html=True)

    with tab2:
        st.subheader("الأسئلة المخبرية والعلمية")
        q = st.text_area("اكتب سؤالك (مثلاً: ما هي خطوات صبغة غرام؟)")
        if st.button("تحليل مخبري"):
            with st.spinner("جاري البحث في المصادر..."):
                ans = get_ai_response(q)
                st.markdown(f"<div class='advice-box'>{ans}</div>", unsafe_allow_html=True)

    with tab3:
        st.subheader("تحليل الأطباق الجزائرية")
        dish = st.text_input("اسم الطبق (مثلاً: كسكسي، شربة)")
        if st.button("تحليل القيمة الغذائية"):
            with st.spinner("جاري التحليل..."):
                ans = get_ai_response(f"ما هي القيمة الغذائية لطبق {dish}؟")
                st.markdown(f"<div class='advice-box'>{ans}</div>", unsafe_allow_html=True)

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()
