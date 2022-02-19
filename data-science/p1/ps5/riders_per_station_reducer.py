import sys
import logging

from util import reducer_logfile
logging.basicConfig(filename=reducer_logfile, format='%(message)s',
                    level=logging.INFO, filemode='w')

def reducer():
    '''
    Given the output of the mapper for this exercise, the reducer should PRINT
    (not return) one line per UNIT along with the total number of ENTRIESn_hourly
    over the course of May (which is the duration of our data), separated by a tab.
    An example output row from the reducer might look like this: 'R001\t500625.0'

    You can assume that the input to the reducer is sorted such that all rows
    corresponding to a particular UNIT are grouped together.

    Since you are printing the output of your program, printing a debug
    statement will interfere with the operation of the grader. Instead,
    use the logging module, which we've configured to log to a file printed
    when you click "Test Run". For example:
    logging.info("My debugging message")
    '''
    register = {}
    for line in sys.stdin:
        data = line.split('\t')
        if len(data) != 2:
            continue
        else:
            unit, entries = data[0], data[1]
            if unit in register:
                register[unit] += float(entries)
            else:
                register[unit] = float(entries)

    for key in register:
        msg = str(key) + '\t' + str(register[key])
        logging.info(msg)
        print msg

    # running_entries = 0
    # previous_key = None

    # for line in sys.stdin:
    #     data = line.split('\t')
    #     if len(data) != 2:
    #         continue
    #     else:
    #         key, entries = data[0], data[1]
    #         if key != previous_key and previous_key:
    #             msg = str(previous_key) + '\t' + str(running_entries)
    #             logging.info(msg)
    #             print msg
    #             running_entries = float(entries)
    #         else:
    #             running_entries += float(entries)
    #         previous_key = key
    # final_msg = str(previous_key) + '\t' + running_entries
    # logging.info(final_msg)
    # print final_msg


reducer()
