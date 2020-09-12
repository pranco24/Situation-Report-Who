import csv,json
from pymongo import MongoClient

def extraer_globales(list,reg):
    #List tiene la tupla y reg el registro del continente actual (7 en total)
    casos_hoy = []
    casos_acumulados = []
    defunciones_hoy = []
    defunciones_acumuladas = []

    for i in range(len(list)):
        if (list[i][0]) == reg:
            (casos_hoy.append(list[i][1]))
            casos_acumulados.append(list[i][2])
            defunciones_hoy.append(list[i][3])
            defunciones_acumuladas.append(list[i][4])
    sum_cases = (sum(casos_hoy), sum(casos_acumulados), sum(defunciones_hoy), sum(defunciones_acumuladas))
    return sum_cases

def escribir_mapa (cuerpo_csv,yesterday,create_directory):

    with open(yesterday + " Mapa.csv", "w", newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Pais español", "Código", "Continente", "Clave", "Casos incidentes del día por país (Día actual)",
             "Casos acumulados al día por país", "Inicidencia acumulada por cien mil habitantes",
             "Defunciones incidentes al día por país (día actual)", "Defunciones acumuladas al día por país",
             "Tasa de Mortalidad por cien mil habitantes", "Label de corte"])

        writer.writerows(cuerpo_csv)
        f.close()

    #### Ordenamos y quitamos el registro otros ####
    # Abrimos nuevamente el documento CSV y cargamos en lista para añadir el registro de la marca o label de corte
    f = open(yesterday + ' Mapa.csv', 'r', encoding='utf-8')
    reader = csv.reader(f)
    mylist = list(reader)
    f.close()

    # Recuperamos en dos listas
    # La lista indice sirve para recuperar el primer registro que contiene la información de la cabecera
    index_csv = (mylist[0])
    # La segunda lista realiza un ordenamiento de todos los datos a partir de la posición 0 con el código de país (1)
    # excepto la cabecera (0) que retiramos
    mylist = (sorted(mylist[1:], key=lambda x: x[1]))

    # Se añade el label de corte a la lista, se reconstruye el CSV
    mylist[1][
        10] = 'Fuente: Reportes de situación de la Organización Mundial de la Salud. Corte al ' + create_directory.yesterday_text
    my_new_list = open(yesterday + ' Mapa.csv', 'w', newline='')
    csv_writer = csv.writer(my_new_list)

    # Escribimos el indice con la cabecera
    csv_writer.writerow(index_csv)

    # Escribimos la lista excepto el primer registro que contiene el registro de "otros"
    csv_writer.writerows(mylist[1:])
    # Cerramos el documento
    my_new_list.close()

def escribir_global (yesterday, globally_regions, globally):
    with open(yesterday + " Global.csv", "w+", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Región OMS", "Casos acumulados", "Casos reportados al dia de hoy", "Defunciones acumuladas",
                         "Defunciones nuevas"])
        writer.writerows(globally_regions)
        writer.writerows(globally)


def send_email (date, document1, document2):
    print(date)

