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
    city = str(input('Choose one city (chicago, new york city, washington): ').lower())
    while city not in CITY_DATA:
        city = str(input('Choose a vaild city (chicago, new york city, washington): ').lower())
    global city_input
    city_input = city


    # get user input for month (all, january, february, ... , june)
    month_list = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    month = str(input('Which month (all, january, february, ... , june): ').lower())
    while month not in month_list:
            month = str(input('Choose a valid month (all, january, february, ... , june): ').lower())

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_list = ('all', 'monday', 'tuesday', 'wednesday', 'thrusday', 'friday', 'saturday', 'sunday')
    day = str(input('Which day of week (all, monday, tuesday, ... sunday): ').lower())
    while day not in day_list:
        day = str(input('Choose a valid day (all, monday, tuesday, ... sunday): ').lower())

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
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month: ', df['month'].mode()[0])

    # display the most common day of week
    print('The most common day of week: ', df['day_of_week'].mode()[0])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most common start hour: ', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common used start station: ', df['Start Station'].mode()[0])


    # display most commonly used end station
    print('The most common used End station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('The most common combination of Start Station and End station: ', df.groupby(['Start Station', 'End Station']).size().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time: ', df['Trip Duration'].sum(skipna=None))

    # display mean travel time
    print('The mean travel time: ', df['Trip Duration'].mean(skipna=None))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())

    if city_input == 'washington':
        print('Washington data does not have Gender and Birth Year information')
    else:
        # Display counts of gender
        print(df['Gender'].value_counts())
        # Display earliest, most recent, and most common year of birth
        print('The most conmmon year of birth: ', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Displays 5 rows of the trip data"""
    
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while (view_data == 'yes'):
        while view_data not in ('yes', 'no'):
            view_data = input("Enter a valid answer: yes or no\n").lower()
        print(df.iloc[start_loc : start_loc + 5])
        start_loc += 5
        view_data = input("Do you wish to continue? Enter yes or no\n").lower()
        while view_data not in ('yes', 'no'):
            view_data = input("Enter a valid answer: yes or no\n").lower()
        


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        while restart not in ('yes', 'no'):
            restart = input("Enter a valid answer: yes or no\n").lower()
        if restart == 'no':
            break


if __name__ == "__main__":
	main()