
import json
import pandas as pd
import numpy as np



# def read_json(file_name: str = "personas copy.json"):
#     try:
#         with open(f'{file_name}', 'r', encoding='utf-8') as file:
#             data = json.load(file)
#             # print(data)
#             return data
#     except Exception as e:
#         print(f"Error: {e}")


# data = read_json()

# data.items()

global df_agrupado_mean
global df

def json_to_df():

  # Leer el archivo JSON
  with open('./app/data/personas.json', 'r', encoding='utf-8') as f:
      data = json.load(f)


  # Convertir el JSON a un DataFrame, desanidando cada "Persona"
  personas = []

  for key, value in data.items():
      # Aplanar el contenido de cada persona y agregar el nombre de la persona como una columna
      persona = pd.json_normalize(value, sep='_')
      persona['nombre'] = key  # Añadir el nombre de la persona como columna
      personas.append(persona)

  # Concatenar todas las filas en un único DataFrame
  df = pd.concat(personas, ignore_index=True)





  df


  # Seleccionar las columnas necesarias para la agrupación y competencias
  columnas_competencias = [col for col in df.columns if 'basicas' in col or 'intermedias' in col or 'avanzadas' in col or 'personalidad'in col]
  columnas_agrupacion = ['region', 'institucion', 'departamento']

  # Crear un DataFrame con las columnas necesarias
  df_competencias = df[columnas_agrupacion + columnas_competencias]



  # Agrupar por región, institución y departamento, y calcular el promedio de las competencias
  df_agrupado_mean = df_competencias.groupby(['region', 'institucion', 'departamento']).mean().reset_index().round(1)

  # Mostrar el DataFrame resultante
  return df_agrupado_mean, df


# # Filtros
# region = 'Sur'
# institucion = 'Institución 3'
# departamento = 'Civil'

# # Filtrar el DataFrame directamente
# df_filtrado = df_agrupado_mean[
#     (df_agrupado_mean['region'] == region) &
#     (df_agrupado_mean['institucion'] == institucion) &
#     (df_agrupado_mean['departamento'] == departamento)
# ].reset_index(drop=True)
# df_filtrado


def eliminar_clave_vacia(lista):
    for registro in lista:
        if "" in registro:  # Si la clave vacía está presente
            del registro[""]  # Eliminar la clave vacía
    return lista


def transformar_registros(filtro_region: pd.DataFrame) -> list:
    # Lista para almacenar los registros transformados
    registros = []

    # Iterar sobre cada fila del DataFrame
    for _, fila in filtro_region.iterrows():
        # Inicializamos un diccionario vacío para cada registro
        registro_transformado = {}

        # Recorremos cada columna (clave) y valor de la fila actual
        for key, value in fila.items():
            # Convertir arrays de numpy a listas nativas
            if isinstance(value, np.ndarray):
                value = value.tolist()
            
            # Si la clave contiene guiones bajos, vamos a dividirla para crear la estructura anidada
            if "_" in key:
                partes = key.split("_")  # Dividimos por guiones bajos
                subdic = registro_transformado  # Referencia al diccionario del registro
                
                # Iteramos sobre las partes (excepto la última) para crear niveles de anidación
                for parte in partes[:-1]:
                    if parte not in subdic:
                        subdic[parte] = {}
                    subdic = subdic[parte]
                
                # Asignamos el valor a la última parte de la clave
                subdic[partes[-1]] = round(value) if isinstance(value, (int, float)) else value  # Redondeamos el valor si es numérico
            else:
                # Si no tiene guiones bajos, lo asignamos directamente en el nivel superior
                registro_transformado[key] = value

        # Añadimos el registro transformado a la lista de registros
        registros.append(registro_transformado)

    return eliminar_clave_vacia(registros)



