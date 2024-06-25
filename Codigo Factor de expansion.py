#biblioteca que se utiliza 
import pandas as pd

#variable en la que se encuetra la base de datos de la muestra 
df_fe=pd.read_excel("datos_agrupados_reducido2.xlsx")

#variables que contienen las columnas que se agregaran a la base de datos
nombres_columnas=["t_paid_work","t_domestic_work","t_care_work","t_unpaid_voluntary","t_education","t_leisure","t_personal_care","t_sleep","t_commute","tiempo_total"]
nombres_columnas_fe=["F.E","w","p"]
columnas_fe=pd.DataFrame(columns=nombres_columnas_fe)
df_survey_fe=pd.concat([df_fe,columnas_fe],axis=1)
df_survey_fe[nombres_columnas_fe]=df_survey_fe[nombres_columnas_fe].fillna(1)

#varibles que contienen la cantidad de respuestas de la muestra y la poblacion objetivo
muestra=df_survey_fe.shape[0]
poblacion= 11454405 #dato modificable dependiendo de la poblacion objetivo

#variable que contiene el valor que ira en la columnas w
w=round((poblacion/muestra),3)

#varibles que describen los porcentajes de los grupos de genero y etarios respectivamente (si se trabaja con mas grupos etarios estos valores pueden llegar a variar)
gender1=0.51 
gender2=0.49
anno2=0.32
anno3=0.32
anno4=0.36 

#variables que obtienen los porcentajes que cada grupo representa de la poblacion
porc_g1a2=round(gender1*anno2,3) 
porc_g1a3=round(gender1*anno3,3)
porc_g1a4=round(gender1*anno4,3)
porc_g2a2=round(gender2*anno2,3)
porc_g2a3=round(gender2*anno3,3)
porc_g2a4=round(gender2*anno4,3)

#variables que obtienen la cantidad de respuesta que tiene cada grupo dentro de la muestra
g1a2=((df_survey_fe['gender_id'] == 1) & (df_survey_fe['age_id'] == 2) ).sum()
g1a3=((df_survey_fe['gender_id'] == 1) & (df_survey_fe['age_id'] == 3) ).sum()
g1a4=((df_survey_fe['gender_id'] == 1) & (df_survey_fe['age_id'] == 4) ).sum()
g2a2=((df_survey_fe['gender_id'] == 2) & (df_survey_fe['age_id'] == 2) ).sum()
g2a3=((df_survey_fe['gender_id'] == 2) & (df_survey_fe['age_id'] == 3) ).sum()
g2a4=((df_survey_fe['gender_id'] == 2) & (df_survey_fe['age_id'] == 4) ).sum()

#variables que contienen los valores del ponderador de ajuste de cada grupo
peso_g1a2=round(muestra*(porc_g1a2/g1a2),3)
peso_g1a3=round(muestra*(porc_g1a3/g1a3),3)
peso_g1a4=round(muestra*(porc_g1a4/g1a4),3)
peso_g2a2=round(muestra*(porc_g2a2/g2a2),3)
peso_g2a3=round(muestra*(porc_g2a3/g2a3),3)
peso_g2a4=round(muestra*(porc_g2a4/g2a4),3)

#codigo que reemplaza el valor de la variable w en la columna w
df_survey_fe["w"]=df_survey_fe["w"].replace(1,w)

#codigo que reemplaza el valor de las variables peso_gxax en la columna p en la fila que le corresponde, ademas de calcular el valor que va en la columna F.E
tipo_pesos=[{"gender_id":1,"age_id":2,"nuevo_p":peso_g1a2},{"gender_id":1,"age_id":3,"nuevo_p":peso_g1a3},{"gender_id":1,"age_id":4,"nuevo_p":peso_g1a4},
            {"gender_id":2,"age_id":2,"nuevo_p":peso_g2a2},{"gender_id":2,"age_id":3,"nuevo_p":peso_g2a3},{"gender_id":2,"age_id":4,"nuevo_p":peso_g2a4}]
for condicion in tipo_pesos:
    gender_id=condicion["gender_id"]
    age_id=condicion["age_id"]
    nuevo_p=condicion["nuevo_p"]
    Filtro=(df_survey_fe["gender_id"]==gender_id) & (df_survey_fe["age_id"]==age_id) & (df_survey_fe["p"]==1)
    df_survey_fe.loc[Filtro,"p"]=nuevo_p
df_survey_fe["F.E"]=df_survey_fe["w"]*df_survey_fe["p"]

#codigo que multiplica el valor que esta en la columna F.E por todos las columnas que presentan usos de tiempo de cada fila
for col in nombres_columnas:
    df_survey_fe[col]=(df_survey_fe["F.E"]*df_survey_fe[col])
df_survey_fe[nombres_columnas]=df_survey_fe[nombres_columnas].round(2)

#codigo que guarda los resultados obtenidos tras aplicar el metodo de F.E en un excel
df_survey_fe.to_excel("datos_F.E.xlsx",index=False)
