import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta, date, time
# timezone module required to get current local time
# https://www.freecodecamp.org/news/how-to-get-the-current-time-in-python-with-datetime/
import pytz

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('time_lord')


local_tz = "Europe/Dublin"
now = datetime.now(pytz.timezone(local_tz))
RESULT_BANNER = "\n\n———————\nRESULT:\n———————\n\nThe current time in Ireland is: " + now.strftime("%H:%M") + "\n"

"""
A selection of most common night / cheap rate time windows
    1: '12am to 9am' - Electric Ireland Summer night rate
    2: '11pm to 8am' - Electric Ireland winter night rate
    3: '1am to 8am', - SSE Airtricity winter
    4: '2am to 9am', - SSE Airtricity summer
    5: '2am to 4am', - EI cheap boost
    6: '2am to 5am', — Pinergy EV
    7: '7pm to 10pm', - Pinergy Family time
"""
times = {
    1: ['12am to 9am', '00:00', '09:00'],
    2: ['11pm to 8am', '23:00', '08:00'],
    3: ['2am to 9am', '02:00', '09:00'],
    4: ['1am to 8am', '01:00', '08:00'],
    5: ['2am to 4am', '02:00', '04:00'],
    6: ['2am to 5am', '02:00', '05:00'],
    7: ['7pm to 10pm', '19:00', '22:00'],
    8: ['Exit']
}

timer_options = {
    1: ['Start delay (number of hours until appliance starts)'],
    2: ['End delay (number of hours until appliance is finished)'],
    3: ['Start time'],
    4: ['End time'],
    5: ['None of the above'],
    6: ['Exit']
}

appliances = ['Dishwasher', 'Washing machine', 'Bread machine',
              'Oven', 'Yogurt maker', 'Other', 'Exit']

# dictionary to hold validated user data, used to compute result 
user_data = {
    'appliance': '',
    'window_start': '',
    'window_end': '',
    'timer_index': '',
    'duration': '',
    'end_time': ''
}


def print_welcome():
    print("\n\nWelcome to:\n\nTIME LORD\n\n")
    print("A night rate appliance time-shifting utility, designed to help ")
    print("you program your appliances to run when cheaper electricity ")
    print("night rates are in effect.\n")


def print_time_options():
    for key in times.keys():
        print(key, '--', times[key][0])


def set_appliance(appliance_list):
    """
    Input #2 — Get the name of the appliance from the list of available
    appliances.
    """
    while (True):
        print("Please choose the appliance that you're setting a timer for:")
        for i in range(len(appliance_list)):
            print(i+1, '--', appliance_list[i])
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except ValueError:
            print('Wrong input. Please enter a number ...')
        # Check that choice is within range of options
        if option not in range(1, len(appliance_list)+1):
            print("\nInvalid option. Please enter a number between 1 and "
                  f"{len(appliance_list)}")
        else:
            # Handle exit
            if appliance_list[option-1].lower() == 'exit':
                print('\nExiting Time Lord... thank you & bye bye!\n')
                exit()
            return appliance_list[option-1]


def get_menu_index_from(menu_dict):
    """
    Allows user to choose an option from a menu dictionary
    passed as an argument
    """
    while (True):
        print("Please choose one of the following options:")
        for key in menu_dict.keys():
            print(key, '--', menu_dict[key][0])

        option = ''
        try:
            option = int(input('Enter your choice: '))
        except ValueError:
            print('Wrong input. Please enter a number ...')
        # Check that choice is within range of options
        if option not in range(1, len(menu_dict)+1):
            print("\nInvalid option. Please enter a number between 1 and "
                  f"{len(menu_dict)}.\n")
        else:
            # Handle exit
            if menu_dict[option][0].lower() == 'exit':
                print('\nExiting Time Lord... thank you & bye bye!\n')
                exit()
            # return selected option
            return option


def get_time_duration(appliance):
    """
    Get time duration from user in format HH:MM
    """
    while True:
        print(f"How long will the {appliance.lower()} run?")
        duration = input("Enter the duration in HH:MM\n")
        if validate_time(duration):
            break

    return duration


