import matplotlib.pyplot as plt
import numpy as np
import pandas

def entries_by_hour(turnstile_weather, csv=False):
    '''
    plots two histograms on the same axes to show hourly entries at
    different times across the day
    '''
    if csv:
        df = pandas.read_csv(turnstile_weather)
    else:
        df = turnstile_weather

    bins = 24
    xmin = ymin = 0
    xmax = 23
    ymax = 3000

    plt.figure()

    # df['Hour'].hist(bins=bins)
    pivot = pandas.tools.pivot.pivot_table(df, values='ENTRIESn_hourly', rows=['Hour'],\
                                           aggfunc=np.mean)

    entries = pivot.values
    hours = pivot.index

    plt.plot(hours, entries, '-o')

    plt.axis([xmin, xmax, ymin, ymax])
    plt.suptitle('Average subway entries by time of day')
    plt.xlabel('Time of day (24-hr)')
    plt.ylabel('Entries')

    return plt

if __name__ == '__main__':
    entries_by_hour('turnstile_data_master_with_weather.csv', True)
    plt.show()