# TimesheetCalculator.py

# This script calculates the distribution of total work hours among different tasks
# based on their respective percentages defined in the config.py file. It also calculates
# the number of full workdays and the remainder hours for each task.

import config

def calculate_distribution(total_hours, distribution, workday_length):
    """
    Calculates the distribution of total hours among different tasks.

    Args:
        total_hours (int): The total number of hours to be distributed.
        distribution (dict): A dictionary where the key is the task name (speedtype)
                             and the value is the percentage of total hours for that task.
        workday_length (int): The length of a workday in hours.

    Returns:
        dict: A dictionary where the key is the task name and the value is a tuple containing:
              - Total hours allocated to the task
              - Total minutes allocated to the task
              - Percentage of total hours for the task
              - Number of full workdays
              - Remainder hours
              - Remainder minutes
    """
    results = {}
    total_minutes = total_hours * 60
    for speedtype, percentage in distribution.items():
        allocated_minutes = total_minutes * (percentage / 100)
        hours = int(allocated_minutes // 60)
        minutes = int(allocated_minutes % 60)
        
        # Calculate the number of full workdays and remainder
        full_workdays = hours // workday_length
        remainder_hours = hours % workday_length
        
        results[speedtype] = (hours, minutes, percentage, full_workdays, remainder_hours, minutes)
    return results

def print_distribution(results, total_hours, workday_length):
    """
    Prints the distribution of hours and workdays for each task.

    Args:
        results (dict): A dictionary containing the calculated distribution for each task.
        total_hours (int): The total number of hours to be distributed.
        workday_length (int): The length of a workday in hours.
    """
    print(f"Total Hours: {total_hours}")
    for speedtype, (hours, minutes, percentage, full_workdays, remainder_hours, remainder_minutes) in results.items():
        print(f"{speedtype}: {hours} hours and {minutes} minutes ({percentage}%)")
        print(f"    -> {full_workdays} full {workday_length}-hour workdays, {remainder_hours} hours and {remainder_minutes} minutes remainder")

def main():
    """
    Main function that retrieves configuration, calculates distribution, and prints the results.
    """
    total_hours = config.total_hours
    distribution = config.speedtype_percentage_distribution
    workday_length = config.length_of_workday
    results = calculate_distribution(total_hours, distribution, workday_length)
    print_distribution(results, total_hours, workday_length)

if __name__ == "__main__":
    main()