def get_end_time(appliance):
    """
    Get end clock time from user in format HH:MM 
    """
    while True:       
        end_time = input("Enter the time in HH:MM 24hr clock format (i.e. 23:30 for "
                         "11.30pm)\n")
        # before time validation, check for empty field and return false if empty
        if not end_time:
            end_time = False
            break
        elif validate_time(end_time):
            break

    return end_time


def validate_time(time_str):
    """
    Passing required format string to datetime object's strptime method seemed quickest!:
    https://stackoverflow.com/questions/33076617/how-to-validate-time-format
    Was going to check for 2 integers, one for hours,
    one for minutes, either side of a :
    then check minutes within range of 0-59 & hours within 0-23
    """
    timeformat = "%H:%M"
    try:
        datetime.strptime(time_str, timeformat)
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

# def add_date_to_time():


def compute_result():
    """
    Calculate the start delay / end delay / start time / end time
    from user input.
    """

    # convert window_start & window_end to date objects
    time_window_start = datetime.strptime(user_data['window_start'],"%H:%M")
    time_window_end = datetime.strptime(user_data['window_end'],"%H:%M")
    
    # add day to window_end if window_start is on previous day 
    if time_window_start > time_window_end: 
        time_window_end += timedelta(days=1)
    # get low rate window duration in hours
    window_duration = (time_window_end - time_window_start).total_seconds() / 3600

    # cycle duration
    hours, mins = user_data['duration'].split(':')
    duration_in_minutes = (int(hours) * 60) + int(mins)

    time_window_text = "Your electricity low rate runs from " + user_data['window_start'] + " to " + user_data['window_end'] +"\n"

    # Start delay
    if user_data['timer_index'] == 1:
        print("Calculating start delay in hours...\n")
        # if current time is within time window, no delay so start now!
        # start delay is the number of hours from present to time_window_start
        # time_window_start must be set to a valid day to calculate time tuntil then 
        # this could be:
        # 1) yesterday if current time is during time window & after midnight
        # 2) later or earlier today if day change happens during time window & current time is before midnight
        # 3) tomorrow if no day change during time window
        
        # start by setting time_window_start date object to today
        today = date.today()
        hours, mins = user_data['window_start'].split(':')
        time_window_start = datetime.combine(today, time(int(hours), int(mins)))
        print(time_window_start)

        # if time window end (time_start_window + time window duration) has passed  
        # (less than current time), then add 24 hrs to time window start date
        # First, make the datetime object timezone aware to compare with now
        tw_end = pytz.timezone(local_tz).localize(time_window_start + timedelta(hours=int(window_duration)))
        if tw_end < now:
            time_window_start += timedelta(hours=24)
        # add time window duration to time_window_start to get actual time Window end 
        time_window_end = time_window_start + timedelta(hours=int(window_duration))
        # print("cheap rate starts: ", time_window_start)
        # print("cheap rate ends: ", time_window_end)
        
        if user_data['end_time'] != False:
            # end time specified, so start delay = (end time - cycle duration) - now time
            hours, mins = user_data['end_time'].split(':')

            end_time = pytz.timezone(local_tz).localize(datetime.combine(today, time(int(hours), int(mins))))
                    
            # end_time = pytz.timezone(local_tz).localize(datetime.strptime(user_data['end_time'],"%H:%M"))
            #  if end time is in the past, add 24 hrs
            if end_time < now:
                end_time += timedelta(hours=24)
            start_delay = (end_time - timedelta(minutes=duration_in_minutes)) - now    
            print(RESULT_BANNER)
            print(time_window_text)
            # if int(start_delay.total_seconds()) <= 0:
            #     print(f"No start delay required as the current time is within the selected cheap rate time window "
            #         f"— you can start the {user_data['appliance'].lower()} right away.\n\n")
            # else: 
            print(f"To finish at {user_data['end_time']}, set the start delay on you {user_data['appliance'].lower()} to "
                    f"{int(start_delay.total_seconds() // 3600)} hours and {int((start_delay.total_seconds()//60)%60)} minutes.\n\n")


        else:
            # no end time spedified
            start_delay = pytz.timezone(local_tz).localize(time_window_start) - now
            # print("tz aware start: ", pytz.timezone(local_tz).localize(time_window_start))
            # print("now: ", now)
            # if start delay is negative, you're in the time window so no delay required
            print(RESULT_BANNER)
            print(time_window_text)
            if int(start_delay.total_seconds()) <= 0:
                print(f"No start delay required as the current time is within the selected cheap rate time window "
                    f"— you can start the {user_data['appliance'].lower()} right away.\n\n")
            else: 
                print(f"Set the start delay on you {user_data['appliance'].lower()} to "
                    f"{int(start_delay.total_seconds() // 3600)} hours and {int((start_delay.total_seconds()//60)%60)} minutes.\n\n")

            # print(f"start_delay: {start_delay}")            


    # End delay
    if user_data['timer_index'] == 2:
        print("Calculating end delay in hours...\n")

    # Start time
    if user_data['timer_index'] == 3:
        print("Calculating start time...\n")
    
    # End time
    if user_data['timer_index'] == 4:
        # just set the end time to window_end?
        # end_time = user_data['window_end']
        # print("Calculating best end time...\n")
        earliest_end_time = time_window_start + timedelta(minutes=duration_in_minutes)
        # if window_start + duration is less than window_end: set end time to 
        # any time between (window_start + duration) and window_end
        # otherwise set it to window_end

        print(RESULT_BANNER)
        print(time_window_text)
        if user_data['end_time'] != False:
            end_time = datetime.strptime(user_data['end_time'],"%H:%M")
            if time_window_start > end_time: 
                end_time = end_time + timedelta(days=1)
        else: 
            end_time = time_window_end

        if earliest_end_time < end_time: 
            print(f"To get the most savings, set your {user_data['appliance'].lower()} to finish anytime between {earliest_end_time.strftime("%H:%M")} and {end_time.strftime("%H:%M")}.\n\n")
        else:
            print(f"To get the most savings, just set your {user_data['appliance'].lower()} to finish at {end_time.strftime("%H:%M")}.\n\n")

    print(f"{user_data}")


