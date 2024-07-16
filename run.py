import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
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

def print_welcome():
    print("\n\nWelcome to:\n\nTIME LORD\n\n")
    print("A night rate appliance time-shifting utility, designed to help you program ")
    print("your appliances to run during cheaper electricity night rates apply.\n")

def print_time_options():
    for key in times.keys():
        print (key, '--', times[key][0] )

def set_times_index():
    """
    Input #1 — Get night rate period from the user.
    Use a menu option to select from preset time windows.
    Python terminal menu code from: 
    https://computinglearner.com/how-to-create-a-menu-for-a-python-console-application/
    Runs a while loop to collect a valid integer from the user
    via the terminal. The loop will repeatedly request data, until it is valid.
    Uses int method to check for valid integer.

    1: '12am to 9am' - Electric Ireland Summer night rate
    2: '11pm to 8am' - Electric Ireland winter night rate
    3: '1am to 8am', - SSE Airtricity winter 
    4: '2am to 9am', - SSE Airtricity summer 
    5: '2am to 4am', - EI cheap boost 
    6: '2am to 5am', — Pinergy EV
    7: '7pm to 10pm', - Pinergy Family time
    8: exit
    """
    
    while(True):
        print("First, let me know the time your cheapest electricity rates apply. These are examples of the most ")
        print("common time windows for lower night rate electricity offered by Irish energy providers in 2024.\n")
        print("Please choose one of the following options:")
        print_time_options()
        option = ''
        try:
            option = int(input('Enter your choice: '))            
        except:
            print('Wrong input. Please enter a number ...')
        # Check that choice is within range of options
        if option not in range(1,9): 
            print('\nInvalid option. Please enter a number between 1 and 8.\n')
        else:
            # Handle exit
            if option == 8:
                print('\nExiting Time Lord... thank you & bye bye!\n')
                exit()
            # set time_window
            return option

def main():
    """
    Run all program functions
    """
    print_welcome()
    now = datetime.now(pytz.timezone("Europe/Dublin"))
    print("The current time in Ireland is:", now.strftime("%H:%M"))
    times_index = set_times_index()
    print(f"Selected low rate time window: {times[times_index][0]}")
    # print(times[times_index])

main()
