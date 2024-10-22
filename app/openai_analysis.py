import os
import openai
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Inicializar el cliente de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_feedback_from_openai(competencias: dict, output_format: str,reporte:dict) -> str:
    """
    Genera una retroalimentación usando OpenAI basada en las competencias y el formato deseado.
    """
    # Crear el prompt en base al formato
    prompt = f"Aquí tienes los datos de competencias de {reporte['tipo']}. Realiza una retroalimentación en formato {output_format}, usando markdown. {reporte['caracteristica']}. Primero menciona los aspectos positivos y luego los negativos. Por favor, habla de manera impersonal y sin mencionar explícitamente las competencias. Luego, agrega recomendaciones para mejorar."

    # Incluir los puntajes en el prompt
    prompt += "\n\nCompetencias:\n"
    for nivel, items in competencias.items():
        prompt += f"{nivel.capitalize()}:\n"
        for key, value in items.items():
            prompt += f"  {key.capitalize()}: {value}\n"

    # Enviar la solicitud a OpenAI
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en análisis psicológico."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        
        # Extraer la respuesta generada por el modelo
        description = response.choices[0].message.content
        return description

    except Exception as e:
        print(f"Error al generar la retroalimentación: {e}")
        return "Ocurrió un error al generar la retroalimentación."

def generate_multiple_outputs(competencias: dict):
    """
    Genera múltiples salidas de retroalimentación en diferentes formatos (narrativo, bullets, tabla).
    """
    narrativo = generate_feedback_from_openai(competencias, "narrativo")
    bullets = generate_feedback_from_openai(competencias, "bullets")
    tabla = generate_feedback_from_openai(competencias, "tabla")

    return {
        "narrativo": narrativo,
        "bullets": bullets,
        "tabla": tabla
    }

def save_reports_to_md(reports: dict, file_name: str):
    """
    Guarda los reportes generados en un archivo Markdown (.md).
    """
    with open(file_name, 'w') as f:
        f.write("# Reportes de Retroalimentación\n")
        
        f.write("\n## Salida Narrativa\n")
        f.write(reports["narrativo"])
        f.write("\n\n")

        f.write("\n## Salida con Bullets\n")
        f.write(reports["bullets"])
        f.write("\n\n")

        f.write("\n## Salida en Tabla\n")
        f.write(reports["tabla"])
        f.write("\n\n")

if __name__ == "__main__":
    # Datos ficticios de ejemplo
    competencias_basicas = {
        "comunicacion": 85,
        "trabajo_equipo": 78
    }
    
    competencias_intermedias = {
        "liderazgo": 80,
        "planificacion": 75
    }
    
    competencias_avanzadas = {
        "innovacion": 90,
        "resolucion_problemas": 85
    }
    
    personalidad = {
        "empatia": 88,
        "organizacion": 82
    }

    competencias = {
        "competencias_basicas": competencias_basicas,
        "competencias_intermedias": competencias_intermedias,
        "competencias_avanzadas": competencias_avanzadas,
        "personalidad": personalidad
    }
    reporte = {
        'tutor_retro':{
            "tipo": "tutor",
            "caracteristica": "Evalúa su desempeño en las competencias y personal"
        }

    }
    
    # Generar los reportes
    reports = generate_multiple_outputs(competencias)
    
    # Imprimir los resultados
    print("=== Salida Narrativa ===")
    print(reports["narrativo"])
    
    
    print("\n=== Salida con Bullets ===")
    print(reports["bullets"])
    
    print("\n=== Salida en Tabla ===")
    print(reports["tabla"])

     # Guardar los reportes en un archivo Markdown
    save_reports_to_md(reports, "./.data/reporte_tutor.md")
    print("Los reportes han sido guardados en 'reporte_tutor.md'")