def main():
    """
    Run all program functions
    """
    print_welcome()

    # Step #1:  Select cheap rate time window
    print("———————\nSTEP 1:\n———————\n")
    print("First, tell me the times that your cheapest electricity rates "
          "apply. These are the most common time windows for lower night rate "
          "electricity offered by Irish energy providers in 2024.\n")
    times_index = get_menu_index_from(times)
    user_data['window_start'] = times[times_index][1]
    user_data['window_end'] = times[times_index][2]
    print(f"\nSelected low rate time window: {times[times_index][0]}\n\n")

    # Step #2: Select the appliance timer is being set on (for feedback only)
    print("———————\nSTEP 2:\n———————\n")
    appliance = set_appliance(appliances)
    user_data['appliance'] = appliance
    print(f"\nAppliance chosen: {appliance}\n\n")

    # Step #3: Select timer option / required input (what we need to calculate)
    print("———————\nSTEP 3:\n———————\n")
    print("Now, tell me which of the following best describes the input"
          f" your {appliance.lower()} requires to set the time delay.\n")
    timer_index = get_menu_index_from(timer_options)
    user_data['timer_index'] = timer_index
    print(f"\nSelected timer option: {timer_options[timer_index][0]}\n\n")

    # Step #4: Get cycle duration / running / cooking time
    print("———————\nSTEP 4:\n———————\n")
    duration = get_time_duration(appliance)
    user_data['duration'] = duration

    hour, min = duration.split(":")
    print("\nRunning time will be: ", hour, "hours and", min, "minutes\n\n")

    # Step #5: Set the time you would like the appliance to finish at,
    # i.e. you might want your bread to finish cooking at 7am. 
    # Input required if user selected end time (option 4) in Step #3 otherwise optional
    print("———————\nSTEP 5:\n———————\n")
    if timer_index == 4:
        print(f"Lastly, you selected end time (option 4) as the timer input for your "
           f"{appliance.lower()}, so please enter that here. \n")
    else:
        print(f"Lastly, if you'd like the {appliance.lower()} to finish at a "
           "specific time, enter it here or just leave it blank & hit enter. \n")
    end_time = get_end_time(appliance)
    user_data['end_time'] = end_time
    if end_time != False:
        print(f"\nPerfect! You'd like the {appliance.lower()} to finish at {end_time}. \n\n")
    # print(f"your {appliance.lower()} requires to set the time delay.\n")     

    # Step #6 - compute & return result to the user
    compute_result()

main()
