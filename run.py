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

appliances = ['Dishwasher', 'Washing machine', 'Bread machine', 'Oven', 'Yogurt maker', 'Other', 'Exit' ]

def print_welcome():
    print("\n\nWelcome to:\n\nTIME LORD\n\n")
    print("A night rate appliance time-shifting utility, designed to help you program ")
    print("your appliances to run when cheaper electricity night rates are in effect.\n")

def print_time_options():
    for key in times.keys():
        print (key, '--', times[key][0] )

def set_appliance(appliance_list):
    """
    Input #2 — Get the name of the appliance from the list of available appliances.
    """
    while(True):
        print("Please choose the appliance that you're setting a timer for:")
        for i in range(len(appliance_list)):
            print (i+1, '--', appliance_list[i] )    
        option = ''
        try:
            option = int(input('Enter your choice: '))            
        except:
            print('Wrong input. Please enter a number ...')
        # Check that choice is within range of options
        if option not in range(1,len(appliance_list)+1): 
            print(f"\nInvalid option. Please enter a number between 1 and {len(appliance_list)}.\n")
        else:
            # Handle exit
            if appliance_list[option-1].lower() == 'exit':
                print('\nExiting Time Lord... thank you & bye bye!\n')
                exit()
            return appliance_list[option-1]


def get_menu_index_from(menu_dict):
    """
    Allows user to choose an option from a menu dictionary passed as an argument
    """
    while(True):
        print("Please choose one of the following options:")
        for key in menu_dict.keys():
            print (key, '--', menu_dict[key][0] )

        option = ''
        try:
            option = int(input('Enter your choice: '))            
        except:
            print('Wrong input. Please enter a number ...')
        # Check that choice is within range of options
        if option not in range(1,len(menu_dict)+1): 
            print(f"\nInvalid option. Please enter a number between 1 and {len(menu_dict)}.\n")
        else:
            # Handle exit
            if menu_dict[option][0].lower() == 'exit':
                print('\nExiting Time Lord... thank you & bye bye!\n')
                exit()
            # return selected option
            return option


def main():
    """
    Run all program functions
    """
    print_welcome()
    now = datetime.now(pytz.timezone("Europe/Dublin"))
    # print("The current time in Ireland is:", now.strftime("%H:%M"))
    
    # Step #1:  Select cheap rate time window
    print("\nFirst, tell me the times that your cheapest electricity rates apply. These are examples of the most ")
    print("common time windows for lower night rate electricity offered by Irish energy providers in 2024.\n")
    times_index = get_menu_index_from(times)
    print(f"\nSelected low rate time window: {times[times_index][0]}\n")
    
    # Step #2: Select the appliance timer is being set on (for feedback only)
    appliance = set_appliance(appliances)
    print(f"\nAppliance chosen: {appliance}\n")

    # Step #3: Select timer option / required input (what we need to calculate)
    print(f"Now, tell me which of the following best describes the input your {appliance.lower()} requires to set the time delay.\n")
    timer_index = get_menu_index_from(timer_options)
    print(f"\nSelected timer option: {timer_options[timer_index][0]}\n")

    # Step #4: Get cycle duration / running / cooking time
    print(f"How long will the {appliance.lower()} run?")
    duration = input("Enter the duration in HH:MM\n")
    hour, min = duration.split(":")
    print("Running time will be: " hour, "hours and", min, "minutes")

    

main()
