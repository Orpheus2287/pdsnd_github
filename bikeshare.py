import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nWhich city do you want to analyze - chicago, new york city, or washington?\n').lower()
    cities = ['chicago', 'new york city', 'washington']
    while city not in cities:
        print('\nNot a valid selection.')
        city = input('\nPlease input one of the following cities: chicago, new york city, washington:\n').lower()
    # get user input for month (all, january, february, ... , june)
    month = input('\nPlease input the month (January - June) that you want to filter by, or select "all" to analyze all months:\n').lower()
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while month not in months:
        month = input('\nPlease input a valid month or input "all" to analyze all months:\n').lower()  
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nPlease input the weekday you want to filter by or select "all" to analyze all days:\n' ).lower()
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while day not in days:
        day = input('\nPlease input a valid weekday or input "all" to analyze all days:\n').lower() 
    
    print('\nFilter Selection Summary:\n City: {}\n Month: {} \n Day: {}'.format(city.title(), month.title(), day.title()))
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['popular_month'] = df['Start Time'].dt.month
    df['popular_weekday'] = df['Start Time'].dt.weekday_name
    df['popular_hour'] = df['Start Time'].dt.hour

    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most popular month is: ', popular_month)
   

    # display the most common day of week
    popular_weekday = df['popular_weekday'].mode()[0]
    print('The most popular weekday is: ', popular_weekday)

    
    # display the most common start hour
    popular_hour = df['popular_hour'].mode()[0]
    print('The most popular start hour is: ', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('The most common start station is: ', start_station)

    
    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('The most common end station is: ', end_station)


    # display most frequent combination of start station and end station trip
    combo_station = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('The most frequent combination of start and end station is:\n', combo_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() / 60 / 60
    print('The total travel time is: %.2f' % total_travel_time, 'hours.')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 60
    print('The mean travel time is: %.2f' % mean_travel_time, 'minutes.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_types = df['User Type'].value_counts()
    print('The user type breakdown is as follows: \n', user_types)

    # display counts of gender
    if 'Gender' in df:
        gender_types = df['Gender'].value_counts()
        print('\nThe gender breakdown is as follows:\n', gender_types)

    else:
        print('\nGender breakdown data is not available.\n')
    # display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_dob = df['Birth Year'].min()
        print('The earliest year of birth is: ', int(earliest_dob))
        recent_dob = df['Birth Year'].max()
        print('The most recent year of birth is: ', int(recent_dob))
        common_dob = df['Birth Year'].mode()[0]
        print('The most common year of birth is: ', int(common_dob))
    else:
        print('The earliest year of birth is: N/A - data not available')
        print('The most recent year of birth is: N/A - data not available')
        print('The most common year of birth is: N/A - data not available')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def raw_data_display(df):
    """Displays 5 rows of data until user says 'no'."""
    i = 0
    list = ['yes', 'y', 'no', 'n'] 
    answer = input('Do you want to see some raw data? (y/n): ').lower()
    
    while answer not in list:
        print('\nNot a valid selection. Please reply with y/n.')
        answer = input('Do you want to see some raw data? (y/n): ').lower()
           
    while answer in ('yes', 'y'):    
        print(df.iloc[i:i+5])
        i += 5
        answer = input('Do you want to see more sample data? (y/n): ').lower()
        
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_display(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
