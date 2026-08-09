import streamlit as st
import pandas as pd
import datetime

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="إيفا للعلوم البيطرية - استطلاع المكملات",
    page_icon="🐴",
    layout="centered"
)

# تهيئة قاعدة البيانات في الـ Session State
if "responses" not in st.session_state:
    st.session_state.responses = []

# القائمة الجانبية لتحديد الخيار (تعبئة الاستبيان أو لوحة التحليلات)
st.sidebar.title("إيفا للعلوم البيطرية")
page = st.sidebar.radio("اختر الصفحة:", ["تعبئة الاستبيان (Survey)", "لوحة التحليلات (Surveyor Dashboard)"])

# ==========================================
# 1. صفحة تعبئة الاستبيان
# ==========================================
if page == "تعبئة الاستبيان (Survey)":
    st.title("🐴 إيفا للعلوم البيطرية - استطلاع مكملات الخيول")
    st.write("نشكر وقتك وملاحظاتك لمساعدتنا في تقديم أفضل الحلول لتغذية وصحة الخيول.")
    st.markdown("---")

    # أسئلة تحديد الهوية
    category = st.selectbox(
        "اختر الفئة التي تناسب عملك / نشاطك:",
        ["طبيب بيطري (Veterinarian)", "مربي / صاحب خيل / مدير إصطبل (Owner/Stable Manager)", "تاجر / موزع أعلاف ومكملات (Feed Retailer/Distributor)", "أخرى (Other)"]
    )

    uses_primigo = st.radio(
        "هل تستخدم منتجات Primigo Equine حالياً؟",
        ["نعم", "لا"]
    )

    st.markdown("---")

    # ==========================================
    # 🟢 فرع مستخدمي Primigo (إجابة: نعم)
    # ==========================================
    if uses_primigo == "نعم":
        with st.form("primigo_user_form"):
            primigo_products = st.multiselect(
                "ما هي منتجات Primigo Equine التي تستخدمها؟",
                [
                    "Primigo Joinessence (Joint Support)",
                    "Primigo Flex Equine (Mobility Support)",
                    "Primigo Iron Flex B (Iron & Energy)",
                    "Primigo Hemo Boost (Blood & Oxygen)",
                    "Primigo Mega Boost (Hepatic & Detox)",
                    "Primigo Electro Fuel (Electrolytes & Rehydration)",
                    "Primigo H Care (Hoof Support)",
                    "Primigo Gut Guard (Digestive & Probiotic)",
                    "Primigo E Sel Boost (Antioxidant & Muscle)"
                ]
            )

            ease_score = st.select_slider(
                "ما مدى سهولة إعطاء المكملات للخيل وقبول الخيل لها (Palatability)؟",
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: {1: "صعب جداً (1)", 2: "صعب (2)", 3: "متوسط (3)", 4: "سهل (4)", 5: "سهل جداً وممتاز (5)"}[x]
            )

            preferred_form = st.radio(
                "ما هو الشكل المفضل لديك للمكملات؟",
                ["مكعبات (Pellets)", "سائل (Liquid)", "بودرة (Powder)", "معجون (Oral Paste)"]
            )

            result_speed = st.selectbox(
                "ما هي المدة المتوقعة بالنسبة لك لملاحظة نتائج المكمل الغذائي؟",
                ["خلال 1-2 أسبوع", "خلال 3-4 أسابيع", "أكثر من شهر", "تعتمد على حالة الخيل"]
            )

            perceived_value = st.radio(
                "كيف ترى أسعار مكملات Primigo مقارنة بجودتها والبدائل المستوردة؟",
                ["مناسب جداً ومنافس", "مناسب نوعاً ما", "مرتفع قليلاً", "مرتفع جداً"]
            )

            decision_factor = st.selectbox(
                "ما هو العامل الأهم بالنسبة لك عند اختيار المكمل الغذائي؟",
                ["التركيبة والجودة العلمية", "السعر والوفرة الاقتصادية", "سهولة الاستخدام وقبول الخيل", "توصية البيطريين وسمعة الشركة"]
            )

            feedback = st.text_area("اقتراحات أو ملاحظات إضافية للتطوير (اختياري):")

            submitted_yes = st.form_submit_button("إرسال الاستبيان")

            if submitted_yes:
                response_data = {
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Category": category,
                    "Uses_Primigo": "نعم",
                    "Primigo_Products": ", ".join(primigo_products) if primigo_products else "غير محدد",
                    "Needed_Categories": "N/A",
                    "Preferred_Form": preferred_form,
                    "Decision_Factor": decision_factor,
                    "Ease_Score": ease_score,
                    "Perceived_Value": perceived_value,
                    "Result_Speed": result_speed,
                    "Feedback": feedback if feedback else "لا يوجد"
                }
                st.session_state.responses.append(response_data)
                st.success("تم إرسال إجاباتك بنجاح! شكراً لمشاركتك مع إيفا للعلوم البيطرية.")

    # ==========================================
    # 🔴 فرع غير مستخدمي Primigo (إجابة: لا)
    # ==========================================
    else:
        with st.form("non_user_form"):
            needed_categories = st.multiselect(
                "ما هي أنواع المكملات التي تحتاج وجودها للخيول حالياً؟",
                [
                    "مفاصل وحركة (Joint & Mobility)",
                    "جهاز هضمي ومعدة (Digestive & Gut Health)",
                    "أملاح واستشفاء (Electrolytes & Recovery)",
                    "حوافر وجلد وشعر (Hoof & Coat)",
                    "تهدئة وسلوك (Calming)",
                    "فيتامينات ومعادن عامة (Multivitamins)",
                    "مضادات أكسدة وعضلات (Antioxidants & Muscle)"
                ]
            )

            preferred_form = st.radio(
                "ما هو الشكل المفضل لديك لتناول المكملات؟",
                ["مكعبات (Pellets)", "سائل (Liquid)", "بودرة (Powder)", "معجون (Oral Paste)"]
            )

            decision_factor = st.selectbox(
                "ما هو العامل الأهم بالنسبة لك عند اختيار المكمل الغذائي؟",
                ["التركيبة والجودة العلمية", "السعر والوفرة الاقتصادية", "سهولة الاستخدام وقبول الخيل", "توصية البيطريين وسمعة الشركة"]
            )

            feedback = st.text_area("ما هي أكثر المشاكل التي تواجهها مع المكملات المتاحة في السوق حالياً؟ (اختياري):")

            submitted_no = st.form_submit_button("إرسال الاستبيان")

            if submitted_no:
                response_data = {
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Category": category,
                    "Uses_Primigo": "لا",
                    "Primigo_Products": "N/A",
                    "Needed_Categories": ", ".join(needed_categories) if needed_categories else "غير محدد",
                    "Preferred_Form": preferred_form,
                    "Decision_Factor": decision_factor,
                    "Ease_Score": "N/A",
                    "Perceived_Value": "N/A",
                    "Result_Speed": "N/A",
                    "Feedback": feedback if feedback else "لا يوجد"
                }
                st.session_state.responses.append(response_data)
                st.success("تم إرسال احتياجاتك بنجاح! شكراً لمشاركتك مع إيفا للعلوم البيطرية.")

