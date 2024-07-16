import gspread
from google.oauth2.service_account import Credentials

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


def main():
    """
    Run all program functions
    """
    print_welcome()


main()
