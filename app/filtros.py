
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



reporte='''Lorem ipsum dolor sit amet consectetur adipisicing elit. At quibusdam sunt laudantium, consectetur, quo aut eaque nobis eos voluptatibus saepe ipsam culpa, cumque deleniti soluta? Quasi veniam quos ea dignissimos!
Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laboriosam, similique voluptatem eligendi ullam perferendis officia iste labore modi illo corporis minus placeat accusantium. Voluptatibus consectetur veritatis rem. Facilis, porro nesciunt?
Corporis non mollitia aperiam doloribus nam repellat quam nemo, pariatur sapiente repellendus tempora ab numquam hic eveniet, aut dignissimos quis officiis quas unde, perferendis sint enim! Alias quos ipsa consequatur.
Ab, rem voluptates amet fugiat animi eveniet! Explicabo molestiae ipsa atque blanditiis odit voluptate et dignissimos tenetur, sapiente voluptatibus necessitatibus nesciunt repudiandae libero sint, cum quisquam. Qui voluptate quod temporibus.
Minus reiciendis ipsum consequuntur quod eligendi distinctio impedit laudantium, iste modi, quis ex accusantium sed omnis officiis nisi. Velit temporibus nobis dolorum reiciendis numquam ipsa nisi vero hic ullam molestias!
Praesentium iure iusto odio blanditiis tempore consequuntur ab nam eaque veritatis commodi accusantium placeat odit deserunt beatae quod, alias sit ea ad totam ducimus? Inventore nisi tempore tempora possimus praesentium?
Esse vitae asperiores accusantium officiis et voluptate obcaecati nam corrupti magnam recusandae dolorem, ipsam aut? Enim ratione, reiciendis beatae odio eaque nemo rerum consequuntur doloremque, eos totam, fugiat esse quia.
Error iusto placeat laboriosam nesciunt ab fuga hic possimus quas id quia ex obcaecati quaerat nostrum, amet earum non esse. Laboriosam velit totam voluptas. Facilis qui quos libero maiores dolores.
Vitae iste amet quasi odio voluptatibus quod reprehenderit nostrum non rerum officia exercitationem, sunt, similique ullam recusandae veritatis deleniti a eligendi magni corporis necessitatibus, fugiat sed est cum! Vero, sed?
Ad magni temporibus voluptatem eveniet similique qui tempore neque fuga, inventore alias, asperiores adipisci ullam quos? Quae recusandae distinctio esse porro corporis? Repudiandae, voluptate maiores. Beatae molestias ab libero ea.
Aliquam debitis, inventore voluptatibus quasi doloribus sed, illo nisi tenetur amet magni totam ut ipsum sint? Maxime eum voluptatibus sapiente officiis quae necessitatibus, aliquid architecto placeat recusandae iste dolore quas.
Iusto similique esse veritatis soluta aspernatur nihil rerum dolore provident hic aliquam ex dolorum, recusandae explicabo eveniet, eligendi voluptatibus ut eaque repellat amet iste assumenda cumque dicta deleniti. Libero, expedita?
Laboriosam, enim atque unde quas, corrupti molestias iusto ducimus voluptate illo deleniti laborum beatae rerum. Velit itaque ad illo adipisci distinctio dolor nemo! Commodi reprehenderit voluptas accusantium iure? Non, iste.
Sapiente sint eligendi facilis, ut vitae quos explicabo obcaecati? Minus qui illum at doloribus culpa, ipsum animi magnam soluta nemo laborum voluptatibus quis cumque et amet suscipit, distinctio harum maiores!
'''


def filtro(region=None, institucion=None, departamento = None, nacional= None, id:int = None)->pd.DataFrame:
  df_agrupado_mean, df= json_to_df()

  if departamento is not None and region is not None and institucion is not None:
    df_filtrado = df_agrupado_mean[
    (df_agrupado_mean['region'] == region) &
    (df_agrupado_mean['institucion'] == institucion) &
    (df_agrupado_mean['departamento'] == departamento)
    ].drop(columns=['region', 'institucion','departamento']).reset_index(drop=True).mean().round(1)
    df_filtrado = df_filtrado.to_frame().T


    _id = df[
    (df['region'] == region) &
    (df['institucion'] == institucion) &
    (df['departamento'] == departamento)]._id.to_list()
    personas = df[df['_id'].isin(_id)].nombre.to_list()

    _id = [[k,v] for k,v in zip(_id,personas)]
    df_filtrado.loc[:,'id'] = [_id]
    # df_filtrado.loc[:,'personas'] = [personas]
    df_filtrado.loc[0, 'reporte'] = reporte
    df_filtrado.insert(0,'reporte',df_filtrado.pop('reporte'))
    # df_filtrado.insert(0,'personas',df_filtrado.pop('personas'))
    df_filtrado.insert(0,'id',df_filtrado.pop('id'))
    
    
    
  elif institucion is not None and region is not None:
    df_filtrado = df_agrupado_mean[
    (df_agrupado_mean['region'] == region) &
    (df_agrupado_mean['institucion'] == institucion)
    ].drop(columns=['region', 'institucion','departamento']).reset_index(drop=True).mean().round(1)

    df_filtrado = df_filtrado.to_frame().T

    departamento = df_agrupado_mean[
    (df_agrupado_mean['region'] == region) &
    (df_agrupado_mean['institucion'] == institucion)
    ].departamento.unique()


    df_filtrado.loc[0, 'departamento'] = departamento
    df_filtrado.loc[0, 'reporte'] = reporte
    df_filtrado.insert(0,'reporte',df_filtrado.pop('reporte'))
    df_filtrado.insert(0,'departamento',df_filtrado.pop('departamento'))
    

  elif region is not None:
    df_filtrado = df_agrupado_mean[
    (df_agrupado_mean['region'] == region)
    ].drop(columns=['region','departamento','institucion']).reset_index(drop=True).mean().round(1)

    df_filtrado = df_filtrado.to_frame().T

    institucion = df_agrupado_mean[
    (df_agrupado_mean['region'] == region)
    ].institucion.unique()  

    df_filtrado.loc[0, 'institucion'] = institucion
    df_filtrado.loc[0, 'reporte'] = reporte
    df_filtrado.insert(0,'reporte',df_filtrado.pop('reporte'))
    df_filtrado.insert(0,'institucion',df_filtrado.pop('institucion'))
  elif nacional =='Nacional':
    df_filtrado = df_agrupado_mean.groupby('region').mean(numeric_only=True).reset_index().round(1)
    df_filtrado = df_filtrado.mean(numeric_only=True).round(1)
    df_filtrado = df_filtrado.to_frame().T

    region = df_agrupado_mean.region.unique()
    df_filtrado.loc[0, 'region'] = region
    df_filtrado.loc[0, 'reporte'] = reporte

    df_filtrado.insert(0,'reporte',df_filtrado.pop('reporte'))
    df_filtrado.insert(0,'region',df_filtrado.pop('region'))
    
  elif id is not None:
    df['reporte'] = reporte
    df_filtrado= df[df['_id']==id].drop(columns=['_id'])
    df_filtrado.insert(0,'reporte',df_filtrado.pop('reporte'))
    df_filtrado.insert(0,'nombre',df_filtrado.pop('nombre'))
    
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
  df_con_filtro =filtro(nacional='Nacional')
  print(df_con_filtro)

