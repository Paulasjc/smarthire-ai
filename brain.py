import os
from groq import Groq
from dotenv import load_dotenv

# Cargamos la API KEY desde el archivo .env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_cv_match(jd_text, cv_text):
    """
    Envía el Job Description y el CV a la IA para un análisis técnico.
    """
    
    
    system_prompt = f"""
    Eres un Senior Technical Recruiter experto en Ingeniería de Software.
    Tu tarea es realizar un "screening" técnico comparando una Oferta de Empleo (JD) con un CV.

    PASOS A SEGUIR:
    1. Del JD: Extrae tecnologías clave y años de experiencia mínimos requeridos.
    2. Del CV: Identifica el rol actual. Calcula los años totales de experiencia sumando los periodos de cada empresa.
    3. Mapeo: Relaciona las hard skills del CV con el tiempo de uso de cada una.
    4. Comparación: Contrasta los requisitos del JD con las capacidades del CV.

    REGLAS CRÍTICAS:
    - El "match_percentage" debe ser una evaluación honesta basada en requisitos obligatorios vs habilidades presentes.
    - Si el CV no menciona una tecnología requerida en el JD, inclúyela en "weak_points".
    - No inventes experiencias que no estén escritas.

    Formato JSON esperado:
    {{
      "match_percentage": 0,
      "seniority_level": "Junior/Mid/Senior",
      "experience_summary": {{
          "total_years": 0,
          "relevant_role": "Nombre del puesto"
      }},
      "skills_analysis": {{
          "matched_skills": [],
          "missing_skills": []
      }},
      "strong_points": [],
      "weak_points": [],
      "hiring_recommendation": "Justificación técnica"
    }}
    """
    
    # El USER PROMPT con los datos reales
    user_prompt = f"""
    OFERTA DE EMPLEO (JD):
    {jd_text}
    
    CV DEL CANDIDATO:
    {cv_text}
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            model="llama-3.3-70b-versatile", # Usamos el modelo más potente de Llama 3
            response_format={"type": "json_object"} # Forzamos salida JSON
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en la IA: {e}"


      