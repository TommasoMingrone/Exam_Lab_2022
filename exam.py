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

        # If the name is not a string, it generates an error
        if not isinstance(name, str):
            raise ExamException(f'Error: the "name" parameter must be a string, not  "{type(name)}"')

        # Set the name
        self.name = name
        
    def get_data(self):

        # Initialising an empty list to save items
        data = []

        # I try to open the file. If I can't, I print an error
        try:
            my_file = open(self.name, 'r')
        except Exception as e:
            raise ExamException('Error: file cannot be read: "{}"'.format(e))

        # I read the file line by line
        for line in my_file:
            try:
                # I remove the newline character from the last element with the strip() function:
                line=line.strip()
                # I split each line on the comma
                elements = line.split(',')
                elements=elements[:2]
                # I split each line on the dash
                timestamp = elements[0].split("-")
                timestamp=timestamp[:2]
                # Changing timestamp type to int, skipping the first line
                if elements[0] != 'date':
                    timestamp[0]=int(timestamp[0])
                    timestamp[1]=int(timestamp[1])
                    assert(timestamp[0]>0)

                    # I check that the timestamp is of the type '[year,month]' without additional data
                    # and that elements be of the type '[year-month, passengers]' without additional data
                    if len(timestamp)<2 or len(elements)<2:
                        raise Exception("Errore: linea non valida")

                    # Check that the months are actually between 1 and 12
                    if timestamp[1]<1 or timestamp[1]>12:
                        raise Exception("Error: not valid moth")
    
                # If I am not processing the header
                if elements[0] != 'date':
                  # Converting to int
                  elements[1]=int(elements[1])
                  assert(elements[1]>0)

                  # Adding the elements to list
                  data.append(elements)

            except Exception as e:
                print(e)

        try:
            # Checking line by line
            for i in range(1, len(data)):
              # If there is a data mismatch problem, 
              # so if the year of the preceding line is greater than the following one
              if data[i-1][0]>data[i][0]:
                  raise ExamException("Error: not valid timestamps")
              # SIf the month of the previous line is greater than the next
              if data[i-1][0]==data[i][0] and data[i-1][1]>=data[i][1]:
                  raise ExamException("Error: not valid timestamps")
        except ExamException as e:
            raise ExamException(e)
          
        # Closing the file
        my_file.close()

        return data


# Creating the compute_avg_monthly_difference function
def compute_avg_monthly_difference(time_series, first_year, last_year):

  # If first_year and last_year are not strings it generates an error
  if not isinstance(first_year, str):
      raise ExamException(f'Error: Parameter "first_year" must be a string, not "{type(first_year)}"')
  if not isinstance(last_year, str):
      raise ExamException(f'Error: Parameter "last_year" must be a string, not "{type(last_year)}"')
  try:
      # Converting to int
      last_year=int(last_year)
      first_year=int(first_year)
      # I check that this is true, otherwise I raise an exception
      assert(last_year-first_year>0)
  except:
      raise ExamException('Error: conversion failed')
  
  # I initialise an empty list to save values
  values=[]

  # Cycle for the chosen year interval
  for i in range(last_year-first_year+1):
      # Adding lists as many as the interval of years chosen
      values.append([])

      # 12-month cycle
      for j in range(12):
        # Adding empty elements to the list
        values[i].append(None)

  # At this point there is this situation: values=[[None],[None],[None]...]

  # Cycle to change the format of time_series #["1949-01", 112].
  for i in range(len(time_series)):
      tmp = time_series[i][0].split("-")
      tmp[0]=int(tmp[0])
      tmp[1]=int(tmp[1])
      # I concatenate the year and month with the value
      time_series[i]=tmp+[time_series[i][1]]
    
  # Check that the year taken into consideration is actually part of the chosen interval
  if time_series[0][0]>first_year or time_series[-1][0]<last_year:
      raise ExamException('Error: invalid range')
  
  for t in time_series:
      # At this point: t = [1949,1,112].

      # If t[0] is within the interval
      if t[0]>=first_year and t[0]<=last_year:

          # Calculating the correlation between passengers and their respective years and months
          values[t[0]-first_year][t[1]-1]=t[2]
  
  for i in range(last_year-first_year+1):
      print('Year:',1949+i,values[i])

  # I initialise an empty list to save the values of variations
  varMedia=[]

  # 12-month cycle
  for m in range(12):
      # Adding to the list
      varMedia.append(0)
      
      # I initialise an empty list to save the passenger values for each month
      month_values=[]

      # Cycle for the chosen year interval
      for y in range(last_year-first_year+1):
        
        # If values is not empty... (So, if a line is empty, it returns None)
        if values[y][m] is not None:
        
          # Adding monthly passenger values to the list
          month_values.append(values[y][m])


      # If month_values is not empty
      if month_values!=[]:
        
        # Cycle through all months
        for i in range(len(month_values)-1):
          
          # Calculating the monthly varation
          varMedia[m]+=month_values[i+1]-month_values[i]

        # Checking that there are at least 2 measurements
        if len(month_values) >=2:

          # Calculating the average monthly variation
          varMedia[m]/=len(month_values)-1

  # Return the varMedia list
  print('The average monthly change in passengers is:')
  return varMedia

#=========================================================================#
#                                   MAIN                                  #
#=========================================================================#

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
result = compute_avg_monthly_difference(time_series, '1949', '1960')
print(result)