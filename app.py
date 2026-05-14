# 3. محرك الذكاء الاصطناعي المطوّر لتجاوز خطأ الـ Quota
def get_ai_response(prompt):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # جلب قائمة بكل الموديلات المتاحة في حسابك
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # ترتيب المحاولة: البدء بـ Flash 1.5 ثم Pro ثم الموديلات الأقدم لضمان العمل
        priority_models = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]
        
        selected_model = None
        for m_name in priority_models:
            if m_name in available_models:
                selected_model = m_name
                break
        
        if not selected_model:
            selected_model = available_models[0] # اختيار أي موديل متاح إذا لم يجد المفضلين
            
        model = genai.GenerativeModel(selected_model)
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        # إذا استمر الخطأ 429 (انتهاء الكوتا)، سنظهر رسالة لطيفة للمستخدم
        if "429" in str(e):
            return "⚠️ عذراً، تم الوصول للحد الأقصى من الطلبات المجانية حالياً. يرجى الانتظار دقيقة ثم إعادة المحاولة أو تجربة متصفح آخر."
        return f"حدث خطأ في الاتصال: {str(e)}"

# تأكدي أن جزء "تحليل الغذاء" يستخدم نفس الدالة:
if choice == T["menu_food"]:
    st.subheader(T["menu_food"])
    dish = st.text_input("اسم الطبق / Nom du plat", key="dish_input")
    if st.button("Analyze", key="analyze_dish"):
        if dish:
            with st.spinner("جاري التحليل..."):
                # أضفنا سياقاً لضمان جودة الرد
                prompt_food = f"أنت خبير تغذية بيوكيميائي. حلل المكونات الكيميائية لطبق {dish} وفوائدها وأضرارها بالدراجة الجزائرية."
                res = get_ai_response(prompt_food)
                st.markdown(f'<div class="advice-box">{res}</div>', unsafe_allow_html=True)
        else:
            st.warning("يرجى إدخال اسم الطبق أولاً")
