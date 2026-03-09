import streamlit as st
import json
from utils import extract_text_from_pdf
from brain import analyze_cv_match

# Configuración de la página
st.set_page_config(page_title="SmartHire AI", layout="wide")

# Estilos globales para un dashboard más compacto y profesional
st.markdown(
    """
    <style>
    .section-title {
        font-size: 0.95rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #9ca3af;
        margin-bottom: 0.35rem;
    }
    .metric-emphasis {
        font-size: 1.15rem;
        font-weight: 600;
    }
    .metric-small {
        font-size: 0.95rem;
        font-weight: 500;
    }
    .skill-pill {
        display: inline-block;
        padding: 0.18rem 0.55rem;
        border-radius: 999px;
        font-size: 0.8rem;
        margin: 0.12rem 0.25rem 0.12rem 0;
        white-space: nowrap;
    }
    .skill-pill-ok {
        background-color: rgba(22,163,74,0.12);
        color: #22c55e;
        border: 1px solid rgba(34,197,94,0.35);
    }
    .skill-pill-missing {
        background-color: rgba(234,179,8,0.08);
        color: #eab308;
        border: 1px solid rgba(250,204,21,0.35);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Cabecera principal
st.title("SmartHire AI · Auditor de Talento")
st.markdown("---")

# Sidebar: entrada de datos
with st.sidebar:
    st.header("📋 Entrada de Datos")

    jd_text = st.text_area(
        "Pega aquí la Descripción del Puesto:",
        height=220,
    )
    uploaded_file = st.file_uploader(
        "Sube el CV del Candidato (PDF):",
        type="pdf",
    )

    analyze_btn = st.button(
        "Analizar Compatibilidad",
        type="primary",
        use_container_width=True,
    )

# Lógica principal
if analyze_btn:
    if jd_text and uploaded_file:
        with st.spinner("La IA está analizando la trayectoria..."):
            # 1. Extraer texto del PDF
            cv_text = extract_text_from_pdf(uploaded_file)

            # 2. Llamar a la IA
            raw_response = analyze_cv_match(jd_text, cv_text)

            # 3. Parsear JSON y renderizar UI
            try:
                res = json.loads(raw_response)

                match_pct = res.get("match_percentage", 0) or 0
                seniority = res.get("seniority_level", "No detectado")
                experience_summary = res.get("experience_summary", {}) or {}
                total_years = experience_summary.get("total_years", 0) or 0
                relevant_role = experience_summary.get(
                    "relevant_role", "Rol no detectado"
                )

                # -------------------------
                # Hero: Perfil del Candidato
                # -------------------------
                with st.container(border=True):
                    st.markdown("<div class='section-title'>Perfil del candidato</div>", unsafe_allow_html=True)

                    col_role, col_seniority, col_score = st.columns([2, 1, 1])

                    with col_role:
                        st.markdown("Rol relevante", help=None)
                        st.markdown(f"<span class='metric-emphasis'>{relevant_role}</span>", unsafe_allow_html=True)

                    with col_seniority:
                        st.markdown("Seniority detectado")
                        st.markdown(f"<span class='metric-emphasis'>{seniority}</span>", unsafe_allow_html=True)

                    with col_score:
                        st.markdown("Match score")
                        # Barra de progreso visual
                        st.progress(min(max(match_pct / 100, 0), 1))

                        # Color dinámico según el score
                        if match_pct > 80:
                            color = "#16a34a"  # verde
                        elif 40 <= match_pct <= 80:
                            color = "#f97316"  # naranja
                        else:
                            color = "#dc2626"  # rojo

                        st.markdown(
                            f"<span class='metric-emphasis' style='color:{color}; display:block; text-align:center;'>{match_pct}%</span>",
                            unsafe_allow_html=True,
                        )

                    # Celebración para perfiles top
                    if match_pct > 80:
                        st.balloons()

                # -------------------------
                # Resumen de experiencia
                # -------------------------
                with st.container(border=True):
                    st.markdown("<div class='section-title'>Resumen de experiencia</div>", unsafe_allow_html=True)

                    exp_col1, exp_col2 = st.columns(2)
                    with exp_col1:
                        st.markdown("Años totales de experiencia")
                        st.markdown(
                            f"<span class='metric-small'>{total_years} años</span>",
                            unsafe_allow_html=True,
                        )
                    with exp_col2:
                        st.markdown("Rol principal evaluado")
                        st.markdown(
                            f"<span class='metric-small'>{relevant_role}</span>",
                            unsafe_allow_html=True,
                        )

                # -------------------------
                # Mapa de Habilidades (Skills)
                # -------------------------
                with st.container(border=True):
                    st.markdown("<div class='section-title'>Mapa de habilidades</div>", unsafe_allow_html=True)

                    skills_analysis = res.get("skills_analysis", {}) or {}
                    matched_skills = skills_analysis.get("matched_skills", []) or []
                    missing_skills = skills_analysis.get("missing_skills", []) or []

                    col_matched, col_missing = st.columns(2)

                    with col_matched:
                        st.markdown("**Habilidades que encajan**")
                        if matched_skills:
                            ok_html = "".join(
                                f"<span class='skill-pill skill-pill-ok'>{skill}</span>"
                                for skill in matched_skills
                            )
                            st.markdown(ok_html, unsafe_allow_html=True)
                        else:
                            st.caption("Sin habilidades claramente alineadas con el JD.")

                    with col_missing:
                        st.markdown("**Habilidades a reforzar**")
                        if missing_skills:
                            missing_html = "".join(
                                f"<span class='skill-pill skill-pill-missing'>{skill}</span>"
                                for skill in missing_skills
                            )
                            st.markdown(missing_html, unsafe_allow_html=True)
                        else:
                            st.caption("No se han identificado gaps relevantes frente al JD.")

                # -------------------------
                # Tabs: Fortalezas, Carencias, Recomendación
                # -------------------------
                tab1, tab2, tab3 = st.tabs(
                    ["Fortalezas", "Carencias", "Recomendación"]
                )

                with tab1:
                    strong_points = res.get("strong_points", []) or []
                    if strong_points:
                        st.markdown("<div class='section-title'>Fortalezas clave</div>", unsafe_allow_html=True)
                        for point in strong_points:
                            st.markdown(f"- {point}")
                    else:
                        st.caption("La IA no ha destacado fortalezas específicas para este perfil.")

                with tab2:
                    weak_points = res.get("weak_points", []) or []
                    if weak_points:
                        st.markdown("<div class='section-title'>Riesgos y carencias</div>", unsafe_allow_html=True)
                        for point in weak_points:
                            st.markdown(f"- {point}")
                    else:
                        st.caption("No se han detectado carencias relevantes frente al JD.")

                with tab3:
                    hiring_recommendation = res.get(
                        "hiring_recommendation",
                        "La IA no ha proporcionado una recomendación explícita.",
                    )
                    st.markdown("<div class='section-title'>Recomendación de contratación</div>", unsafe_allow_html=True)
                    st.write(hiring_recommendation)

            except Exception as e:
                st.error(f"Error al procesar la respuesta de la IA: {e}")
                st.text(raw_response)  # Para depurar si la IA no devolvió JSON puro
    else:
        st.warning("Por favor, completa ambos campos (JD y CV) en la barra lateral.")