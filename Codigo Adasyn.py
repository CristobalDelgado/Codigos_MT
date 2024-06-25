#bibliotecas que se utilizan 
import pandas as pd
from imblearn.over_sampling import ADASYN

#esta parte agrega la columna clase, le asiga el valor 0 a todas las filas excepto cuanto estas sean de los grupos age_id=2 para gender_id= 1 y 2, en ese caso se cambia por 1
#ademas se rellan con valores 100 algunas celdas de algunas columnas la cuales estaban vacias
df_adasyn=pd.read_excel("datos_agrupados_reducido2.xlsx")
nom_columna=["clase"]
df_2=pd.DataFrame(columns=nom_columna)
df_adasyn2=pd.concat([df_adasyn,df_2],axis=1)
df_adasyn2["clase"]=df_adasyn2["clase"].fillna(0)
df_adasyn2["education_id"]=df_adasyn2["education_id"].fillna(100)
df_adasyn2["version"]=df_adasyn2["version"].fillna(100)
df_adasyn2["salary_id"]=df_adasyn2["salary_id"].fillna(100)
df_adasyn2['clase'] =df_adasyn2.apply(lambda row: 1 if (row['gender_id'] == 1 and row['age_id'] == 2) or (row['gender_id'] == 2 and row['age_id'] == 2) else 0, axis=1)

#esta parte quita de la base de datos las columnas las cuales no contienen valores numericos y que no se vayan a utilizar despues
df_adasyn2.drop(["id","user_id","email","ip_address","created_at","start_datetime","locale","session_id"],axis=1,inplace=True) 

#aqui se guarda la base de datos completa y en otra se guarda solo la columna clase
x_train=df_adasyn2.iloc[:,0:19] 
y_train=df_adasyn2.iloc[:,19] 

#aqui se aplica el meotodo Adasyn y se crea una nueva base de datos con las nuevas respuestas sinteticas
adasyn = ADASYN(random_state=8)
x_train,y_train= adasyn.fit_resample(x_train,y_train) 
df_adasyn3=pd.concat([x_train,y_train],axis=1)

#este codigo es el que se reutilizo del metodo factor de expansion para obtener la distribucion de la muestra
muestra=df_adasyn2.shape[0]
gender1=0.51
gender2=0.49
anno2=0.32
anno3=0.32
anno4=0.36 
porc_g1a2=round(gender1*anno2,3)
porc_g1a3=round(gender1*anno3,3)
porc_g1a4=round(gender1*anno4,3)
porc_g2a2=round(gender2*anno2,3)
porc_g2a3=round(gender2*anno3,3)
porc_g2a4=round(gender2*anno4,3)

#este codigo lo que hace es determinar cuantas respuestas de cada grupo etario y de genero se necesitan para igual la distribucion de la poblacion
resultados=[]
condiciones=[
(df_adasyn3['age_id'] == 2) & (df_adasyn3['gender_id'] == 1),
(df_adasyn3['age_id'] == 3) & (df_adasyn3['gender_id'] == 1),
(df_adasyn3['age_id'] == 4) & (df_adasyn3['gender_id'] == 1),
(df_adasyn3['age_id'] == 2) & (df_adasyn3['gender_id'] == 2),
(df_adasyn3['age_id'] == 3) & (df_adasyn3['gender_id'] == 2),
(df_adasyn3['age_id'] == 4) & (df_adasyn3['gender_id'] == 2)
]
value_g1a2=round(muestra*porc_g1a2)
value_g1a3=round(muestra*porc_g1a3)
value_g1a4=round(muestra*porc_g1a4)
value_g2a2=round(muestra*porc_g2a2)
value_g2a3=round(muestra*porc_g2a3)
value_g2a4=round(muestra*porc_g2a4)
n_values=[value_g1a2,value_g1a3,value_g1a4,value_g2a2,value_g2a3,value_g2a4]

#este codigo lo que hace es aplicar un muestreo aletorio simple para obtener una muestra con la misma distribucion que la poblacion
for i,(condition,n) in enumerate(zip(condiciones,n_values)): 
    df_filtrado=df_adasyn3[condition] 
    try:                                
        random_sample=df_filtrado.sample(n=n,random_state=i)
    except ValueError as e:
        random_sample=df_filtrado.sample(n=n,replace=True,random_state=i)
    resultados.append(random_sample)
final_df = pd.concat(resultados, ignore_index=True)
final_df.to_excel('muestra_adasyn_reducida.xlsx', index=False)
