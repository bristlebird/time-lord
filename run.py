from datetime import datetime, timedelta, date, time
# timezone module required to get current local time
# https://www.freecodecamp.org/news/how-to-get-the-current-time-in-python-with-datetime/
import pytz

# SET UP SOME GLOBAL VARIABLES & DATA STRUCTURES FOR MENUS & USER DATA

local_tz = "Europe/Dublin"
now = datetime.now(pytz.timezone(local_tz))
RESULT_BANNER = "\n\n———————\nRESULT:\n———————\n\n"
"The current time in Ireland is: " + now.strftime("%H:%M") + "\n"

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
    5: ['Exit']
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

menu = {
    1: ['Yes please! Set another timer'],
    2: ['Exit']
}


def print_welcome():
    """
    Prints welcome message when program loads
    """
    print("\n\nWelcome to:\n\nTIME LORD\n\n")
    print("A night rate appliance time-shifting utility, designed to help ")
    print("you program your appliances to run when cheaper electricity ")
    print("night rates are in effect.\n")


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
            option = int(input('Enter your choice: \n'))
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
    passed as an argument.
    Credit - menu system adapted from:
    https://computinglearner.com/
    how-to-create-a-menu-for-a-python-console-application/
    """
    while (True):
        print("Please choose one of the following options:")
        for key in menu_dict.keys():
            print(key, '--', menu_dict[key][0])

        option = ''
        try:
            option = int(input('Enter your choice: \n'))
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
        duration = input("Enter the duration in HH:MM \n")
        if validate_time(duration):
            break

    return duration


def get_end_time():
    """
    Get optional preferred end time from user in 24hr clock format HH:MM
    """
    while True:
        end_time = input("Enter the time in HH:MM 24hr clock format "
                         "(i.e. 23:30 for 11.30pm) \n")
        # before time validation, check for empty field, return false if empty
        if not end_time:
            end_time = False
            break
        elif validate_time(end_time):
            break

    return end_time


def validate_time(time_str):
    """
    By passing required format string to datetime object's strptime method
    Credit:
    https://stackoverflow.com/questions/33076617/how-to-validate-time-format
    """
    try:
        datetime.strptime(time_str, "%H:%M")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def compute_result():
    """
    Calculate the start delay / end delay / start time / end time
    from user input & return the result to the user.
    """

    # convert window_start & window_end to date objects
    time_window_start = datetime.strptime(user_data['window_start'], "%H:%M")
    time_window_end = datetime.strptime(user_data['window_end'], "%H:%M")

    # add day to window_end if window_start is on previous day
    if time_window_start > time_window_end:
        time_window_end += timedelta(days=1)
    # get low rate window duration in hours
    window_duration = (time_window_end - time_window_start).total_seconds()
    window_duration /= 3600

    # cycle duration
    hours, mins = user_data['duration'].split(':')
    duration_in_minutes = (int(hours) * 60) + int(mins)

    # get end time into correct format for calculations if it's set
    # by adding todays date and making timezone aware
    today = date.today()
    if user_data['end_time']:
        hours, mins = user_data['end_time'].split(':')
        end_time = pytz.timezone(local_tz).localize(
            datetime.combine(today, time(int(hours), int(mins)))
        )
        #  if end time is in the past, add 24 hrs
        if end_time < now:
            end_time += timedelta(hours=24)

    # set time_window_start date object to today & make timezone aware
    hours, mins = user_data['window_start'].split(':')
    time_window_start = pytz.timezone(local_tz).localize(
        datetime.combine(today, time(int(hours), int(mins)))
    )

    # if time window end (time_start_window + time window duration) has passed
    # (less than current time), then add 24 hrs to time window start date
    tw_end = time_window_start + timedelta(hours=int(window_duration))
    if tw_end < now:
        time_window_start += timedelta(hours=24)
    # add time window duration to time_window_start to get (timezone aware)
    # time window end
    time_window_end = time_window_start + timedelta(hours=int(window_duration))

    print(RESULT_BANNER)
    print(
        f"Your electricity low rate runs from "
        f"{user_data['window_start']} to {user_data['window_end']}.\n"
    )

    # Start delay -----------------------
    if user_data['timer_index'] == 1:
        print("Timer input required: START DELAY\n——————————————\n")
        if user_data['end_time']:
            # end time specified, so...
            # calculate start delay from future preferred end time
            start_delay = (
                (end_time - timedelta(minutes=duration_in_minutes)) - now
            )

            print(
                f"To finish at {user_data['end_time']}, set the start delay on"
                f" your {user_data['appliance'].lower()} to "
                f"{int(start_delay.total_seconds() // 3600)} hours and "
                f"{int((start_delay.total_seconds()//60)%60)} minutes.\n\n"
            )
            # if end time is later than the time window end, suggest an
            # alternate earlier start delay
            if end_time > time_window_end:
                start_delay = (
                    (time_window_end - timedelta(minutes=duration_in_minutes))
                    - now
                )
                print(
                    f"WARNING! Your preferred end time falls outside of the "
                    f"selected low rate time window. \n"
                    f"To maximise savings, you could set the start delay to "
                    f"{int(start_delay.total_seconds() // 3600)} hours and "
                    f"{int((start_delay.total_seconds()//60)%60)} minutes "
                    f"instead.\n"
                    f"This would result in your "
                    f"{user_data['appliance'].lower()} finishing at "
                    f"{user_data['window_end']}.\n"
                )

        else:
            # no end time specified, so...
            start_delay = time_window_start - now
            # if start delay is negative, no delay required
            if int(start_delay.total_seconds()) <= 0:
                print(
                    f"No start delay required as the current time is within "
                    f"the selected low rate time window — you can start the "
                    f"{user_data['appliance'].lower()} right away.\n\n"
                )
            else:
                print(
                    f"Set the start delay on you "
                    f"{user_data['appliance'].lower()} to "
                    f"{int(start_delay.total_seconds() // 3600)} hours and "
                    f"{int((start_delay.total_seconds()//60)%60)} minutes.\n\n"
                )

    # End delay -----------------------
    if user_data['timer_index'] == 2:
        print("Timer input required: END DELAY\n——————————————\n")
        # end delay is number of hours from now until time window end
        # or end time if specified - check this first

        if user_data['end_time']:
            end_delay = end_time - now
            print(
                f"To finish at {user_data['end_time']}, set the end delay on "
                f"your {user_data['appliance'].lower()} to "
                f"{int(end_delay.total_seconds() // 3600)} hours and "
                f"{int((end_delay.total_seconds()//60)%60)} minutes.\n\n"
            )
        else:
            end_delay = time_window_end - now
            print(
                f"Set the end delay on your {user_data['appliance'].lower()} "
                f"to {int(end_delay.total_seconds() // 3600)} hours and "
                f"{int((end_delay.total_seconds()//60)%60)} minutes.\n\n"
            )

    # Start time -----------------------
    if user_data['timer_index'] == 3:
        print("Timer input required: START TIME\n——————————————\n")
        if user_data['end_time']:
            # User specified a preferred end time
            # Is there time for cycle to complete before specified end time
            if (end_time - timedelta(minutes=duration_in_minutes) > now):
                # yes there is, so start time can be set (to future time!)
                start_time = end_time - timedelta(minutes=duration_in_minutes)
                print(
                    f"To finish at {user_data['end_time']}, set the start "
                    f"time on your {user_data['appliance'].lower()} to "
                    f"{start_time.strftime('%H:%M')}.\n\n"
                )
            else:
                # not enough time to complete cycle before specified end time,
                # so start now & tell user when it'll actually finish
                adjusted_end_time = (
                    now + timedelta(minutes=duration_in_minutes)
                )
                print(
                    f"The selected cycle duration of {user_data['duration']} "
                    f"will cause your {user_data['appliance'].lower()} to "
                    f"finish after your preferred end time of "
                    f"{user_data['end_time']}, so it's best to start it right "
                    f"away.\n"
                    f"If you start it now, it'll finish at "
                    f"{adjusted_end_time.strftime('%H:%M')}.\n\n"
                )

            # Add warnings & suggestions if outside low rate time window
            # if end time is later than the time window end, suggest start time
            # of (time window end - cycle duration)
            if end_time > time_window_end:
                start_time = (
                    time_window_end - timedelta(minutes=duration_in_minutes)
                )
                print(
                    f"WARNING! Your preferred end time of "
                    f"{user_data['end_time']} falls outside of the selected "
                    f"low rate time window. \n"
                    f"To maximise savings, you could set the start time to "
                    f"{start_time.strftime('%H:%M')}\n"
                    f"which would result in your "
                    f"{user_data['appliance'].lower()} finishing at "
                    f"{user_data['window_end']}.\n"
                )
            # or if end time is before time window start, suggest starting at
            # time window start
            elif end_time < time_window_start:
                adjusted_end_time = (
                    time_window_start + timedelta(minutes=duration_in_minutes)
                )
                print(
                    f"WARNING! Your preferred end time of "
                    f"{user_data['end_time']} means that it'll finish before "
                    f"the low rate time window starts. \n"
                    f"To maximise savings, you could set the start time to "
                    f"{user_data['window_start']}\n"
                    f"which would result in your "
                    f"{user_data['appliance'].lower()} finishing at "
                    f"{adjusted_end_time.strftime('%H:%M')}.\n"
                )
        else:
            # No preferred end time specified, so...
            # set start time to time window end - cycle duration
            # Is there time for cycle to complete before time window end?
            if (
                time_window_end - timedelta(minutes=duration_in_minutes) > now
            ):
                # yes there is, so start time can be set (to future time!)
                start_time = (
                    time_window_end - timedelta(minutes=duration_in_minutes)
                )
                print(
                    f"Set the start time on your "
                    f"{user_data['appliance'].lower()} to "
                    f"{start_time.strftime('%H:%M')} and it'll be finished at "
                    f"{user_data['window_end']}.\n\n"
                )
            else:
                # not enough time to complete cycle before time window end time
                # so start now & tell user when it'll actually finish
                adjusted_end_time = (
                    now + timedelta(minutes=duration_in_minutes)
                )
                print(
                    f"The selected cycle duration of {user_data['duration']} "
                    f"will cause your {user_data['appliance'].lower()} "
                    f"to finish after the low rate time window ends, so it's "
                    f"best to start it right away.\n"
                    f"If you start it now, it'll be finished at "
                    f"{adjusted_end_time.strftime('%H:%M')}.\n\n"
                )

    # End time -----------------------
    if user_data['timer_index'] == 4:
        print("Timer input required: END TIME\n——————————————\n")
        # if earliest end time (window_start + duration) is less than
        # time_window_end: set end time to any time between earliest end time
        # and time_window_end otherwise just set it to time_window_end
        earliest_end_time = (
            time_window_start + timedelta(minutes=duration_in_minutes)
        )
        if user_data['end_time']:
            if time_window_start > end_time:
                end_time = end_time + timedelta(days=1)
        else:
            # just set it to time window end if no end time specified
            end_time = time_window_end

        if earliest_end_time < end_time:
            print(
                f"To get the most savings, set your "
                f"{user_data['appliance'].lower()} to finish anytime between "
                f"{earliest_end_time.strftime('%H:%M')} and "
                f"{end_time.strftime('%H:%M')}.\n\n")
        else:
            print(
                f"To get the most savings, just set your "
                f"{user_data['appliance'].lower()} to finish at "
                f"{end_time.strftime('%H:%M')}.\n\n"
            )


def main():
    """
    Run all program functions
    """
    print_welcome()

    while True:
        # Step #1:  Select cheap rate time window
        print("———————\nSTEP 1:\n———————\n")
        print(
            "First, tell me the times that your cheapest electricity rates "
            "apply. These are the most common time windows for lower night "
            "rate electricity offered by Irish energy providers in 2024.\n"
        )
        times_index = get_menu_index_from(times)
        user_data['window_start'] = times[times_index][1]
        user_data['window_end'] = times[times_index][2]
        print(f"\nSelected low rate time window: {times[times_index][0]}\n\n")

        # Step #2: Select appliance timer is being set on (for feedback only)
        print("———————\nSTEP 2:\n———————\n")
        appliance = set_appliance(appliances)
        user_data['appliance'] = appliance
        print(f"\nAppliance chosen: {appliance}\n\n")

        # Step #3: Select timer option (what we need to calculate)
        print("———————\nSTEP 3:\n———————\n")
        print(
            f"Now, tell me which of the following best describes the input"
            f" your {appliance.lower()} requires to set the time delay.\n"
        )
        timer_index = get_menu_index_from(timer_options)
        user_data['timer_index'] = timer_index
        print(f"\nSelected timer option: {timer_options[timer_index][0]}\n\n")

        # Step #4: Get cycle duration / running / cooking time
        print("———————\nSTEP 4:\n———————\n")
        duration = get_time_duration(appliance)
        user_data['duration'] = duration

        hour, min = duration.split(":")
        print(
            f"\nRunning time will be: {hour} hours and {min} minutes.\n\n"
        )

        # Step #5: Set preferred time for appliance to finish
        # Input required if user selected end time (option 4) in Step #3
        print("———————\nSTEP 5:\n———————\n")
        if timer_index == 4:
            print(
                f"Lastly, you selected end time (option 4) as the timer input "
                f"for your {appliance.lower()}, so please enter that here. \n"
            )
        else:
            print(
                f"Lastly, if you'd like the {appliance.lower()} to finish at "
                f"a specific time, enter it here or just leave it blank & hit "
                f"enter. \n"
            )
        end_time = get_end_time()
        user_data['end_time'] = end_time
        if end_time:
            print(
                f"\nPerfect! You'd like the {appliance.lower()} to finish at "
                f"{end_time}. \n\n"
            )
        else:
            print(
                f"\n Great! We don't need to set your {appliance.lower()} to "
                f"finish at a specific time. \n\n"
            )

        # Step #6 - compute & return result to the user
        compute_result()

        # Step #7: Set another timer or Quit
        print("Would you like to set another timer?\n")
        if get_menu_index_from(menu):
            print("\n\n!!! Yay, lets set another timer!!! \n\n")


main()
