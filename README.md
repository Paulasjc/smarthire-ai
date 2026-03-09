# SmartHire AI: Auditor de Talento con IA

**SmartHire AI** es una herramienta avanzada de screening técnico que utiliza Inteligencia Artificial (Llama 3 via Groq) para analizar la compatibilidad entre una Oferta de Empleo y el CV de un candidato en formato PDF, relacionado con el sector IT.



##  Características principales
- **Análisis Técnico Profundo:** Extrae habilidades, años de experiencia y seniority real.
- **Match Score Dinámico:** Cálculo inteligente basado en requisitos críticos.
- **Detección de Skill Gap:** Visualiza qué tecnologías tiene el candidato y cuáles le faltan.
- **Interfaz Moderna:** Dashboard interactivo construido con Streamlit.
- **Procesamiento de PDF:** Extracción de texto automática y precisa.

## Stack Tecnológico
- **Frontend:** [Streamlit](https://streamlit.io/)
- **IA/LLM:** [Groq Cloud](https://console.groq.com/) (Modelo: Llama-3.3-70b)
- **Lenguaje:** Python 3.11+
- **Procesamiento de PDF:** PyMuPDF (Fitz)

## Instalación Local

1. **Clona el repositorio:**
   ```bash
   git clone [https://github.com/TU_USUARIO/smarthire-ai.git](https://github.com/TU_USUARIO/smarthire-ai.git)
   cd smarthire-ai
   ```
2. **Crea y activa un entorno virtual:**
   ```bash
   python -m venv venv
    ```
3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   
   ```
4. **Configura variables de entorno:**
     ```bash
    GROQ_API_KEY=tu_api_key_aqui
    ```
6. **Lanza la aplicación:**
   ```bash
   streamlit run app.py
   ```

## ¿Cómo funciona?

La aplicación sigue un flujo de procesamiento estructurado:

1. Ingesta: El usuario sube un PDF y pega el texto de la vacante.

2. Extracción: Se limpia el texto del CV eliminando ruido.

3. Inferencia: La IA mapea las experiencias cronológicamente y detecta las "Hard Skills".

4. Evaluación: Se genera un JSON estructurado con el porcentaje de match y recomendaciones.
