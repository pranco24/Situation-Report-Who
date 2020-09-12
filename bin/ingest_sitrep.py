import os
import pandas as pd
import csv
import create_directory
import functions
import os.path as path

main_path =  path.abspath(path.join(__file__ ,"../../"))

cases = []
poblacion = []
poblacion_csv = []
paises = []
tasa_mortalidad = []
incidencia = []
cuerpo_csv = []
cases_csv = []
regiones = ['AFRO', 'AMRO', 'EMRO', 'EURO', 'SEARO', 'WPRO', 'Other']
region_oms = []
total_cases_today = []
global_cases = []
global_cases_today = []
global_deaths_today = []
global_deaths = []
globally = []
globally_regions = []
espacios = []
paises_esp = []
continente_esp = []
codigo_esp =[]

################################################################################################################
        #   GENERAMOS UNA FECHA DE EXTRACCIÓN
#################################################################################################################
#Traemos las fechas del directorio create_directory y mandamos a crear el directorio con el archivo
yesterday = create_directory.yesterday
yesterday_format = create_directory.yesterday_format

################################################################################################################
        #   PROPORCIONAMOS LA RUTA CON LA FUENTE DE INFORMACIÓN A ANALIZAR
#################################################################################################################

os.getcwd()
os.chdir(main_path+'/dir/' + yesterday)

file_cases = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
file_sabana = main_path +"/bin/Sabana_Poblacion.csv"
################################################################################################################
        #   CREAMOS LOS DATAFRAME CON PANDAS
#################################################################################################################
#Creamos el dataframe para almacenar la información de la sábana y otro con la información del informe de casos
#Es necesario utilizar UTF-8 para cargar en standard
df_cases = pd.read_csv(file_cases, encoding='utf-8')
df2_countries = pd.read_csv(file_sabana)

################################################################################################################
        #   GUARDAMOS LOS DATAFRAMES EN DOS LISTAS PRINCIPALES
#################################################################################################################
csv_cases = (df_cases.values.tolist())
csv_sabana = (df2_countries.values.tolist())

################################################################################################################
        #   FILTRAMOS AL DÍA QUE SE REQUIERE BUSCAR
#################################################################################################################
#Verificamos la fecha correspondiente al día de ayer y lo comparamos con toda la lista de casos por día.
#Almacenamos toda la infomación referente a los casos reportados diariamente y acumulados
#La finalidad es filtrar y concentrar los datos con los casos únicamente del día buscado
for i in range(len(csv_cases)):
    if csv_cases[i][0] == yesterday_format:
        cases.append(csv_cases[i])

################################################################################################################
        #   EXTRAEMOS EL CSV CON LA SÁBANA PRINCIPAL
#################################################################################################################
#Se almacenan los datos de la sabana principal en listas separadas
for i in range(len(csv_sabana)):
    paises.append(csv_sabana[i][:6])
    poblacion.append(csv_sabana[i][3])
    paises_esp.append(csv_sabana[i][1])  # paises en español
    continente_esp.append(csv_sabana[i][5])
    codigo_esp.append(csv_sabana[i][0])

# Nos aseguramos de que la lista de población de la sabana principal no tenga valores nulos
poblacion_csv = [0 if x != x else x for x in poblacion]


################################################################################################################
        #   EXTRAEMOS Y CONSTRUIMOS UNA LISTA CON LOS ELEMENTOS NECESARIOS PARA CREAR EL CSV DE CASOS DE LA OMS (MAPA)
#################################################################################################################

# Recolectamos y empaquetamos la información en formato tuplas para enviarlos a CSV

for i in range(len(cases)):
    poblacion_csv.append(poblacion_csv[i])
    tasa_mortalidad.append(round((cases[i][7] / poblacion[i]) * 100000, 2))
    espacios.append('')
    incidencia.append(round((cases[i][5] / poblacion[i]) * 100000, 2))

    # Revisamos que las siguientes listas no tengan valores nulos nan
    paises_esp = ['' if x != x else x for x in paises_esp]
    continente_esp = ['' if x != x else x for x in continente_esp]
    codigo_esp = ['NA' if x != x else x for x in codigo_esp]
    tasa_mortalidad = [0 if x != x else x for x in tasa_mortalidad]
    incidencia = [0 if x != x else x for x in incidencia]

    # Empaquetamos en la tupla cuerpo_csv las listas con los valores que componen el CSV
    cuerpo_csv.append(
        [paises[i][1], codigo_esp[i], continente_esp[i], paises[i][4], cases[i][4],
         cases[i][5], incidencia[i], cases[i][6], cases[i][7], tasa_mortalidad[i], espacios[i]])

    # Empaquetamos en la tupla cases_csv los cuatro valores de las listas: Región, incidencias, incidencias acumuladas,
    # defunciones nuevas y acumuladas
    cases_csv.append(
        [paises[i][2], cases[i][4], cases[i][5], cases[i][6], cases[i][7]])


################################################################################################################
        #   EXTRAEMOS Y CONSTRUIMOS UNA LISTA CON LOS ELEMENTOS PARA CREAR EL CSV DE CONTEOS TOTALES  (GLOBAL)
#################################################################################################################

for each in regiones:
    region_oms.append(functions.extraer_globales(cases_csv, each))

#Almacenamos en listas separadas lo que nos devuelve la función
for i in range(len(region_oms)):
    globally_regions.append([regiones[i], region_oms[i][1],region_oms[i][0],region_oms[i][3], region_oms[i][2] ])
    global_cases_today.append(region_oms[i][0])
    global_cases.append(region_oms[i][1])
    global_deaths_today.append(region_oms[i][2])
    global_deaths.append(region_oms[i][3])

#Realiza la operación para obtener el total de todos los casos por región
global_cases_today = (sum(global_cases_today))
global_cases = (sum(global_cases))
global_deaths_today = (sum(global_deaths_today))
global_deaths = (sum(global_deaths))

#Construimos las listas con la información que será almacenada en csv y reporte de HTML
globally.append(["Total", global_cases, global_cases_today, global_deaths, global_deaths_today])

################################################################################################################
            #   ESCRIBIMOS LOS DOCUMENTOS CSV, HTML y JSON; ENVIAMOS A LA FUNCIÓN SUS PARÁMETROS
#################################################################################################################

functions.escribir_mapa(cuerpo_csv, yesterday, create_directory)
functions.escribir_global(yesterday, globally_regions, globally)
functions.to_html(["Reporte al " + create_directory.yesterday_text,len(cases), globally, region_oms])
#functions.create_db(yesterday_format, globally_regions, globally, cuerpo_csv, yesterday, create_directory )

##################################################################################################################
            #   IMPRIMIMOS LA INFORMACIÒN DEL DÌA
#################################################################################################################
print("Reporte al " + create_directory.yesterday_text + " para "+ str(len(cases)) +" paises" )
print("Casos acumulados: ", globally[0][1])
print("Casos reportados en el día de hoy: ", globally[0][2])
print("Defunciones acumuladas: ", globally[0][3])
print("Defunciones nuevas: ", globally[0][4])