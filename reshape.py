# script per modificare il file calendar_dates.txt

input_file = 'GTFS_230406_240405\calendar_dates.txt'
output_file = 'new_calendar_dates.txt'
header = 'service_id,year,month,day,exception_type'

with open(input_file, 'r') as file_in, open(output_file, 'w') as file_out:
    for line_num, line in enumerate(file_in):
        if line_num == 0:
            # Scrive la prima riga senza modifiche nel file di output
            file_out.write(header)
        else:
            # Modifica le righe successive differenziando l'anno il mese e il giorno
            parts = line.strip().split(',')
            date = parts[1]
            modified_date = f"{date[:4]},{date[4:6]},{date[6:]}"
            modified_line = f"{parts[0]},{modified_date},{parts[2]}"
            file_out.write(modified_line + '\n')
