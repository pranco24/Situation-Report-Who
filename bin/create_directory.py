import os
from datetime import datetime
from datetime import timedelta
import locale
import os.path as path
#locale.setlocale(locale.LC_ALL, 'es-MX')
main_path = path.abspath(path.join(__file__ ,"../../"))
dias_atraso = 0

yesterday = (datetime.now()-timedelta(days=dias_atraso)).strftime('%Y%m%d')
directory_today = main_path +'/dir/'+ yesterday



yesterday_format=(datetime.now()-timedelta(days=dias_atraso)).strftime('%Y-%m-%d')
yesterday_text = (datetime.now()-timedelta(days=dias_atraso)).strftime('%d de %B de %Y')
try:
    os.mkdir(directory_today)
except OSError:
    print("")
else:
    print ("Directorio creado satisfactoriamente %s " % directory_today)
