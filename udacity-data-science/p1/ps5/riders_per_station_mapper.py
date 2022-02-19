import sys
import string
import logging

from util import mapper_logfile
logging.basicConfig(filename=mapper_logfile, format='%(message)s',
                    level=logging.INFO, filemode='w')

def mapper():
    """
    The input to this mapper will be the final Subway-MTA dataset, the same as
    in the previous exercise.  You can check out the csv and its structure below:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv

    For each line of input, the mapper output should PRINT (not return) the UNIT as
    the key, the number of ENTRIESn_hourly as the value, and separate the key and
    the value by a tab. For example: 'R002\t105105.0'

    Since you are printing the output of your program, printing a debug
    statement will interfere with the operation of the grader. Instead,
    use the logging module, which we've configured to log to a file printed
    when you click "Test Run". For example:
    logging.info("My debugging message")

    The logging module can be used to give you more control over your debugging
    or other messages than you can get by printing them. In this exercise, print
    statements from your mapper will go to your reducer, and print statements
    from your reducer will be considered your final output. By contrast, messages
    logged via the loggers we configured will be saved to two files, one
    for the mapper and one for the reducer. If you click "Test Run", then we
    will show the contents of those files once your program has finished running.
    The logging module also has other capabilities; see
    https://docs.python.org/2/library/logging.html for more information.
    """
    keys = []

    for line in sys.stdin:
        data = line.split(',')
        if data[0] == "":
            keys = data
        else:
            data_point = dict(zip(keys,data))
            logging.info(str(data_point['UNIT']) + '\t' + str(data_point['ENTRIESn_hourly']))

mapper()
