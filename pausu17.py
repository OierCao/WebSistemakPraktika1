import csv
import time
from datetime import datetime, timedelta

# CSV file name
csvPath = 'pausu17.csv'  # Actualiza esto con tu ruta deseada

# Crear y escribir en el archivo CSV
with open(csvPath, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Escribir el encabezado
    writer.writerow(['time-stamp', 'field1', 'field2'])

    for i in range(2):
        time_stamp = datetime.now()
        field1 = 23
        field2 = 47
        # Escribir en el archivo CSV
        writer.writerow([time_stamp.strftime('%Y-%m-%d %H:%M:%S'), field1, field2])
        #Para que no sea inmediato, hacemos que espere 3seg
        time.sleep(3)
