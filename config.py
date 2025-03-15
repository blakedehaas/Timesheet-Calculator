#!/usr/bin/env python3
"""
Configuration Generator for the Timesheet Application

This file lets you configure your timesheet schedule for multiple projects.
For example, you might allocate:
  - 48 hours per week to "Operations Software" (with multiple speedtypes)
    on Monday, Wednesday, and Friday.
  - 32 hours per week to "Space Physics" (with 100% allocation to "Space Physics")
    on Tuesday and Thursday.

You also configure your total paid time off (PTO) in hours.
In this updated version, PTO is subtracted equally from each project's total hours.
For instance, if you have 8 hours of PTO then each project will have 4 hours subtracted.
Additionally, you specify the number of weeks to schedule.
For example, "weeks": 2 creates a schedule for 10 work days (2 weeks x 5 days).

Please review the parameters below and edit them as needed. Running this script
will create a file named "config.json" in the same directory.
"""

import json

# --- PROJECT CONFIGURATIONS ---
# Each key in the "projects" dictionary is a project name.
# For each project, set the "total_hours" for that project and provide a
# "speedtype_percentage_distribution" dictionary mapping each task (or speedtype)
# to its percentage share. The percentages for each project should sum to 100.
projects = {
    "Operations Software": {
        "total_hours": 48,
        "speedtype_percentage_distribution": {
            "TSIS-1 Follow On Ground Systems 12345": 25,
            "IMAP SOC POC SW and SYS Devl 12345": 25,
            "MMS POC Software S 12345": 13,
            "EMM Extended Mission Mission Ops Labor 12345": 13,
            "All Allowable; Subclass: NSOSW 12345": 13,
            "MO GOLD 12345": 8,
            "SDO EVE Instrument O 12345": 3
        }
    },
    "Space Physics": {
        "total_hours": 32,
        "speedtype_percentage_distribution": {
            "Quantifying The Impa 12345": 100
        }
    }
}

# --- WORK SCHEDULE ---
# Map each weekday to the project you will work on that day.
# In the example below, Mondays, Wednesdays, and Fridays are assigned to
# "Operations Software" while Tuesdays and Thursdays are dedicated to "Space Physics".
work_schedule = {
    "Monday": "Operations Software",
    "Tuesday": "Space Physics",
    "Wednesday": "Operations Software",
    "Thursday": "Space Physics",
    "Friday": "Operations Software"
}

# --- WORKDAY TIMING ---
# Set your workday timings. Times should be in "H:MM AM/PM" format.
workday_start_time = "8:00 AM"
lunch_start_time = "12:00 PM"
lunch_end_time = "1:00 PM"
workday_end_time = "5:00 PM"

# --- PAID TIME OFF ---
# Specify your total paid time off (PTO) in hours.
# PTO is subtracted equally from each project's total hours.
paid_time_off = 0

# --- SCHEDULING PERIOD ---
# Specify the number of weeks for the schedule.
# For example, "weeks": 2 creates a schedule for 10 work days (Monday-Friday for 2 weeks).
weeks = 2

# --- AGGREGATE CONFIGURATION ---
config = {
    "projects": projects,
    "work_schedule": work_schedule,
    "weeks": weeks,
    "workday_start_time": workday_start_time,
    "lunch_start_time": lunch_start_time,
    "lunch_end_time": lunch_end_time,
    "workday_end_time": workday_end_time,
    "paid_time_off": paid_time_off
}

with open("config.json", "w") as f:
    json.dump(config, f, indent=2)

print("Configuration file 'config.json' has been generated. Please review and adjust it as needed.")
