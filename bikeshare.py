import time
import pandas as pd
import numpy as np
from collections import Counter

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    print ('Welcome to exploring the Bikeshare data.')
    print('This is how it works: You can select data from one of'
          'three Cities: New York, Chicago or Washington.')
    print('You have two options to further filter the data. By month'
          'and/or by day of the week, if you do not want to filter, '
          'please enter \"All\".')
    print ('Let\'s begin........')
    print ('')
    # list, strings and variables for city, month and day
    city_list = ['Chicago', 'New York City', 'Washington']
    month_list = ['January', 'February', 'March', 'April', 'May', 'June',
                  'All']
    day_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                'Saturday', 'Sunday', 'All']
    city_string = ('Enter city. Choose between New York City, Chicago and'
                   ' Washington ')
    city = None
    month_string = ('Enter month. Valid Options: January, February, March'
                    ', April, June, All  ')
    month = None
    day_string = ('Enter day. Valid Options: Monday, Tuesday, Wednesday,'
                  'Thursday, Friday, Saturday, Sunday, All ')
    day = None
    # Function to get input

    def check_input(data, s_string, data_list):
        while True:
            data = input(s_string)
            data_s = data.title()
            if data_s in data_list:
                print (data_s, 'selected')
                return data_s
                break
            else:
                print ('Please try again. Maybe you mistyped?')

    # Calling function for input
    city = check_input(city, city_string, city_list)
    month = check_input(month, month_string, month_list)
    day = check_input(day, day_string, day_list)
    # Returning three key_values
    return city, month, day


def load_data(city, month, day):
    if city == 'Chicago':
        city = 'chicago.csv'
    elif city == 'New York City':
        city = 'new_york_city.csv'
    elif city == 'Washington':
        city = 'washington.csv'
    else:
        print("Sorry, please try again.")
# Loading the file depending on city, month, day of week and hour columns
    df = pd.read_csv(city)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
# Narrowing the selection based on month
    if month == 'January':
        df = df[df['month'] == 1]
    elif month == 'February':
        df = df[df['month'] == 2]
    elif month == 'March':
        df = df[df['month'] == 3]
    elif month == 'April':
        df = df[df['month'] == 4]
    elif month == 'May':
        df = df[df['month'] == 5]
    elif month == 'June':
        df = df[df['month'] == 6]
    elif month == 'All':
        df = df
    else:
        print("Sorry")
# Narrowing selection based on day
    if day == 'Monday':
        df = df[df['day_of_week'] == day]
    elif day == 'Tuesday':
        df = df[df['day_of_week'] == day]
    elif day == 'Wednesday':
        df = df[df['day_of_week'] == day]
    elif day == 'Thursday':
        df = df[df['day_of_week'] == day]
    elif day == 'Friday':
        df = df[df['day_of_week'] == day]
    elif day == 'Saturday':
        df = df[df['day_of_week'] == day]
    elif day == 'Sunday':
        df = df[df['day_of_week'] == day]
    elif day == 'All':
        df = df
    else:
        print("Sorry")
    print ('')
    print ('The file:', city, ' was loaded, filtering by month:', month, ' and'
           'day of the week: ', day)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    max_hour = df['hour'].value_counts().max()
    frequent_hour = df['hour'].mode()
    print('Most frequent hour to take trips: ', frequent_hour.loc[0])
    print('Total trips taken at that hour: ', max_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station. Using imported counter function
    data = Counter(df['Start Station'])
    pop_start_station_result = data.most_common(1)

    def key_and_values(result, station):  # using loop to separate key/value
            for key, value in result:
                print ('Most popular ', station, ':', key, 'with', value,
                       'trips')
    key_and_values(pop_start_station_result, 'start station')
    data_end = Counter(df['End Station'])
    pop_end_station_result = data_end.most_common(1)
    key_and_values(pop_end_station_result, 'end station')
    # display most frequent combination of start station and end station trip
    pop_combo = df.groupby(['Start Station',
                            'End Station']).size().sort_values(ascending=False)
    print('Most popular combination of start station'
          'and end station:\n', pop_combo.index[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    total_trip_duration = df['Trip Duration'].sum()
    print (total_trip_duration)
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_trip_duration = df['Trip Duration'].sum()
    trip_duration_mean = df['Trip Duration'].mean()
    print('\nTotal Trip Duration for the selected'
          ' time frame: ', total_trip_duration)
    print('Average Trip Duration for the selected time'
          'frame: ', trip_duration_mean)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    df_na = df.dropna(axis=0, how='any')
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    data_user = Counter(df['User Type'])
    user_type = data_user.most_common()
    for key, value in user_type:
        print ('Number of users of type', key, ':', value)
    # Display counts of gender
    if ('Gender') in df:

        gender_user = Counter(df_na['Gender']).most_common()
        for key, value in gender_user:
            print ('Number of', key, 'users:', value)
    else:
        print('The selected data does not contain \"Gender\"')
    # Display earliest, most recent, and most common year of birth
    if ('Birth Year') in df:
        # df_na=df.dropna(axis = 0, how='any')
        min_year = min(df_na['Birth Year'])
        max_year = max(df_na['Birth Year'])
        mode_year = df_na['Birth Year'].mode()[0]
        print ('\nThe oldest rider was born: ', int(min_year))
        print('The youngest rider was born: ', int(max_year))
        print('Most riders were born: ', int(mode_year))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        print('The selected data does not contain \"Birth Year\"')


def raw_data(city):
    if city == 'Chicago':
        city = 'chicago.csv'
    elif city == 'New York City':
        city = 'new_york_city.csv'
    elif city == 'Washington':
        city = 'washington.csv'
    else:
        print("Sorry, please try again.")
    df = pd.read_csv(city)
    raw_quest = input('\nWould you like to see the raw data? ')
    if raw_quest.lower() == 'no':
        print('OK')
    else:
        print(df.iloc[0:5])
    x = 5
    i = 10
    while True:
        raw_quest2 = input('\nWould you like to see five more rows of raw'
                           ' data? ')
        if raw_quest2.lower() == 'no':
            print("OK")
            break
        else:
            print(df.iloc[x:i])
            i = i+5
            x = x+5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
    main()
