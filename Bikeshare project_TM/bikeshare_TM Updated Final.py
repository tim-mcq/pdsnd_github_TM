import time
import pandas as pd
import numpy as np
import datetime as dt

cities = ('chicago', 'new york city', 'washington')

months = ('january', 'february', 'march', 'april', 'may', 'june')

days = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday', 'sunday')

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


"""This message initiates the bike share data application"""

print('\nHello, and welcome to the bikeshare database! You can press \'end\' to exit the program or \'restart\' to start again at any time.')


"""This section gathers the user input to inform data filtering"""

def selection(response, selections=('y', 'n')):
    while True:
        selection = input(response).lower().strip()
        response = ("\nOops. Looks like that entry is invalid. Please check your formatting and enter a valid response.\n\nYou can press \'end\' to exit the program or \'restart\' to start again at any time.\n>")
        if ',' in selection:
            selection = [i.strip().lower() for i in selection.split(',')]
            if list(filter(lambda x: x in selections, selection)) == selection:
                break
        elif selection == 'restart':
            main ()
        elif selection == 'end':
            raise SystemExit
        elif ',' not in selection:
            if selection in selections:
                break
    return selection

    """Uses while loop for error handling to evaluate if user entry is valid or not and instructs the user to enter a valid answer if needed. Allows user to enter end to exit program or restart to start again at any time"""



def get_filters():
    while True:
        print('\nWhich cities do you want to select data: New York City, Chicago, or Washington?\nYou can select more than one option by separating your selections with commas.')
        city = selection('\n', cities)
        
        print('\nWhich months (January - June) do you want to filter by?\nYou can select more than one option by separating your selections with commas.')
        month = selection('\n', months) 
        
        print('\nWhich days do you want to filter data by?\nYou can select more than one option by separating your selections with commas.')
        day = selection('\n', days)

        print('\n---\n\nAre these the correct selections?: \n\nCities: {}\nMonths: {}\nDays: {}' 
              .format(city, month, day))
        validation = selection("\n [y] Yes\n [n] No\n\n>")
        if validation == 'y':
            break
        elif validation == 'n':
            print('\nOkay, you can re-select your filters.')

    """Captures the user input for city, month, and day and confirm if selection is correct for filtering"""

    print('-'*40)
    return city, month, day
    return validation


    """This section loads the user selections for data querying. Note that this is referenced in the Practice Solution 3 of this project lesson."""

def load_data(city, month, day):
    try:
        df = pd.read_csv(CITY_DATA[city])
    except TypeError:
        if isinstance(city, list):
            df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city), sort=True)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    df['Start hour'] = df['Start Time'].dt.hour

    """Creates data frames in necessary time format to be used in analysis"""

    try:
        df = df[df['day'] == day.title()]
    except:
        if isinstance(day, list):
            df = pd.concat(map(lambda day: df[df['day'] == (day.title())], day))

    try:
        df = df[df['month'] == (months.index(month))]
    except:
        if isinstance(month, list):
            df = pd.concat(map(lambda month: df[df['month'] == (months.index(month))], month))

    """Loads data file into data frame and provides error handling during data querying"""

    return df
    print('-'*40)


"""This section provides the user information on bike user stat data. This solution is referenced in the Practice Solution 2 of the project lesson """

def bike_user_info(df):
    start_time = time.time()
    print('\nCalculating Bike User Information...\n')

    try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print("\nDistribution for each gender:\n", gender_distribution)
    except KeyError:
        print("Looks like there is no gender data for the city you have selected.")

    """Provides count of gender for queried bike share data"""

    """Uses try and except clauses for error handling in case the user has selected Washington, which does not have gender data"""

    user_types = df['User Type'].value_counts().to_string()
    print("\nDistribution for user types:\n", user_types)


    """Shows count of user types: subscriber or customer"""

    try:
        youngest_birthyear = df['Birth Year'].max()
        print('\nFor the inputs you have selected, the youngest bicyclist was born in:', int(youngest_birthyear))
        oldest_birthyear = df['Birth Year'].min()
        print('\nFor the inputs you have selected, the oldest bicyclist was born in:', int(oldest_birthyear))
        popular_birthyear = df['Birth Year'].mode()[0]
        print('\nFor the inputs you have selected, the most common birth year in the bicyclist data is:', int(popular_birthyear))
    except:
        print("\nLooks like there is no birth year data for the city you have selected.\n")

    """"Returns bike share birth year information based on user input"""

    """Uses try and except clauses for error handling in case the user has selected Washington, which does not have birth year data"""

    print("\nThis statistical analysis required %s seconds to compute." % (time.time() - start_time))
    print('-'*40)

    return user_types
    return earliest_birth_year
    return most_recent_birth_year
    return most_common_birth_year
    return gender_distribution


    """This section shows the user the most popular station and trip details. This solution is referenced in the Practice Solution 1 of the project lesson."""

