from fastapi import FastAPI, HTTPException
import json
from pathlib import Path
from app.filtros import filtro

app = FastAPI()

# Ruta del archivo personas.json
json_file_path = Path("app/data/personas.json")

# Función para leer el archivo personas.json
def read_json(file_name: str = "personas.json"):
    try:
        with open(f'data/{file_name}', 'r', encoding='utf-8') as file:
            data = json.load(file)
            # print(data)
            return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo JSON: {str(e)}")



# Función para escribir en el archivo personas.json
def write_json(data):
    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Endpoint para obtener todas las personas
@app.get("/info")
def get_personas(region: str = None, institucion: str = None, departamento: str = None, id: int = None, nacional: str = None):
    try:
        # data = read_json()
        



        # if departamento is not None and region is not None and institucion is not None:
        #     for nombre, element in data.items():
        #         if (element['departamento'] == departamento and
        #             element['region'] == region and
        #             element['institucion'] == institucion):
        #             resultados[nombre] = element
        
        # elif institucion is not None and region is not None:
        #     departamentos = []
        #     for nombre, element in data.items():
        #         if (element['region'] == region and
        #             element['institucion'] == institucion):
        #             departamentos.append(element['departamento'])
        #     resultados['departamentos'] = list(set(departamentos))  

        # elif region is not None:
        #     instituciones = []
        #     for nombre, element in data.items():
        #         if element['region'] == region:
        #             instituciones.append(element['institucion'])
        #     resultados['instituciones'] = list(set(instituciones))
        # elif id is not None:
        #     for nombre, element in data.items():
        #         if element['_id'] == id:
        #             resultados[nombre] = element
        # else:
        #     regiones = []
        #     for nombre, element in data.items():
                
        #         regiones.append(element['region'])
        #     resultados['regiones'] = list(set(regiones))

        resultados = filtro(region=region, institucion=institucion, departamento=departamento, id=id, nacional=nacional)
        print(resultados)

        if not resultados:
            raise HTTPException(status_code=404, detail="No se encontraron resultados con esos filtros")

        return resultados

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo JSON: {str(e)}")