reporte='''Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quaerat quia adipisci laboriosam tenetur sed animi omnis tempora quas totam officia ipsam neque delectus, numquam ratione est dolorum amet facere accusamus.
Quibusdam, tempora harum dolores ipsa quos inventore, aliquam consequatur cum ab tempore consectetur voluptatibus aperiam nemo. Rem labore quis reiciendis iusto maxime, animi ad obcaecati provident possimus sed laboriosam placeat.
Necessitatibus nobis sunt odit quaerat fugiat. Debitis deleniti vel quasi. Iste, deserunt? Itaque odio sequi vel quod eum est? Assumenda odio ut voluptate qui quos illo est porro officiis sit!
Quo error rem quasi distinctio reiciendis officiis dolores vel voluptates, nisi est. Quod, velit. Unde esse saepe vitae eum soluta atque quaerat officiis, tenetur assumenda placeat odio architecto amet consequatur?
'''


def filtro(region=None, institucion=None, departamento=None, nacional=None, id: int = None) -> pd.DataFrame:
  # Convert JSON data to DataFrame
  df_agrupado_mean, df = json_to_df()

  # Filter by region, institution, and department
  if departamento is not None and region is not None and institucion is not None:
    df_filtrado = df_agrupado_mean[
      (df_agrupado_mean['region'] == region) &
      (df_agrupado_mean['institucion'] == institucion) &
      (df_agrupado_mean['departamento'] == departamento)
    ].drop(columns=['region', 'institucion', 'departamento']).reset_index(drop=True).mean().round(1)
    df_filtrado = df_filtrado.to_frame().T

    # Get IDs and names of people in the filtered group
    _id = df[
      (df['region'] == region) &
      (df['institucion'] == institucion) &
      (df['departamento'] == departamento)
    ]._id.to_list()
    personas = df[df['_id'].isin(_id)].nombre.to_list()

    # Combine IDs and names into a list of tuples
    _id = [[k, v] for k, v in zip(_id, personas)]
    df_filtrado.loc[:, 'id'] = [_id]
    df_filtrado.loc[0, 'reporte_A'] = reporte
    df_filtrado.loc[0, 'reporte_2'] = reporte
    df_filtrado.loc[0, 'reporte_3'] = reporte
    df_filtrado.insert(0, 'reporte_3', df_filtrado.pop('reporte_3'))
    df_filtrado.insert(0, 'reporte_2', df_filtrado.pop('reporte_2'))
    df_filtrado.insert(0, 'reporte_A', df_filtrado.pop('reporte_A'))
    df_filtrado.insert(0, 'id', df_filtrado.pop('id'))

  # Filter by region and institution
  elif institucion is not None and region is not None:
    df_filtrado = df_agrupado_mean[
      (df_agrupado_mean['region'] == region) &
      (df_agrupado_mean['institucion'] == institucion)
    ].drop(columns=['region', 'institucion', 'departamento']).reset_index(drop=True).mean().round(1)
    df_filtrado = df_filtrado.to_frame().T

    # Get unique departments in the filtered group
    departamento = df_agrupado_mean[
      (df_agrupado_mean['region'] == region) &
      (df_agrupado_mean['institucion'] == institucion)
    ].departamento.unique()

    df_filtrado.loc[0, 'departamento'] = departamento
    df_filtrado.loc[0, 'reporte_A'] = reporte
    df_filtrado.loc[0, 'reporte_B'] = reporte
    df_filtrado.loc[0, 'reporte_C'] = reporte
    df_filtrado.insert(0, 'reporte_C', df_filtrado.pop('reporte_C'))
    df_filtrado.insert(0, 'reporte_B', df_filtrado.pop('reporte_B'))
    df_filtrado.insert(0, 'reporte_A', df_filtrado.pop('reporte_A'))
    df_filtrado.insert(0, 'departamento', df_filtrado.pop('departamento'))

  # Filter by region
  elif region is not None:
    df_filtrado = df_agrupado_mean[
      (df_agrupado_mean['region'] == region)
    ].drop(columns=['region', 'departamento', 'institucion']).reset_index(drop=True).mean().round(1)
    df_filtrado = df_filtrado.to_frame().T

    # Get unique institutions in the filtered group
    institucion = df_agrupado_mean[
      (df_agrupado_mean['region'] == region)
    ].institucion.unique()

    df_filtrado.loc[0, 'institucion'] = institucion
    df_filtrado.loc[0, 'reporte_A'] = reporte
    df_filtrado.loc[0, 'reporte_B'] = reporte
    df_filtrado.loc[0, 'reporte_C'] = reporte
    df_filtrado.insert(0, 'reporte_C', df_filtrado.pop('reporte_C'))
    df_filtrado.insert(0, 'reporte_B', df_filtrado.pop('reporte_B'))
    df_filtrado.insert(0, 'reporte_A', df_filtrado.pop('reporte_A'))
    df_filtrado.insert(0, 'institucion', df_filtrado.pop('institucion'))

  # Filter for national level
  elif nacional == 'Nacional':
    df_filtrado = df_agrupado_mean.groupby('region').mean(numeric_only=True).reset_index().round(1)
    df_filtrado = df_filtrado.mean(numeric_only=True).round(1)
    df_filtrado = df_filtrado.to_frame().T

    # Get unique regions
    region = df_agrupado_mean.region.unique()
    df_filtrado.loc[0, 'region'] = region
    df_filtrado.loc[0, 'reporte_A'] = reporte
    df_filtrado.loc[0, 'reporte_B'] = reporte
    df_filtrado.loc[0, 'reporte_C'] = reporte
    df_filtrado.insert(0, 'reporte_C', df_filtrado.pop('reporte_C'))
    df_filtrado.insert(0, 'reporte_B', df_filtrado.pop('reporte_B'))
    df_filtrado.insert(0, 'reporte_A', df_filtrado.pop('reporte_A'))
    df_filtrado.insert(0, 'region', df_filtrado.pop('region'))

  # Filter by ID
  elif id is not None:
    
    df_filtrado = df[df['_id'] == id].drop(columns=['_id'])
    df_filtrado.reset_index(drop=True, inplace=True)
    df_filtrado.loc[0, 'retroalimentacion_A'] = reporte
    df_filtrado.loc[0, 'retroalimentacion_B'] = reporte
    df_filtrado.loc[0, 'retroalimentacion_C'] = reporte
    df_filtrado.insert(0, 'retroalimentacion_C', df_filtrado.pop('retroalimentacion_C'))
    df_filtrado.insert(0, 'retroalimentacion_B', df_filtrado.pop('retroalimentacion_B'))
    df_filtrado.insert(0, 'retroalimentacion_A', df_filtrado.pop('retroalimentacion_A'))

    df_filtrado.loc[0, 'reporte_A'] = reporte
    df_filtrado.loc[0, 'reporte_B'] = reporte
    df_filtrado.loc[0, 'reporte_C'] = reporte
    df_filtrado.insert(0, 'reporte_C', df_filtrado.pop('reporte_C'))
    df_filtrado.insert(0, 'reporte_B', df_filtrado.pop('reporte_B'))
    df_filtrado.insert(0, 'reporte_A', df_filtrado.pop('reporte_A'))
    
    df_filtrado.insert(0, 'nombre', df_filtrado.pop('nombre'))

  # Transform the filtered DataFrame into a list of dictionaries
    
  return transformar_registros(df_filtrado) 


df_con_filtro =filtro(
  id=1
)
df_con_filtro

# 
# filtro=filtro(
 
#   institucion='Institución 1'
# )
# filtro

# # 
# # def guardar_json(data, file_name: str = "resultados.json"):
# #     with open('registros.json', 'w', encoding='utf-8') as archivo_json:
# #         json.dump(data, archivo_json, ensure_ascii=False, indent=4)

# #     print("El archivo JSON se ha guardado correctamente.")


# guardar_json(filtro)



if __name__ =='__main__':
  df_con_filtro =filtro(id=3)
  print(df_con_filtro)

