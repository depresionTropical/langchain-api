# openai_analysis.py

import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import pandas as pd

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Inicializar el cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_analysis_prompt(competencias: dict) -> str:
    """
    Genera un prompt para enviar a la API de OpenAI basado en las competencias de la persona.
    """
    prompt = "Aquí tienes los datos de competencias de una persona. Realiza un análisis y proporciona una descripción general:\n\n"
    
    # Iterar sobre las competencias para construir el prompt
    for nivel, datos in competencias.items():
        prompt += f"Nivel {nivel.capitalize()}:\n"
        for tipo, items in datos.items():
            prompt += f"  {tipo.capitalize()}:\n"
            for key, value in items.items():
                prompt += f"    {key.capitalize()}: {value}\n"
        prompt += "\n"

    return prompt

def analyze_competencias(competencias: dict) -> str:
    """
    Envía el prompt generado a la API de OpenAI y devuelve el análisis generado.
    """
    try:
        # Generar el prompt basado en las competencias de la persona
        prompt = generate_analysis_prompt(competencias)
        
        # Crear una solicitud de chat con el modelo de OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en análisis psicológico de competencias."},
                {"role": "user", "content": f"{prompt}\n Devuelve una retroalimentación hacia la persona sobre su competencias.La persona va leer su retroalimentación, habla de manera impersonal, refiriendose a esa persona. Sin mencionar explicitamente las competencias, describe cómo es esta persona en términos generales. Primero menciona los aspectos positivos y luego los negativos, sin mencionar directate los aspectos postiivos o negativos. Puedes incluir recomendaciones para mejorar. Usa lenguaje claro. Gracias. Al final agrega si la persona está capacitada para ser tutor de alumnos univesitarios."}
            ],
            max_tokens=300
        )
        
        # Extraer la respuesta generada por el modelo
        response_dict = response.model_dump()
        description = response_dict["choices"][0]["message"]["content"]
        return description
    except Exception as e:
        print(f"Error al realizar el análisis de competencias: {e}")
        return "Ocurrió un error al generar el análisis."
    

async def generate_personal_analysis(competencias: dict) -> str:
  try:
  # Generar el prompt basado en las competencias de la persona
    prompt = generate_analysis_prompt(competencias)

    # Crear una solicitud de chat con el modelo de OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un experto en análisis psicológico de competencias.Y tienes que hacer un análisis personal de la persona."},
            {"role": "user", "content": f"{prompt}\n Devuelve una retroalimentación hacia la persona sobre su competencias.La persona va leer su retroalimentación, habla de manera impersonal, refiriendose a TÚ. Sin mencionar explicitamente las competencias, describe cómo es esta persona en términos generales. Primero menciona los aspectos positivos y luego los negativos, sin mencionar directate los aspectos postiivos o negativos. Puedes incluir recomendaciones para mejorar. Usa lenguaje claro. Gracias. Al final agrega si la persona está capacitada para ser tutor de alumnos univesitarios. Regresa la información en viñetas."}
        ],
        max_tokens=300
    )

    # Extraer la respuesta generada por el modelo
    response_dict = response.model_dump()
    description = response_dict["choices"][0]["message"]["content"]
    return description
  except Exception as e:
    print(f"Error al realizar el análisis de competencias: {e}")
  return "Ocurrió un error al generar el análisis."

async def generate_jefe_analysis(competencias: dict) -> str:
  try:
  # Generar el prompt basado en las competencias de la persona
    prompt = generate_analysis_prompt(competencias)

    # Crear una solicitud de chat con el modelo de OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un experto en análisis psicológico de competencias. Y tienes que devolver un análisis para el jefe sobre los datos de competencias de una persona."},
            {"role": "user", "content": f"{prompt}\n Devuelve una retroalimentación sobre su competencias. Siempre te vas a referir hacia los datos de la persona, como los datos del tutor o maestro. Sin mencionar explicitamente las competencias, describe cómo es esta persona en términos generales. Primero menciona los aspectos positivos y luego los negativos, sin mencionar directate los aspectos postiivos o negativos. Puedes incluir recomendaciones para mejorar. Usa lenguaje claro. Gracias. Al final agrega si la persona está capacitada para ser tutor de alumnos univesitarios."}
        ],
        max_tokens=300
    )

    # Extraer la respuesta generada por el modelo
    response_dict = response.model_dump()
    description = response_dict["choices"][0]["message"]["content"]
    return description
  except Exception as e:
    print(f"Error al realizar el análisis de competencias: {e}")
  return "Ocurrió un error al generar el análisis."

def read_json(file_name: str = "personas.json"):
    try:
        with open(f'data/{file_name}', 'r', encoding='utf-8') as file:
            data = json.load(file)
            # print(data)
            return data
    except Exception as e:
        raise print(f"Error al leer el archivo JSON: {str(e)}")


    