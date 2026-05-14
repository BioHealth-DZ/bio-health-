import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="BioHealth DZ", page_icon="🧪", layout="wide")

# 2. التنسيق وإخفاء أشرطة GitHub (للمظهر الاحترافي)
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display:none;}
    [data-testid="stHeader"] {display:none;}
    .stApp { background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%) !important; }
    .main-header {
        background: linear-gradient(90deg, #1b5e20, #43a047);
        color: white !important; padding: 15px; border-radius: 15px; text-align: center;
    }
    .history-box {
        background-color: #f1f8e9; border: 1px solid #c8e6c9;
        padding: 10px; border-radius: 10px; margin-top: 5px; font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. دالة الذكاء الاصطناعي
def get_ai_response(prompt):
    try:
        if "GEMINI_API_KEY" not in st.secrets: return "Error: API Key missing"
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")
        return model.generate_content(prompt).text
    except Exception as e: return f"Error: {str(e)}"

# 4. قاعدة البيانات (عربي، فرنسي، إنجليزي)
strings = {
    "العربية": {
        "welcome": "BioHealth DZ", "name": "الاسم الكامل", "enter": "دخول",
        "menu_bmi": "📊 حاسبة الصحة", "menu_food": "🥘 تحليل الغذاء", "menu_lab": "🔬 المخبر",
        "btn": "تحليل", "history": "📜 السجل (النتائج السابقة)", "no_history": "لا توجد نتائج محفوظة بعد"
    },
    "English": {
        "welcome": "Welcome to BioHealth DZ", "name": "Full Name", "enter": "Login",
        "menu_bmi": "📊 BMI Calculator", "menu_food": "🥘 Food Analysis", "menu_lab": "🔬 Lab Questions",
        "btn": "Analyze", "history": "📜 Result History", "no_history": "No results saved yet"
    },
    "Français": {
        "welcome": "Bienvenue sur BioHealth DZ", "name": "Nom Complet", "enter": "Entrer",
        "menu_bmi": "📊 Calcul IMC", "menu_food": "🥘 Analyse Plats", "menu_lab": "🔬 Labo",
        "btn": "Analyser", "history": "📜 Historique", "no_history": "Aucun résultat enregistré"
    }
}

# 5. إدارة الجلسة والسجل
if 'logged' not in st.session_state: st.session_state.logged = False
if 'history' not in st.session_state: st.session_state.history = []

if not st.session_state.logged:
    st.markdown("<h1 style='text-align:center;'>🧪 BioHealth DZ</h1>", unsafe_allow_html=True)
    sl = st.selectbox("Language / اللغة", ["العربية", "English", "Français"])
    un = st.text_input(strings[sl]["name"])
    if st.button(strings[sl]["enter"]):
        if un:
            st.session_state.logged, st.session_state.user, st.session_state.lang = True, un, sl
            st.rerun()
else:
    T = strings[st.session_state.lang]
    st.sidebar.title(f"👤 {st.session_state.user}")
    choice = st.sidebar.radio("Menu", [T["menu_bmi"], T["menu_food"], T["menu_lab"]])
    
    st.markdown(f'<div class="main-header"><h2>{T["welcome"]}</h2></div>', unsafe_allow_html=True)

    # --- قسم تحليل الغذاء ---
    if choice == T["menu_food"]:
        st.subheader(T["menu_food"])
        dish = st.text_input("Dish / الطبق")
        if st.button(T["btn"]):
            with st.spinner("..."):
                res = get_ai_response(f"Analyze the dish '{dish}' biochemically in {st.session_state.lang}.")
                st.session_state.history.append({"type": T["menu_food"], "item": dish, "result": res})
                st.info(res)

    # --- قسم BMI ---
    elif choice == T["menu_bmi"]:
        w = st.number_input("Weight (kg)", 30, 200, 70)
        h = st.number_input("Height (cm)", 100, 250, 170)
        if st.button(T["btn"]):
            bmi = w / ((h/100)**2)
            res = f"BMI: {bmi:.1f}"
            st.session_state.history.append({"type": T["menu_bmi"], "item": f"W:{w} H:{h}", "result": res})
            st.success(res)

    # --- قسم المخبر ---
    elif choice == T["menu_lab"]:
        q = st.text_area("Question?")
        if st.button(T["btn"]):
            res = get_ai_response(q)
            st.session_state.history.append({"type": T["menu_lab"], "item": q[:20], "result": res})
            st.write(res)

    # --- قسم عرض النتائج القديمة (السجل) ---
    st.divider()
    st.subheader(T["history"])
    if not st.session_state.history:
        st.write(T["no_history"])
    else:
        for entry in reversed(st.session_state.history):
            with st.expander(f"{entry['type']} - {entry['item']}"):
                st.write(entry['result'])

    if st.sidebar.button("Logout"):
        st.session_state.logged = False
        st.session_state.history = []
        st.rerun()
