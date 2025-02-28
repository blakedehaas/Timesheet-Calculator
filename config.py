# config.py

# This configuration file is used to set up your timesheet distribution.
# The project calculates the distribution of total work hours among different speedtypes
# based on their respective percentages. Follow the instructions below to configure
# your timesheet.

# 1. Total Hours
#    Define the total number of hours to be distributed among all the speedtypes.
#    This should be the total number of hours you have worked for your timesheet.
total_hours = 72

# 2. Speedtype Percentage Distribution
#    This dictionary contains the different speedtypes and their respective
#    percentages of the total hours. Each key is a string representing a speedtype, and
#    each value is the percentage of the total hours to be allocated to that task.
#    Ensure that the sum of all percentages equals 100.
speedtype_percentage_distribution = {
    "Phase C F OPS": 20,
    "Follow On Ground Systems": 80,
}

# 3. Length of Workday
#    Specify the length of your workday in hours. This will be used to calculate the
#    number of full workdays and the remainder hours for each task.
length_of_workday = 8



# Example:
# If the total number of hours you worked for this timesheet is 72, then set total_hours to 72 
# If the length of your workday is 8 hours, then set length_of_workday to 8
# If you are distributing your hours to the speedtype "Phase C F OPS" at 20% and "Follow On Ground Systems" at 80%,
# then add the following entries to the speedtype_percentage_distribution dictionary:
# "Phase C F OPS": 20,
# "Follow On Ground Systems": 80

# After configuring the timesheet, run the TimesheetCalculator.py script to calculate the distribution of hours using this command:
# python3 TimesheetCalculator.py

# Your speedtype will be distributed as follows:
# Total Hours: 72
# Phase C OPS: 14 hours and 24 minutes (20%)
#     -> 1 full 8-hour workdays, 6 hours and 24 minutes remainder
# Follow On Ground Systems: 57 hours and 36 minutes (80%)
#     -> 7 full 8-hour workdays, 1 hours and 36 minutes remainder