# ==========================================
# 2. لوحة التحليلات (Surveyor Dashboard)
# ==========================================
else:
    st.title("📊 لوحة تحليلات الاستبيان (خاصة بالشركة)")
    
    passcode = st.text_input("أدخل كود المرور للوصول للنتائج:", type="password")

    if passcode == "eva2026":
        st.success("تم الوصول بنجاح!")

        if len(st.session_state.responses) == 0:
            st.warning("لا توجد إجابات مسجلة حتى الآن.")
        else:
            df = pd.DataFrame(st.session_state.responses)

            df_primigo_users = df[df["Uses_Primigo"] == "نعم"]
            df_non_users = df[df["Uses_Primigo"] == "لا"]

            st.markdown("### 📈 إحصائيات عامة")
            col1, col2, col3 = st.columns(3)
            col1.metric("إجمالي المشاركين", len(df))
            col2.metric("مستخدمي Primigo (نعم)", len(df_primigo_users))
            col3.metric("عملاء محتملين (لا)", len(df_non_users))

            st.markdown("---")

            # شيت 1: مستخدمي Primigo
            st.subheader("1️⃣ شيت مستخدمي Primigo Equine (Yes Users)")
            if len(df_primigo_users) > 0:
                cols_yes = ["Timestamp", "Category", "Primigo_Products", "Ease_Score", "Preferred_Form", "Result_Speed", "Perceived_Value", "Decision_Factor", "Feedback"]
                st.dataframe(df_primigo_users[cols_yes])
                
                # استخدام sep='\t' لتقسيم الأعمدة بشكل ممتاز في إكسيل
                csv_yes = df_primigo_users[cols_yes].to_csv(index=False, sep='\t').encode('utf-16')
                st.download_button(
                    label="📥 تحميل شيت مستخدمي Primigo (Excel/CSV)",
                    data=csv_yes,
                    file_name="Primigo_Current_Users.xls",
                    mime="application/vnd.ms-excel"
                )
            else:
                st.info("لا توجد إجابات من مستخدمي Primigo حتى الآن.")

            st.markdown("---")

            # شيت 2: العملاء المحتملين
            st.subheader("2️⃣ شيت الاحتياجات والعملاء المحتملين (Non-Users Leads)")
            if len(df_non_users) > 0:
                cols_no = ["Timestamp", "Category", "Needed_Categories", "Preferred_Form", "Decision_Factor", "Feedback"]
                st.dataframe(df_non_users[cols_no])

                csv_no = df_non_users[cols_no].to_csv(index=False, sep='\t').encode('utf-16')
                st.download_button(
                    label="📥 تحميل شيت العملاء المحتملين والاحتياجات (Excel/CSV)",
                    data=csv_no,
                    file_name="Primigo_Potential_Leads.xls",
                    mime="application/vnd.ms-excel"
                )
            else:
                st.info("لا توجد إجابات من عملاء غير مستخدمين حتى الآن.")

    elif passcode != "":
        st.error("كود المرور غير صحيح!")
                    
    
