### Exam Python Project ###

#==============================#
#  Exception Class             #
#==============================#

class ExamException(Exception):
    pass

#==============================#
#  CSVTimeSeriesFile Class     #
#==============================#

class CSVTimeSeriesFile:

    def __init__(self, name):

        # Se il nome non è una stringa genera un errore
        if not isinstance(name, str):
            raise ExamException(f'Errore: il parametro "name" deve essere una stringa, non "{type(name)}"')

        # Imposta il nome
        self.name = name
        
    def get_data(self):

        # Inizializzo una lista vuota per salvare i valori
        data = []

        # Provo ad aprire il file per estrarci i dati. Se non ci riesco, stampo un errore
        try:
            my_file = open(self.name, 'r')
        except Exception as e:
            
            raise ExamException('Errore: impossibile lettura del file: "{}"'.format(e))

        # Leggo il file linea per linea
        for line in my_file:
            try:
              # Tolgo il carattere di newline dall'ultimo elemento con la funzione strip():
              line=line.strip()
              # Faccio lo split di ogni linea sulla virgola
              elements = line.split(',')
              elements=elements[:2]
              # Faccio lo split di ogni linea sulla trattino
              timestamp = elements[0].split("-")
              timestamp=timestamp[:2]
              # Cambio tipo di timestamp a int, saltando la prima linea
              if elements[0] != 'date':
                  timestamp[0]=int(timestamp[0])
                  timestamp[1]=int(timestamp[1])
                  assert(timestamp[0]>0)

            # Controllo che timestamp sia del tipo "[year,month]" senza dati aggiuntivi
            # e che elements sia del tipo "[year-month, passengers]" senza dati aggiuntivi
                  if len(timestamp)<2 or len(elements)<2:
                      raise Exception("Errore: linea non valida")

                # Controllo che i mesi siano compresi effettivamente tra 1 e 12
                  if timestamp[1]<1 or timestamp[1]>12:
                      raise Exception("Errore: mese non valido")
    
            # Se non sto processando l'intestazione
              if elements[0] != 'date':
                # Converto ad int
                elements[1]=int(elements[1])
                assert(elements[1]>0)

                # Aggiungo alla lista gli elementi
                data.append(elements)

            except Exception as e:
                print(e)

        try:
          # Controllo linea per linea
          for i in range(1, len(data)):
            # Se c'è un problema di sfasatura dei dati, 
            # quindi se l'anno della linea precedente è maggiore della successiva
            if data[i-1][0]>data[i][0]:
              raise ExamException("Errore: timestamps non è valido")
            # Se il mese della linea precedente è maggiore della successiva
            if data[i-1][0]==data[i][0] and data[i-1][1]>=data[i][1]:
              raise ExamException("Errore: timestamps non è valido")
        except ExamException as e:
          raise ExamException(e)
          
        # Chiudo il file
        my_file.close()

        return data


# Creo la funzione compute_avg_monthly_difference
def compute_avg_monthly_difference(time_series, first_year, last_year):

  # Se first_year e last_year non sono delle stringhe genera un errore
  try:
      # Converto ad int
      last_year=int(last_year)
      first_year=int(first_year)
      # Controllo che sia vero, altrimenti alzo un'eccezione
      assert(last_year-first_year>0)
  except:
    raise ExamException('Errore: conversione non riuscita')
  
  # Inizializzo una lista vuota per salvare i valori
  values=[]

  # Ciclo per l'intervallo di anni scelto
  for i in range(last_year-first_year+1):
    values.append([])

    # Ciclo per i 12 mesi
    for j in range(12):

      # Aggiungo alla lista gli elementi vuoti
      values[i].append(None)

  # A questo punto c'è questa situazione: values=[[None],[None],[None]...]

  # Ciclo per cambiare il formato di time_series #["1949-01", 112]
  for i in range(len(time_series)):
    tmp = time_series[i][0].split("-")
    tmp[0]=int(tmp[0])
    tmp[1]=int(tmp[1])
    # Concateno l'anno e mese con il valore
    time_series[i]=tmp+[time_series[i][1]]

  # Faccio i controlli
  if time_series[0][0]>first_year or time_series[-1][0]<last_year:
    raise ExamException('Errore: intervallo non valido')

  for t in time_series:
    # A questo punto: t = [1949,1,112]

    # Se t[0] è compreso nell'intervallo
    if t[0]>=first_year and t[0]<=last_year:

      # Calcolo la correlazione tra i passengers e i rispettivi anni e mesi
      values[t[0]-first_year][t[1]-1]=t[2]
  
  for i in range(last_year-first_year+1):
    print('Anno:',1949+i, values[i])

  # Inizializzo una lista vuota per salvare i valori delle variazioni
  varMedia=[]

  # Ciclo per i 12 mesi
  for m in range(12):

    # Aggiungo alla lista gli elementi
    varMedia.append(0)

    # Inizializzo una lista vuota per salvare i valori dei passeggeri per ogni mese
    month_values=[]

    # Ciclo per l'intervallo di anni scelto
    for y in range(last_year-first_year+1):

      # Se values non è vuoto (Se una linea è vuota, resta 0, quindi torna 0)
      if values[y][m] is not None:
        
        # Aggiugo alla lista gli elementi
        month_values.append(values[y][m])


    # Se month_values non è vuoto
    if month_values!=[]:
      
      # Ciclo scorrendo tutti i mesi
      for i in range(len(month_values)-1):

        # Calcolo la varazione
        varMedia[m]+=month_values[i+1]-month_values[i]

      # Controllo che ci siano almeno 2 misurazioni
      if len(month_values) >=2:

        # Calcolo la variazione media
        varMedia[m] /=len(month_values)-1

  # Ritorno la lista varMedia
  print('La variazione media mensile di passeggeri è:')
  return varMedia

#=========================================================================#
#                                 MAIN                                    #
#=========================================================================#

time_series_file = CSVTimeSeriesFile(name='data.csv')

#print('Nome del file: "{}"'.format(time_series_file.name))
#print('Dati contenuti nel file: "{}"'.format(time_series_file.get_data()))

data = time_series_file.get_data()
res = compute_avg_monthly_difference(data, '1949', '1951')
print(res)