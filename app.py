import streamlit as st
import json
from utils import extract_text_from_pdf
from brain import analyze_cv_match

# Configuración de la página
st.set_page_config(page_title="SmartHire AI", layout="wide")

st.title("🚀 SmartHire AI: Auditor de Talento")
st.markdown("---")

# Layout de dos columnas
col_input, col_result = st.columns([1, 1.5])

with col_input:
    st.header("📋 Entrada de Datos")
    jd_text = st.text_area("Pega aquí la Descripción del Puesto (JD):", height=200)
    uploaded_file = st.file_uploader("Sube el CV del Candidato (PDF):", type="pdf")
    
    analyze_btn = st.button("Analizar Compatibilidad", type="primary")

if analyze_btn:
    if jd_text and uploaded_file:
        with st.spinner("La IA está analizando la trayectoria..."):
            # 1. Extraer texto del PDF
            cv_text = extract_text_from_pdf(uploaded_file)
            
            # 2. Llamar a la IA
            raw_response = analyze_cv_match(jd_text, cv_text)
            
            # 3. Parsear JSON
            try:
                res = json.loads(raw_response)
                
                with col_result:
                    st.subheader("🎯 Evaluación de Perfil")

                    # Resumen principal
                    with st.container(border=True):
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Match Score", f"{res['match_percentage']}%")
                        m2.metric("Seniority", res['seniority_level'])
                        m3.metric(
                            "Años totales",
                            f"{res['experience_summary'].get('total_years', 0)} yrs",
                        )
                    
                    # Detalle de experiencia
                    st.markdown("### 📄 Resumen de Experiencia")
                    st.markdown(
                        f"**Rol relevante detectado:** {res['experience_summary'].get('relevant_role', 'No detectado')}"
                    )

                    # Análisis de skills (matched vs missing) en formato tabla
                    st.markdown("### 🧠 Análisis de Skills")
                    skills_analysis = res.get("skills_analysis", {}) or {}
                    matched = skills_analysis.get("matched_skills", []) or []
                    missing = skills_analysis.get("missing_skills", []) or []

                    skills_rows = []
                    for skill in matched:
                        skills_rows.append({"Skill": skill, "Estado": "Encaja con el JD"})
                    for skill in missing:
                        skills_rows.append({"Skill": skill, "Estado": "Requerida y ausente"})

                    if skills_rows:
                        st.table(skills_rows)
                    else:
                        st.info("No se ha proporcionado análisis de skills en la respuesta.")

                    # Tabs para organizar la información técnica general
                    tab1, tab2, tab3 = st.tabs(["✅ Fortalezas", "🚩 Carencias", "💡 Recomendación"])
                    
                    with tab1:
                        for point in res['strong_points']:
                            st.markdown(f"🔹 {point}")
                            
                    with tab2:
                        for point in res['weak_points']:
                            st.markdown(f"🔸 {point}")
                            
                    with tab3:
                        st.success(res['hiring_recommendation'])

            except Exception as e:
                st.error(f"Error al procesar la respuesta de la IA: {e}")
                st.text(raw_response) # Para depurar si la IA no devolvió JSON puro
    else:
        st.warning("Por favor, completa ambos campos (JD y CV).")