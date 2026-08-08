import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Eva Vet Science - Equine Survey", page_icon="🐴", layout="wide")

# --- DATABASE SETUP (Local CSV Storage) ---
DATA_FILE = "survey_responses.csv"

if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=[
        "Category", "Supplement_Types", "Ease_Of_Administration", 
        "Preferred_Form", "Visible_Results_Time", "Value_For_Money", 
        "Key_Decision_Factor", "Feedback"
    ])
    df_init.to_csv(DATA_FILE, index=False)

def save_response(data_dict):
    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# --- APP NAVIGATION ---
st.sidebar.title("🐴 Eva Vet Science")
mode = st.sidebar.radio("اختر الوجهة / Select Mode:", ["تعبئة الاستبيان (Take Survey)", "لوحة التحليلات (Surveyor Dashboard)"])

# ==========================================
# MODE 1: TAKE SURVEY (للعملاء والأطباء)
# ==========================================
if mode == "تعبئة الاستبيان (Take Survey)":
    st.title("🐴 Eva Vet Science - Equine Supplements Survey")
    st.write("نقدر وقتك وملاحظاتك لتطوير أفضل المكملات الغذائية للخيل. الاستبيان يستغرق أقل من دقيقتين.")
    
    category = st.selectbox(
        "من فضل اختر الفئة التي تنتمي إليها / Select your category:",
        ["مربّي / صاحب خيل / مدير إصطبل (Owner/Stable Manager)", 
         "تاجر / مستلزمات خيل / موزع (Retailer/Distributor)", 
         "طبيب بيطري خيل (Equine Veterinarian)"]
    )
    
    st.divider()
    
    with st.form("survey_form"):
        # Question 1
        supp_types = st.multiselect(
            "1. ما هي أنواع المكملات الغذائية التي تستخدمها/توصي بها حالياً؟",
            ["مفاصل وحركة (Joint & Mobility)", "جهاز هضمي ومعدة (Digestive & Gut Health)", 
             "أملاح واستشفاء (Electrolytes & Recovery)", "حوافر وجلد وشعر (Hoof & Coat)", 
             "تهدئة وسلوك (Calming)", "فيتامينات ومعادن عامة (Multivitamins)"]
        )
        
        # Question 2
        ease = st.select_slider(
            "2. ما مدى سهولة إعطاء المكمل الخيل؟ (1 = صعب جداً, 5 = سهل جداً)",
            options=[1, 2, 3, 4, 5], value=4
        )
        
        # Question 3
        pref_form = st.selectbox(
            "3. ما هو الشكل المفضل لديك للمكملات؟",
            ["مكعبات / Pellets", "سائل / Liquid", "بودرة / Powder", "معجون / Oral Paste"]
        )
        
        # Question 4
        results_time = st.selectbox(
            "4. خلال كم ظهرت التحسنات والنتائج على الخيل؟",
            ["خلال 1-2 أسبوع", "خلال 3-4 أسابيع", "أكثر من شهر", "لم ألاحظ تحسن"]
        )
        
        # Question 5
        value = st.radio(
            "5. تقييم السعر مقابل الجودة والنتائج:",
            ["ممتاز يستحق", "مناسب", "مرتفع مقارنة بالبدائل"]
        )
        
        # Question 6
        factor = st.selectbox(
            "6. العامل الأهم لديك عند اختيار مكمل جديد:",
            ["توصية الطبيب البيطري", "إقبال الخيل عليه (الطعم/الرائحة)", "المكونات الموثوقة والعلمية", "السعر وحجم العبوة"]
        )
        
        # Question 7
        feedback = st.text_area("7. اقتراحات أو ملاحظات إضافية للتطوير (اختياري):")
        
        submitted = st.form_submit_button("إرسال الاستبيان / Submit Survey")
        
        if submitted:
            response_data = {
                "Category": category,
                "Supplement_Types": ", ".join(supp_types),
                "Ease_Of_Administration": ease,
                "Preferred_Form": pref_form,
                "Visible_Results_Time": results_time,
                "Value_For_Money": value,
                "Key_Decision_Factor": factor,
                "Feedback": feedback
            }
            save_response(response_data)
            st.success("✅ تم إرسال إجابتك بنجاح! شكراً لوقتك ومشاركتك.")

# ==========================================
# MODE 2: SURVEYOR DASHBOARD (للمسؤول فقط)
# ==========================================
else:
    st.title("🔒 Surveyor Dashboard & AI Analysis")
    
    # PASSCODE PROTECTION
    passcode = st.text_input("أدخل كود المرور للوصول للنتائج (Enter Surveyor Passcode):", type="password")
    
    if passcode == "eva2026":  # يمكنك تغيير كلمة السر من هنا
        st.success("تم التحقق بنجاح! مرحباً بك في لوحة التحليلات.")
        
        df = pd.read_csv(DATA_FILE)
        
        if len(df) == 0:
            st.warning("لا توجد إجابات مسجلة حتى الآن.")
        else:
            # --- METRICS OVERVIEW ---
            col1, col2, col3 = st.columns(3)
            col1.metric("إجمالي الإجابات (Total Responses)", len(df))
            col2.metric("متوسط سهولة الاستخدام", f"{df['Ease_Of_Administration'].mean():.2f} / 5")
            col3.metric("أكثر الشكل تفضيلاً", df['Preferred_Form'].mode()[0] if not df.empty else "N/A")
            
            st.divider()
            
            # --- GRAPHS & VISUALIZATIONS ---
            g_col1, g_col2 = st.columns(2)
            
            with g_col1:
                st.subheader("📊 توزيع الفئات المشاركة")
                fig1 = px.pie(df, names="Category", hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig1, use_container_width=True)
                
                st.subheader("🥣 الشكل المفضل للمكملات")
                fig3 = px.bar(df['Preferred_Form'].value_counts().reset_index(), x='Preferred_Form', y='count',
                              labels={'Preferred_Form': 'الشكل', 'count': 'العدد'}, color_discrete_sequence=['#2E86C1'])
                st.plotly_chart(fig3, use_container_width=True)

            with g_col2:
                st.subheader("⏱️ سرعة ظهور النتائج")
                fig2 = px.bar(df['Visible_Results_Time'].value_counts().reset_index(), x='Visible_Results_Time', y='count',
                              labels={'Visible_Results_Time': 'الفترة', 'count': 'العدد'}, color_discrete_sequence=['#27AE60'])
                st.plotly_chart(fig2, use_container_width=True)
                
                st.subheader("💡 أهم عامل لاختيار المنتج")
                fig4 = px.pie(df, names="Key_Decision_Factor", color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig4, use_container_width=True)

            st.divider()
            
            # --- RAW DATA TABLE & DOWNLOAD ---
            st.subheader("📋 جدول الإجابات الكامل (Raw Data)")
            st.dataframe(df)
            
            # Export to CSV Button
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 تحميل البيانات شيت Excel/CSV",
                data=csv_data,
                file_name="eva_equine_survey_results.csv",
                mime="text/csv"
            )
            
    elif passcode != "":
        st.error("❌ كود المرور غير صحيح. يرجى المحاولة مرة أخرى.")
