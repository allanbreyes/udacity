from ggplot import *
import matplotlib.pyplot as plt
import numpy as np
import pandas
import scipy
import scipy.stats

# ps3.1
def entries_histogram(turnstile_weather, csv=False):
    '''
    plots two histograms on the same axes to show hourly entries when raining
    vs. when not raining.
    '''
    if csv:
        df = pandas.read_csv(turnstile_weather)
    else:
        df = turnstile_weather

    bins = 150
    alpha = 0.5
    xmin = ymin = 0
    xmax = 6000
    ymax = 45000

    plt.figure()

    df['ENTRIESn_hourly'][df['rain'] == 0].hist(bins=bins, alpha=alpha)
    df['ENTRIESn_hourly'][df['rain'] == 1].hist(bins=bins, alpha=alpha)

    plt.axis([xmin, xmax, ymin, ymax])
    plt.suptitle('Histogram of ENTRIESn_hourly')
    plt.xlabel('ENTRIESn_hourly')
    plt.ylabel('Frequency')
    plt.legend(['No rain', 'Rain'])

    return plt

# ps3.3
def mann_whitney_plus_means(turnstile_weather, csv=False):
    '''
    consumes the turnstile_weather dataframe (or csv file), and returns:
        1) the mean of entries with rain
        2) the mean of entries without rain
        3) the Mann-Whitney U-statistic and p-value comparing the number
           of entries with rain and the number of entries without rain
    '''
    if csv:
        df = pandas.read_csv(turnstile_weather)
    else:
        df = turnstile_weather

    df_wet = df['ENTRIESn_hourly'][df['rain'] == 1] # 44104
    df_dry = df['ENTRIESn_hourly'][df['rain'] == 0] # 87847

    with_rain_mean = df_wet.mean()
    without_rain_mean = df_dry.mean()

    U, p = scipy.stats.mannwhitneyu(df_wet, df_dry)

    return with_rain_mean, without_rain_mean, U, p

def normalize_features(array):
   '''
   normalizes the features in the data set.
   '''
   mu = array.mean()
   sigma = array.std()
   array_normalized = (array - mu)/sigma

   return array_normalized, mu, sigma

def compute_cost(features, values, theta):
    '''
    computes the cost function given a set of features / values,
    and the values for our thetas.
    '''
    m = len(values)
    sum_of_square_errors = (np.square(np.dot(features, theta) - values)).sum()
    return sum_of_square_errors/2*m

def gradient_descent(features, values, theta, alpha, num_iterations):
    '''
    performs gradient descent given a data set with an arbitrary number
    of features.
    '''
    m = len(values)
    cost_history = []

    for i in range(num_iterations):
        predicted_values = np.dot(features, theta) - values
        theta = theta - (alpha/m) * np.dot(predicted_values, features)
        cost = compute_cost(features, values, theta)
        cost_history.append(cost)
    return theta, pandas.Series(cost_history)

def predictions(dataframe):
    '''
    runs predictions via gradient descent on turnstile dataframe
    '''
    # Select Features (try different features!)
    features = dataframe[['rain', 'precipi', 'meanwindspdi', 'Hour', 'meantempi']]

    # Add UNIT to features using dummy variables
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    features = features.join(dummy_units)
    print len(features)

    # Values
    values = dataframe['ENTRIESn_hourly']
    m = len(values)

    features, mu, sigma = normalize_features(features)
    features['ones'] = np.ones(m) # Add a column of 1s (y intercept)

    # Convert features and values to numpy arrays
    features_array = np.array(features)
    values_array = np.array(values)

    # Set values for alpha, number of iterations.
    alpha = 0.1 # please feel free to change this value
    num_iterations = 75 # please feel free to change this value

    # Initialize theta, perform gradient descent
    theta_gradient_descent = np.zeros(len(features.columns))
    theta_gradient_descent, cost_history = gradient_descent(features_array,
                                                            values_array,
                                                            theta_gradient_descent,
                                                            alpha,
                                                            num_iterations)
    print theta_gradient_descent
    plot = plot_cost_history(alpha, cost_history)
    predictions = np.dot(features_array, theta_gradient_descent)
    return predictions, plot


def plot_cost_history(alpha, cost_history):
    '''
    returns plot of the cost history
    '''
    cost_df = pandas.DataFrame({
        'Cost_History': cost_history,
        'Iteration': range(len(cost_history))
    })
    return ggplot(cost_df, aes('Iteration', 'Cost_History')) + \
        geom_point() + ggtitle('Cost History for alpha = %.3f' % alpha )

def plot_residuals(turnstile_weather, predictions):
    '''
    makes a histogram of the residuals, the difference between the original
    hourly entry data and the predicted values)
    '''

    plt.figure()
    (turnstile_weather['ENTRIESn_hourly'] - predictions).hist(bins=150)
    plt.suptitle('Residual histogram')
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    return plt

def compute_r_squared(data, predictions):
    '''
    Calculate R square -- the coefficient of determination. The closer to one,
    the better the model.

    Given a list of original data points, and also a list of predicted data
    points, write a function that will compute and return the coefficient of
    determination (R^2) for this data.  numpy.mean() and numpy.sum() might both
    be useful here, but not necessary.

    Documentation about numpy.mean() and numpy.sum() below:
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.mean.html
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.sum.html
    '''

    r_squared = 1-(np.sum(np.square(data-predictions)))/\
                np.sum(np.square(data-np.mean(data)))

    return r_squared

if __name__ == '__main__':
    filename = 'turnstile_data_master_with_weather.csv'
    df = pandas.DataFrame.from_csv(filename)

    # print "Histogram of turnstile data:"
    # entries_histogram(filename, True)
    # plt.show()
    # raw_input("Press enter to continue...")

    # print "Mann-Whitney U test:"
    # print mann_whitney_plus_means(filename, csv=True)
    # raw_input("Press enter to continue...")

    print "Linear regression predictions via gradient descent:"
    predicted, plot = predictions(df)
    print plot
    raw_input("Press enter to continue...")

    print "Plotting residuals:"
    plot_residuals(df, predicted)
    plt.show()
    raw_input("Press enter to continue...")

    print "R-squared value:"
    print compute_r_squared(df['ENTRIESn_hourly'], predicted)
