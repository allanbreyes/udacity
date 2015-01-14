from pandas import *
from ggplot import *
from datetime import *
from numpy import mean

def plot_weather_data(turnstile_weather, csv=False):
    '''
    plots a histogram of entries by day of week
    '''
    if csv:
        df = read_csv(turnstile_weather)
    else:
        df = turnstile_weather

    df['Day'] = df['DATEn'].map(lambda x:datetime.strptime(x, '%Y-%m-%d')\
                           .strftime('%w'))
    agg = df.groupby(['Day'], as_index=False).aggregate(mean)

    plot = ggplot(agg, aes(x='Day', y='ENTRIESn_hourly')) +\
           geom_line() +\
           ggtitle('NYC Subway ridership by day of week') + xlab('Week day (0=Sunday)') + ylab('Entries')
    return plot

if __name__ == '__main__':
    filename = 'turnstile_data_master_with_weather.csv'
    print plot_weather_data(filename, True)