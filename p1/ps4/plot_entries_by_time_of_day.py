from pandas import *
from ggplot import *

def plot_weather_data(turnstile_weather, csv=False):
    '''
    plots a histogram of entries by time of day
    '''
    if csv:
        df = read_csv(turnstile_weather)
    else:
        df = turnstile_weather

    plot = ggplot(df, aes(x='Hour')) +\
           geom_histogram(binwidth=1) +\
           scale_x_continuous(limits=[0,23]) +\
           ggtitle('NYC Subway ridership by time of day') + xlab('Hour (24-hr)') + ylab('Entries')
    return plot


if __name__ == '__main__':
    filename = 'turnstile_data_master_with_weather.csv'
    print plot_weather_data(filename, True)