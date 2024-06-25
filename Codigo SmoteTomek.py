#bibliotecas que se utilizan 
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import TomekLinks
from imblearn.combine import SMOTETomek

#esta parte agrega la columna clase, le asiga el valor 0 a todas las filas excepto cuanto estas sean de los grupos age_id=2 para gender_id= 1 y 2, en ese caso se cambia por 1
#ademas se rellan con valores 100 algunas celdas de algunas columnas la cuales estaban vacias
df_smote=pd.read_excel("datos_agrupados_reducido2.xlsx")
nom_columna=["clase"]
df_2=pd.DataFrame(columns=nom_columna)
df_smote2=pd.concat([df_smote,df_2],axis=1)
df_smote2["clase"]=df_smote2["clase"].fillna(0)
df_smote2["education_id"]=df_smote2["education_id"].fillna(100)
df_smote2["version"]=df_smote2["version"].fillna(100)
df_smote2["salary_id"]=df_smote2["salary_id"].fillna(100)
df_smote2['clase'] =df_smote2.apply(lambda row: 1 if (row['gender_id'] == 1 and row['age_id'] == 2) or (row['gender_id'] == 2 and row['age_id'] == 2) else 0, axis=1)

#esta parte quita de la base de datos las columnas las cuales no contienen valores numericos y que no se vayan a utilizar despues
df_smote2.drop(["id","user_id","email","ip_address","created_at","start_datetime","locale","session_id"],axis=1,inplace=True) #esto saca del df las columnas que no vaya a utilizar

#aqui se guarda la base de datos completa y en otra se guarda solo la columna clase
x_train=df_smote2.iloc[:,0:19] #estas son todas las columnas
y_train=df_smote2.iloc[:,19] #esta solo selecciona la ultima columna, la cual es la que muestra que los datos estan desbalanceados 

#aqui se aplica el meotodo SmoteTomke y se crea una nueva base de datos con las nuevas respuestas sinteticas y las que se eliminaron
hibrido=SMOTETomek(tomek=TomekLinks(sampling_strategy="not minority"),smote=SMOTE(sampling_strategy=1,k_neighbors=4))
x_train,y_train=hibrido.fit_resample(x_train,y_train) #esto es lo que hace el remuestreo
df_smote3=pd.concat([x_train,y_train],axis=1)

#este codigo es el que se reutilizo del metodo factor de expansion para obtener la distribucion de la muestra
muestra=df_smote2.shape[0]
gender1=0.51 #los valores de aqui hasta el siguiente comentario son fijos y dependen del rango de edad que se utilice
gender2=0.49#estos valores son el % de la poblacion que da el censo
anno2=0.32
anno3=0.32
anno4=0.36 #hasta aqui son fijos
porc_g1a2=round(gender1*anno2,3) #estos valores son la proporcion que debiese haber de cada tipo de caracteristica
porc_g1a3=round(gender1*anno3,3)
porc_g1a4=round(gender1*anno4,3)
porc_g2a2=round(gender2*anno2,3)
porc_g2a3=round(gender2*anno3,3)
porc_g2a4=round(gender2*anno4,3)

#este codigo lo que hace es determinar cuantas respuestas de cada grupo etario y de genero se necesitan para igual la distribucion de la poblacion
resultados=[]
condiciones=[
(df_smote3['age_id'] == 2) & (df_smote3['gender_id'] == 1), #este parte lo que hace es poner todas las condiciones que hay en la muestra es decir edad y genero
(df_smote3['age_id'] == 3) & (df_smote3['gender_id'] == 1),
(df_smote3['age_id'] == 4) & (df_smote3['gender_id'] == 1),
(df_smote3['age_id'] == 2) & (df_smote3['gender_id'] == 2),
(df_smote3['age_id'] == 3) & (df_smote3['gender_id'] == 2),
(df_smote3['age_id'] == 4) & (df_smote3['gender_id'] == 2)
]
value_g1a2=round(muestra*porc_g1a2) #esta parte lo que hace es decir cuantas personas de cada condicion debe haber en la muestra final
value_g1a3=round(muestra*porc_g1a3)
value_g1a4=round(muestra*porc_g1a4)
value_g2a2=round(muestra*porc_g2a2)
value_g2a3=round(muestra*porc_g2a3)
value_g2a4=round(muestra*porc_g2a4)
n_values=[value_g1a2,value_g1a3,value_g1a4,value_g2a2,value_g2a3,value_g2a4] #aqui se dejan todos estos valores en una lista

#este codigo lo que hace es aplicar un muestreo aletorio simple para obtener una muestra con la misma distribucion que la poblacion
for i,(condition,n) in enumerate(zip(condiciones,n_values)): #esto lo que hace seleccionar del data frame con el remuestreo el numero de filas que se obtuvo un poco mas arriba correspondiente
    df_filtrado=df_smote3[condition] # a cada condicion para que el data frame final tenga la misma distribucion de la poblacion para poder comparar
    try:                                #la parte de try toma de manera aleatoria la cantidad n que se calculo siempre que esta en el df de remuestreo esten todas las filas necesarias
        random_sample=df_filtrado.sample(n=n,random_state=i)
    except ValueError as e:             #el except lo que hace es que cuando no hay la cantidad de filas requeridad se duplican algunas para lograr la distribucion
        random_sample=df_filtrado.sample(n=n,replace=True,random_state=i)
    resultados.append(random_sample)
final_df = pd.concat(resultados, ignore_index=True)
final_df.to_excel('muestra_smotetomek_reducida.xlsx', index=False)