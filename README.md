# Time Lord

Time Lord is a little python console application designed to help save money by making it easier to time shift usage of  energy intensive appliances to avail of lower night time rate electricity rates. 

[Run the live deployed app here](https://time-lord-bristlebird-f6d274971209.herokuapp.com/)

Many modern household appliances such as dishwashers, washing machines, ovens, bread-makers, yogurt makers and so forth,  come with a time delay function, allowing you to set them to run at a time that best suits your lifestyle, daily routine and budget. Most electricity supply companies offer night rate and smart meter plans that have lower rates at certain times, so you can save money by time-shifting your energy intensive appliances so that use power charged at the lower rate. 

Attaining any cost-saving from these kind of plans requires a good handle on how to time shift your appliances. Here lies...

## The problem

Unless all your appliances are made by the same high end manufacturer, it's more than likely that their time shifting functions will behave differently and require different timing inputs to work at the optimal time. Working out the different time offsets for all these appliances at the end of long day can become tiresome and confusing!

Luckily... Time lord is here to help!

In some cases you'll want a cycle to finish at a certain time: bread, for example, should be taken out of a bread maker as soon as it's ready as it goes soggy if left in for long after — this usually means as soon as you get up in the morning. In other cases, you just want the appliance to start when the cheap night rate kicks in, or at least to be finished by the time the more expensive day rate kicks in.

In most cases, an appliance will have several different cycles of varying durations, and turn themselves off automatically when the cycle is complete, so you'll usually need to know what the cycle duration is — this is usually displayed on the appliance when the cycle is selected. Sometimes you'll have to set your own 'cooking time / duration' in addition to setting a start time or onset delay.

## Pre project planning

The objective is to run appliances at cheaper night rate & to help you set your appliance timers so that they run at the best and most cost effective time. Based on your low rate time window, the appliance's cycle duration, when you'd like it to end, Time Lord will do all the tricky time based maths and tell what the best time or value to set the timer with, depending on the kind of input required.

## User flow

1. User is asked to chose their night rate hours (11pm - 8am / 12am - 9am / 1am - 8am / 2am - 9am) — these may differ depending on the supplier.
2. User is asked to select appliance from list (washing machine, dishwasher, bread oven, cooker, yogurt maker)
3. User is asked to how their appliance timer works to determine what input is required — choose  from list of options... i.e. Which of the following inputs does your appliance require to set the time delay? 
4. User is asked what the programme duration / cooking time?
5. Do you need or would you like the appliance to finish at a specific time? i.e. you might like bread to finish baking at 6.30am 


### Timer Input Options
1. Start delay (hours until cycle starts)
	- request duration
	- night rate end time - duration = latest start time
	- if cheap boost && (cheap boost start time + duration < night rate end time) start at cheap boost start time, else start at night rate end time - duration
2. Delay end (hours until cycle ends)
3. Start time 
4. End time
5. Start delay + end time (Bosch Oven)



### Start Delay




Does it need to end at a specific time?

## Future features
 - Display potential cost savings per program, per week / month / year based on actual cost per Kw/h or based on current average rates.
 - Option to save the settings for each appliance in a Google sheet so it can be quickly recalled next time. These settings would be unique to each individual to it would also require secure user authentication. 
 - Code refactors: create a separate compute output function for each timer input option.
 - Tell user if appliance's complete cycle falls within low rate window, if it doesn't tell them how much falls outside.

## Technologies Used
1. Python — for the main application logic
2. Heroku — for app deplyment & hosting
3. Git — for version control
3. Github — for code storage / repository
4. Gitpod — IDE used to write the code
5. Visual Studio Code for Mac — IDE also used to write code (connected to Gitpod Workspace)
5. [Code Institute's Python essentials template](https://github.com/Code-Institute-Org/python-essentials-template)
6. [Macdown](https://macdown.uranusjr.com/) — open source Markdown editor for macOS, used to create this README

##  Deployment Procedure
This python was deployed on Heroku — [view the live app here](https://time-lord-bristlebird-f6d274971209.herokuapp.com/). 

If you want to fork this project and deploy this app on Heroku, you can follow these 10 steps:

1. Ensure that the project requirements.txt has been generated by running the following command in the terminal from the application root folder `pip3 freeze > requirements.txt` (some dependencies were installed that were not required in the end, such as gspread and google-auth, so these could be ommitted from the requirements.txt file).
2. If you don't already have one, set up a free account [here](https://signup.heroku.com/).
3.  When creating the account, you can choose the country you're in, set Python as the primary development language, set your password & agree to their terms of service.
4. When you've created your account & logged in, hit the 'Create new app' button in the dashboard.
5. Give the app a unique name & select your region & hit 'Create app' button.
6. Once the app is created, hit the 'Settings' tab, hit 'Add buildpack', select Python & save changes, then hit 'Add buildpack' again, select Nodejs & save changes. Ensure Python is first in the list and Nodejs second by re-ordering if necessary.
7. Next hit the 'Deploy' tab and select 'Github' in the Deployment method section, then hit the 'Connect to Github' button. You'll need to be logged in to Github to authorise this connection.
8. Once Github is connected, enter the repository name in the 'Search for a repository to connect to' field, hit the 'search' button then hit the 'Connect' button for the chosen repository.
9. You can then either enable automatic deployment or deploy manually — to deploy manually, select the branch to deploy (probably 'main'), the hit the 'Deploy branch' button.
10. Once the app has been successfully deployed you can click the 'View' button to open the deployed app in your browser.

## Testing

### Manual Tests

| Test | Result |
| -- | -- |
| User prompted with step 1 menu choice after intro message | Pass |

### Error handling tests

| Test | Result |
| -- | -- |
| Menu selection: User enters empty string | Pass |
| Menu selection: User enters number out of range | Pass |
| Menu selection: User enters any random letters | Pass |

### Pep8 Code Linter
[Code Institute's Pep8 Python Linter](https://pep8ci.herokuapp.com/) was used to correctly format python code and ensure it was free from errors:
![](assets/docs/linter.png)

## Credits
 - [How to create a menu for a python console application](https://computinglearner.com/how-to-create-a-menu-for-a-python-console-application/) 
 - [Time input validation in python](https://stackoverflow.com/questions/33076617/how-to-validate-time-format)
 - [Get duration between 2 python datetime objects](https://stackoverflow.com/questions/43305577/python-calculate-the-difference-between-two-datetime-time-objects) 
 - [Alan Bushell's Blackjack project Readme structure](https://github.com/Alan-Bushell/blackjack/)

    