def location_info(df):
    start_time = time.time()
    print('\nCalculating The Most Popular Trip Location Information...\n')

    popular_start_location = df['Start Station'].mode()[0]
    popular_end_location = df['End Station'].mode()[0]
    df['Start-End Combo'] = df['Start Station']+'  ---> \n'+df['End Station']
    popular_start_end_combo = df['Start-End Combo'].mode()[0]

    print('\nFor the inputs you have selected, the most popular start location is:\n', popular_start_location)

    """Provides the most popular start station"""

    print('\nFor the inputs you have selected, the most popular end location is:\n', popular_end_location)

    """Provides the most popular end station"""

    print('\nFor the inputs you have selected, the most popular start-and-end location combination is:\n', popular_start_end_combo)
    
    """Provides the most popular start-end station combination"""

    print("\nThis calculation required %s seconds to compute." % (time.time() - start_time))
    print('-'*40)

    return popular_start_location
    return popular_end_location
    return popular_start_end_combo


"""This section shows the user the most frequent times of travel data. Note that this is referenced in the Practice Solution 1 of this project lesson."""

def travel_time_prevalence(df):
    start_time = time.time()
    print('\nCalculating The Most Prevalent Travel Times...\n')

    popular_month = df['month'].mode()[0]
    popular_day = df['day'].mode()[0]
    popular_hour = df['Start hour'].mode()[0]

    print('For the month input you have selected, the most popular travel month is:', months[popular_month].title())
    print('For the day input you have selected, the most popular day of the week is:', popular_day)
    print('For the inputs you have selected, the most popular start hour is:', popular_hour)

    """Provides stats on the most popular travel month, day, and hour"""

    print("\nThis calculation required %s seconds to compute." % (time.time() - start_time))
    print('-'*40)

    return popular_month
    return popular_day
    return popular_hour
    

    """This section provides the user stats on the total and average travel time, based on user selection"""

def trip_duration_stats(df):
    start_time = time.time()
    print('\nCalculating Trip Duration Statistics...\n')

    avg_travel_time = df['Trip Duration'].mean()
    avg_travel_time = int(avg_travel_time//60)

    print("For the inputs you have selected, the mean travel time duration is:", avg_travel_time, "minutes.")

    """This provides the mean travel time"""

    sum_total_travel = df['Trip Duration'].sum()
    total_travel_days = int(sum_total_travel//86400)
    total_travel_hours = int((sum_total_travel % 86400)//3600)
    total_travel_mins = int(((sum_total_travel % 86400) % 3600)//60)
    sum_total_travel = (total_travel_days,total_travel_hours,total_travel_mins)

    print('For the inputs you have selected, the total travel time duration is:', total_travel_days,'days,', total_travel_hours,'hours,', total_travel_mins,'minutes.')

    """Provides the total travel time based on user input"""

    print("\nThis calculation required %s seconds to compute." % (time.time() - start_time))
    print('-'*40)

    return avg_travel_time
    return sum_total_travel


    """This section allows user to view raw data for selected data query"""

def display_raw_data(df, mark_place):
    print("\nYou have selected to display the raw data for your bike data inputs.")
    while True:
        for i in range(mark_place, len(df.index)):
            print(df.iloc[mark_place:mark_place+5].to_string())
            mark_place += 5
            print("\n---\nDo you want to see the next 5 rows of raw data?")
            if selection("\n[y]Yes\n[n]No\n\n>") == 'y': continue
            else:
                main ()
                break
    """Uses while loop to display the next 5 rows of raw data if user answers yes"""


"""This section provides the main nav for users to select data inputs through their journey in the app"""

def main():
    while True:
        city, month, day = get_filters()
        mark_place = 0
        df = load_data(city, month, day)
        while True:
            print("\nWhat data are you interested in viewing? You can enter \'end\' or \'restart\' any time.")
            menu_option = selection("\n [bui] Bike User Information\n [lfi] Location Frequency Information\n [ttp] Travel Time Prevalence \n [tds] Trip Duration Statistics\n [drd] Display Raw Data\n\n ", ('bui', 'lfi', 'ttp', 'tds', 'drd'))
            if menu_option == 'bui':
                bike_user_info(df)
            elif menu_option == 'lfi':
                location_info(df)
            elif menu_option == 'ttp':
                travel_time_prevalence(df)
            elif menu_option == 'tds':
                trip_duration_stats(df)
            elif menu_option == 'drd':
                mark_place = display_raw_data(df, mark_place)
                break

        bike_user_info(df)
        location_info(df)
        travel_time_prevalence(df)
        trip_duration_stats(df)

if __name__ == "__main__":
	main()
