import pandas
import pandasql
import csv
import datetime
import time

# ps2.1
def num_rainy_days(filename):
    '''
    converts a CSV file into a dataframe and runs a SQL query, returning a
    count of days when it rained.
    '''
    weather_data = pandas.read_csv(filename)

    q = """
    SELECT count(*)
    FROM weather_data
    WHERE rain=1;
    """

    rainy_days = pandasql.sqldf(q.lower(), locals())
    return rainy_days

# ps2.2
def max_temp_aggregate_by_fog(filename):
    '''
    converts a CSV file into a dataframe and runs a SQL query, returning the
    max temperatures on days with and without fog.
    '''
    weather_data = pandas.read_csv(filename)

    q = """
    SELECT fog, max(cast (maxtempi as integer))
    FROM weather_data
    GROUP BY fog;
    """

    foggy_days = pandasql.sqldf(q.lower(), locals())
    return foggy_days

# ps2.3/4
def avg_min_temperature(filename):
    '''
    converts a CSV file into a dataframe and runs a SQL query, returning the
    average minimum temperature
    '''
    weather_data = pandas.read_csv(filename)

    q = """
    SELECT avg(cast (mintempi as integer))
    FROM weather_data
    WHERE cast (mintempi as integer) > 55 and rain=1;
    """

    #Execute your SQL command against the pandas frame
    mean_temp_weekends = pandasql.sqldf(q.lower(), locals())
    return mean_temp_weekends

# ps2.5
def fix_turnstile_data(*filenames):
    '''
    fixes turnstile data, converting the below input to output:

    input example: A002,R051,02-00-00,04-30-11,00:00:00,REGULAR,003143506,
    001087907,04-30-11,04:00:00,REGULAR,003143547,001087915,04-30-11,08:00:00,
    REGULAR,003143563,001087935,04-30-11,12:00:00,REGULAR,003143646,001088024,
    04-30-11,16:00:00,REGULAR,003143865,001088083,04-30-11,20:00:00,REGULAR,
    003144181,001088132,05-01-11,00:00:00,REGULAR,003144312,001088151,05-01-11,
    04:00:00,REGULAR,003144335,001088159

    output example:
    A002,R051,02-00-00,05-28-11,00:00:00,REGULAR,003178521,001100739
    A002,R051,02-00-00,05-28-11,04:00:00,REGULAR,003178541,001100746
    A002,R051,02-00-00,05-28-11,08:00:00,REGULAR,003178559,001100775

    write the updates to a text file in the format of "updated_" + filename.
    '''
    for name in filenames:
        result = []
        raw = read_csv(name)
        for row in raw:
            first = row.pop(0)
            second = row.pop(0)
            third = row.pop(0)
            while row:
                new_line = [first, second, third]
                for item in range(min(5,len(row))):
                    new_line.append(row.pop(0).strip())
                result.append(new_line)
        write_csv('updated_'+name, result)

def read_csv(filename):
    result = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            result.append(row)
    return result

def write_csv(filename, array):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for row in array:
            writer.writerow(row)

# ps2.6
def create_master_turnstile_file(filenames, output_file):
    '''
    takes the files in the list filenames and consolidates them into one file
    located at output_file.
    '''
    header_string = 'C/A,UNIT,SCP,DATEn,TIMEn,DESCn,ENTRIESn,EXITSn\n'
    with open(output_file, 'w') as master_file:
        master_file.write(header_string)
        for filename in filenames:
            with open(filename, 'r') as input_file:
                for line in input_file:
                    if line.strip() == header_string.strip():
                        pass
                    else:
                        master_file.write(line)

# ps2.7
def filter_by_regular(filename):
    '''
    reads the csv file located at filename into a pandas dataframe, and filters
    the dataframe to only rows where the 'DESCn' column has the value 'REGULAR'.
    '''

    df = pandas.read_csv(filename)
    turnstile_data = df[df['DESCn']=='REGULAR']
    return turnstile_data

# ps2.8
def get_hourly_entries(df):
    '''
    changes the cumulative entry numbers to a count of entries since the last reading
    (i.e., entries since the last row in the dataframe).
    '''
    df['ENTRIESn_hourly'] = df['ENTRIESn'] - df['ENTRIESn'].shift(periods=1)
    df = df.fillna(1)

    return df

# ps2.9
def get_hourly_exits(df):
    '''
    changes the cumulative exit numbers to a count of exits since the last reading
    (i.e., exits since the last row in the dataframe).
    '''

    df['EXITSn_hourly'] = df['EXITSn'] - df['EXITSn'].shift(periods=1)
    df = df.fillna(0)

    return df

# ps2.10
def time_to_hour(time):
    '''
    given an input variable time that represents time in the format of:
    "00:00:00" (hour:minutes:seconds)

    returns the hour as an integer
    '''

    hour = int(time.split(':')[0])
    return hour

# ps2.11
def reformat_subway_dates(date):
    '''
    converts dates formatted in the format month-day-year to dates formatted
    as year-month-day.
    '''

    array = time.strptime(date, "%m-%d-%y")

    date = datetime.datetime(array[0], array[1], array[2])
    date_formatted = date.strftime("%Y-%m-%d")

    return date_formatted

if __name__ == '__main__':
    print "Number of rainy days:"
    print num_rainy_days('weather_underground.csv')
    raw_input("Press Enter to continue...")
    print "Maximum temperature aggregate by fog:"
    print max_temp_aggregate_by_fog('weather_underground.csv')
    raw_input("Press Enter to continue...")
    print "Average minimum temperature:"
    print avg_min_temperature('weather_underground.csv')
    raw_input("Press Enter to continue...")
    print "Fixed turnstile data:"
    fix_turnstile_data('turnstile_110507.txt')
    print open('updated_turnstile_110507.txt').read()
    raw_input("Press Enter to continue...")
    print "Filter by regular:"
    df = filter_by_regular('turnstile_data.csv')
    print df
    raw_input("Press Enter to continue...")
    print "Hourly entries:"
    df = pandas.read_csv('turnstile_data.csv')
    print get_hourly_entries(df)
    raw_input("Press Enter to continue...")
    print "Hourly exits:"
    df = pandas.read_csv('turnstile_data.csv')
    print get_hourly_exits(df)