def to_html(report):

    html = """<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>WHO Situation Reports</title>
    <meta name="description" content="Reporte del día de la OMS.">
    <link rel="stylesheet" href="main.css">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">

</head>

<style>
    html {
        background: #e6e9e9;
        background-image: linear-gradient(270deg, rgb(230, 233, 233) 0%, rgb(216, 221, 221) 100%);
        -webkit-font-smoothing: antialiased;
    }

    body {
        background: #fff;
        box-shadow: 0 0 2px rgba(0, 0, 0, 0.06);
        color: #545454;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-size: 12px;
        line-height: 1.5;
        margin: 0 auto;
        max-width: 800px;
        padding: 2em 2em 4em;
    }

    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    td{
        color: #222;
        font-weight: 600;
        line-height: 1.3;
    }

    h2 {
        margin-top: 1.3em;
    }

    a {
        color: #0083e8;
    }

    b,
    strong {
        font-weight: 600;
    }

    samp {
        display: none;
    }

    img {
        animation: colorize 2s cubic-bezier(0, 0, .78, .36) 1;
        background: transparent;
        border: 10px solid rgba(0, 0, 0, 0.12);
        border-radius: 4px;
        display: block;
        margin: 1.3em auto;
        max-width: 95%;
    }

    @keyframes colorize {
        0% {
            -webkit-filter: grayscale(100%);
            filter: grayscale(100%);
        }

        100% {
            -webkit-filter: grayscale(0%);
            filter: grayscale(0%);
        }
    }

</style>

<body>

    <h5>"""+report[0]+"""</h5>
    <h6>Al día de hoy se ha reportado en """+str(report[1])+""" paises: </h6>
    

    <table class="table">
        <thead class="thead-dark">
            <tr>
                <th>Continente</th>
                <th>Casos acumulados</th>
                <th>Casos reportados al día de hoy</th>
                <th>Defunciones acumuladas</th>
                <th>Defunciones nuevas al día de hoy</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <th scope="row">África</th>
                <td>"""+str(report[3][0][1])+"""</td>
                <td>"""+str(report[3][0][0])+"""</td>
                <td>"""+str(report[3][0][3])+"""</td>
                <td>"""+str(report[3][0][2])+"""</td>
            </tr>
            <tr>
                <th scope="row">América</th>
                <td>"""+str(report[3][1][1])+"""</td>
                <td>"""+str(report[3][1][0])+"""</td>
                <td>"""+str(report[3][1][3])+"""</td>
                <td>"""+str(report[3][1][2])+"""</td>
            </tr>

             <tr>
                <th scope="row">EMRO</th>
                <td>"""+str(report[3][2][1])+"""</td>
                <td>"""+str(report[3][2][0])+"""</td>
                <td>"""+str(report[3][2][3])+"""</td>
                <td>"""+str(report[3][2][2])+"""</td>
            </tr>

             <tr>
                <th scope="row">EURO</th>
                <td>"""+str(report[3][3][1])+"""</td>
                <td>"""+str(report[3][3][0])+"""</td>
                <td>"""+str(report[3][3][3])+"""</td>
                <td>"""+str(report[3][3][2])+"""</td>
            </tr>
             <tr>
                <th scope="row">SEARO</th>
                <td>"""+str(report[3][4][1])+"""</td>
                <td>"""+str(report[3][4][0])+"""</td>
                <td>"""+str(report[3][4][3])+"""</td>
                <td>"""+str(report[3][4][2])+"""</td>
            </tr>

             <tr>
                <th scope="row">WPRO</th>
                <td>"""+str(report[3][5][1])+"""</td>
                <td>"""+str(report[3][5][0])+"""</td>
                <td>"""+str(report[3][5][3])+"""</td>
                <td>"""+str(report[3][5][2])+"""</td>
            </tr>

            <tr>
                <th scope="row">Otro</th>
                <td>"""+str(report[3][6][1])+"""</td>
                <td>"""+str(report[3][6][0])+"""</td>
                <td>"""+str(report[3][6][3])+"""</td>
                <td>"""+str(report[3][6][2])+"""</td>
            </tr>
            <tr>
                <th scope="row ">TOTAL</th>
                <td>"""+str(report[2][0][1])+"""</td>
                <td>"""+str(report[2][0][2])+"""</td>
                <td>"""+str(report[2][0][3])+"""</td>
                <td>"""+str(report[2][0][4])+"""</td>
            </tr>


        </tbody>
    </table>

    <p>
        
    </p>


    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
</body>

</html>
"""

    with open("Log.html", "w", encoding='utf-8') as file:
        file.write(html)


def create_db (yesterday_format,globally_regions,globally, cuerpo_csv, yesterday, create_directory):

    data = {}
    data['fecha'] = yesterday_format
    data['global'] = []
    data['total'] = []
    data['paises'] = []

    for i in range (len(globally_regions)):
        data['global'].append({
            'Región OMS': globally_regions[i][0],
            'Casos acumulados': (globally_regions[i][1]),
            'Casos reportados hoy': (globally_regions[i][2]),
            'Defunciones acumuladas': (globally_regions[i][3]),
            'Defunciones hoy': (globally_regions[i][4])
        })
    data['total'].append({
        'Total Casos acumulados': (globally[0][1]),
        'Total Casos reportados hoy': (globally[0][2]),
        'Total Defunciones acumuladas': (globally[0][3]),
        'Total Defunciones hoy': (globally[0][4])

        })
    for i in range (len(cuerpo_csv)):
        data['paises'].append({
            'pais': cuerpo_csv[i][0],
            'codigo': cuerpo_csv[i][1],
            'continente': cuerpo_csv[i][2],
            'clave': cuerpo_csv[i][3],
            'Casos incidentes del día por país (Día actual)' : cuerpo_csv[i][4],
            'Casos acumulados al día por país': cuerpo_csv[i][5],
            'Inicidencia acumulada por cien mil habitantes': cuerpo_csv[i][6],
            'Defunciones incidentes al día por país (día actual)': cuerpo_csv[i][7],
            'Defunciones acumuladas al día por país': cuerpo_csv[i][8],
            'Tasa de Mortalidad por cien mil habitantes': cuerpo_csv[i][9]
        })

    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)

    client = MongoClient()  # Inicializamos el objeto
    client = MongoClient('127.0.0.1', 27017)
    db = client['Situation_reports_COVID']
    collection = db['daily_report']
    collection.insert(data)