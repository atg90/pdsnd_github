import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'newyork': 'new_york_city.csv',
              'washington': 'washington.csv' }

def load_data():

    # get user input for city (chicago, new york city, washington).
    print('-'*40,'\nHello! Let\'s explore some US bikeshare data!')
    city = ''
    while city not in CITY_DATA:
            city = input('\nWhich city do you like to explore US bihkeshare data for?\n \
            Chicago, NewYork or Washington\n').lower()
            if city not in CITY_DATA:
                print('Ops! City name entered is not available. Please choose from above..')
    df = pd.read_csv(CITY_DATA[city])

    return city, df

def get_filters(df):
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.dayofweek
    df['weekdayname'] = df['Start Time'].dt.weekday_name

    month, day = '', ''
    unique_months_index, unique_months = [], []
    unique_days_index, unique_days = [], []
    
    #find the list of months available in the raw data
    unique_months_index = sorted(df['month'].unique())
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    for i in unique_months_index:
        unique_months.append(months[i-1])
    
    # get user input for month (all, january, february, ... , june)
    while month not in unique_months:
        print('\nWhat month do you like to get the data analysis for?\n \
        Choose month filter from below list or type \'All\'')
        for unique_month in unique_months:
            print('{}'.format(unique_month.capitalize()), end = '')
            if unique_month != unique_months[-1]:
                print(' ,', end = ' ')
        month = input('\n').lower()   
        
        if month == 'all':
            break
        elif month not in unique_months:
                print('Ops! Month entered is not correct. Please choose again..')
    
    #assign month number to month variable to be returned and used by other functions
    if month != 'all':
        month = months.index(month) +1

    #find the list of days of the week available in the raw data
    unique_days_index = sorted(df['weekday'].unique())
    days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    for i in unique_days_index:
        unique_days.append(days[i-1])

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in unique_days:
        print('\nWhat day of the week do you like to get the data analysis for?\n \
        Choose day filter from below list or type \'All\'')
        for unique_day in unique_days:
            print('{}'.format(unique_day.capitalize()), end = '')
            if unique_day != unique_days[-1]:
                print(' ,', end = ' ')
        day = input('\n').lower()   

        if day == 'all':
            break
        elif day not in unique_days:
            print('Ops! Day entered is not correct. Please choose again..')

    #assign day number of the week to day variable to be returned and used by other functions
    if day != 'all':
        day = days.index(day)

    print('-'*40)
    return month, day

def filter_data(df, city, month, day):
    
    #Loads data for the specified filters by month if applicable.
    if month != 'all':
        if month in df['month'].unique():
            df = df[df['month'] == month]
        else:
            print('No data is available for this month')

    #Loads data for the specified filters by day if applicable.
    if day != 'all':
        df = df[df['weekday'] == day]

    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'all']
    most_month = df['month'].mode()[0]
    if month != 'all':
        print('No stats for most frequent month. Month filter is applied')
    else:
        print('The most frequent month for travel is: {}'.format(months[most_month].capitalize()))    

    # display the most common day of week
    most_weekday = df['weekdayname'].mode()[0]
    if day != 'all':
        print('No stats for most frequent day of week. Day of week filter is applied')
    else:
        print('The most frequent day of week for travel is: {}'.format(most_weekday))

    # display the most common start hour
    most_hour = df['hour'].mode()[0]
    print('The most frequent traveled hour of the day is: {}'.format(most_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df['Start Station'].mode()[0]
    print('The most frequent Start Station for this filter is: {}'.format(most_start_station))

    # display most commonly used end station
    most_end_station = df['End Station'].mode()[0]
    print('The most frequent End Station for this filter is: {}'.format(most_end_station))

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + '_' + df['End Station']

    most_common_trip = df['trip'].mode()[0]

    most_common_trip_mask = (df['trip'] == most_common_trip)
    most_common_trip_start = df.loc[most_common_trip_mask, 'Start Station'].unique()[0]
    most_common_trip_end = df.loc[most_common_trip_mask, 'End Station'].unique()[0]

    print('The most common trips starts from {} and ends at {}:\n'.format(most_common_trip_start, most_common_trip_end))
    print('The most common trips data are listed below:\n{}'.format(df[df['trip'] == most_common_trip]))
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # here we convert the travel time in minutes to weeks, days, hours & minutes
    total_travel_time_m = df['Trip Duration'].sum()
    total_travel_time_w = total_travel_time_m // (60*24*7)
    total_travel_time_wr = total_travel_time_m % (60*24*7)
    total_travel_time_d = total_travel_time_wr // (60*24)
    total_travel_time_dr = total_travel_time_wr % (60*24)
    total_travel_time_h = total_travel_time_dr // (60)
    total_travel_time_hr = total_travel_time_dr % (60)
    total_travel_time_mr = total_travel_time_hr

    print('Total travel time for this filter is: {} weeks, {} days, {} hrs, {} mins'.format(total_travel_time_w, total_travel_time_d, total_travel_time_h, total_travel_time_mr))
    
    # display mean travel time
    travel_time_avg = int(df['Trip Duration'].mean())
    travel_time_avg_h = int(travel_time_avg // 60)
    travel_time_avg_hr = int(travel_time_avg % 60)

    print('Travel time average for this filter is: {} mins or {} hrs, {} mins'.format(travel_time_avg, travel_time_avg_h, travel_time_avg_hr ))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts()
    print('User types and their counts for this filter are:\n{}'.format(user_count))
    # Display counts of gender
    if city != 'washington':
        gender_count = df['Gender'].value_counts()
        print('Gender types and their counts for this filter are:\n{}'.format(gender_count))


    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        first_birth = int(df['Birth Year'].min())
        last_birth = int(df['Birth Year'].max())
        most_birth = int(df['Birth Year'].mode())
        print('Elder user was born in: {} and younger user was born in: {}, while most common birth is: {}'.format(first_birth, last_birth, most_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, df0 = load_data()
        month, day = get_filters(df0)
        print(city, month, day)
        
        df = filter_data(df0, city, month, day)
        
        #print(df.info())

        #asking user whether to view more raw data or proceed with stats.
        raw_data = 'yes'
        i = 5
        print(df.head(i))
        
        while raw_data == 'yes' or raw_data == 'y':
            raw_data = input('Do you want to see more five (5) raws of data? Enter \'Yes\' to show or any key to skip.  ').lower()
            if raw_data == 'yes' or raw_data == 'y':
                i += 5
                print(df.head(i).tail(5))

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        #asking user whether to restart or end the program
        restart = input('\nWould you like to restart? Enter \'Yes\' or any key otherwise\n')
        if restart.lower() != 'yes' and restart.lower() !='y' :
            break
    

if __name__ == "__main__":
	main()
