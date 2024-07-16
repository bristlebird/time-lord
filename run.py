import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
# timezone module required to get current local time
# https://www.freecodecamp.org/news/how-to-get-the-current-time-in-python-with-datetime/
import pytz 
import time 

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('time_lord')

def print_welcome():
    print("\n\nWelcome to:\n\nTIME LORD\n\n")
    print("A night rate appliance time-shifting utility, designed to help you program ")
    print("your appliances to run during cheaper electricity night rates apply.\n")

menu_options = {
    1: '12am to 9am',
    2: '11pm to 8am',
    3: '2am to 9am',
    4: '1am to 8am',
    5: '2am to 4am',
    6: '2am to 5am',
    7: '7pm to 10pm',
    8: 'Exit',
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def get_night_rate_period():
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
    """

    while(True):
        print("First, let me know the time your cheapest electricity rates apply. These are examples of the most ")
        print("common time windows for lower night rate electricity offered by Irish energy providers in 2024.\n")
        print("Please choose one of the following options:")
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        #Check what choice was entered and act accordingly
        if option == 1:
           print('Handle option \'Option 1\'')
        elif option == 2:
            print('Handle option \'Option 2\'')
        elif option == 3:
            print('Handle option \'Option 3\'')
        elif option == 4:
            print('Handle option \'Option 4\'')
        elif option == 5:
            print('Handle option \'Option 5\'')
        elif option == 6:
            print('Handle option \'Option 6\'')
        elif option == 7:
            print('Handle option \'Option 7\'')
        elif option == 8:
            print('\nExiting Time Lord... thank you & bye bye!\n')
            exit()
        else:
            print('\nInvalid option. Please enter a number between 1 and 8.\n')



def main():
    """
    Run all program functions
    """
    print_welcome()

    # irelandTz = pytz.timezone("Europe/Dublin") 
    now = datetime.now(pytz.timezone("Europe/Dublin"))
    print("The current time in Ireland is:", now.strftime("%H:%M"))
    get_night_rate_period()

main()
