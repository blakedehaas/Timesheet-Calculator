#!/usr/bin/env python3
"""
Configuration Generator for the Timesheet Application

This file lets you configure your timesheet schedule for multiple projects.

Key Configuration Areas:
1.  Project Details: Define each project, its total planned hours (work + PTO),
    and how work time (excluding PTO) is distributed among specific tasks/speedtypes.
    The speedtype percentages for each project must sum to 100.
2.  Workday Timings: Set start and end times for each day.
3.  Paid Time Off (PTO):
    - Set the total PTO hours for the entire period.
    - Optionally, define how these PTO hours are distributed among projects using
      `pto_percentage_distribution`. The percentages here must sum to 100 if provided.
    - If `pto_percentage_distribution` is not provided or is empty, PTO will be
      distributed equally among all projects.
4.  Scheduling Period: Specify the dates that should be covered in the schedule.

Running this script will create or overwrite a file named "config.json" in the same directory.
"""

import json
from datetime import datetime, date

# --- PROJECT CONFIGURATIONS ---
# Define projects, their total hours, and work task distribution.
# The total hours from all projects will be distributed evenly across the schedule.
projects = {
    "Operations Software": {
        "total_hours": 67,
        "speedtype_percentage_distribution":
        {
            "Speedtype 1": 37,
            "Speedtype 2": 21,
            "Speedtype 3": 21,
            "Speedtype 4": 14,
            "Speedtype 5": 7
        }
    },
    "TSIS-1": {
        "total_hours": 5,
        "speedtype_percentage_distribution":
        {
            "Speedtype 1": 100
        }
    },
    "SmallSAT": {
        "total_hours": 8,
        "speedtype_percentage_distribution":
        {
            "Speedtype 1": 100
        }
    },
    "Sick Hourly": {
        "total_hours": 0,
        "speedtype_percentage_distribution":
        {
            "Sick Hourly": 100
        }
    }
}

# --- WORKDAY TIMING ---
# Times should be in "H:MM AM/PM" format.
workday_start_time = "8:00 AM"
workday_end_time = "12:00 PM"

# --- PAID TIME OFF (PTO) ---
paid_time_off = 0  # total PTO hours for the entire period

# PTO distribution per project (optional). Keys must match 'projects'. Percentages must sum to 100.
# If left empty ({}), this script will distribute PTO equally among all projects.
pto_percentage_distribution = {
    "Operations Software": 100,
    "SmallSAT": 0
}

# --- SCHEDULING PERIOD ---
start_date = "2026-02-01"  # Format: YYYY-MM-DD
end_date = "2026-02-28"    # Format: YYYY-MM-DD
work_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

# --- INTERNAL HELPERS ---

_VALID_DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def _parse_iso_date(s: str) -> date:
    return date.fromisoformat(s)

def _parse_time_12h(s: str) -> datetime:
    # returns a datetime with dummy date; only time component is used
    return datetime.strptime(s, "%I:%M %p")

def _resolve_pto_distribution(projects_dict, pto_dist):
    """
    If pto_dist is falsy (None or {}), return an equal distribution among projects (summing to 100).
    Otherwise return pto_dist unchanged.
    """
    if not pto_dist:
        n = len(projects_dict)
        if n == 0:
            return {}
        base = 100 // n
        remainder = 100 - base * n
        projects_list = list(projects_dict.keys())
        eq = {p: base for p in projects_list}
        # Distribute the remaining 1% chunks to the first 'remainder' projects
        for i in range(remainder):
            eq[projects_list[i]] += 1
        return eq
    return pto_dist

# --- VALIDATION ---
try:
    # Validate Speedtype Percentages
    for name, project_cfg in projects.items():
        percentages = project_cfg.get("speedtype_percentage_distribution", {})
        total_percentage = sum(percentages.values())
        if not abs(total_percentage - 100.0) < 0.01:
            print(f"WARNING in config.py: Speedtype percentages for project '{name}' sum to {total_percentage}, not 100.")

    # Validate scheduling period
    try:
        sd = _parse_iso_date(start_date)
        ed = _parse_iso_date(end_date)
        if sd > ed:
            print(f"WARNING in config.py: start_date {start_date} is after end_date {end_date}.")
    except ValueError as ve:
        print(f"WARNING in config.py: Invalid date format. Use YYYY-MM-DD. Details: {ve}")

    # Validate workday names
    invalid_days = [d for d in work_days if d not in _VALID_DAY_NAMES]
    if invalid_days:
        print(f"WARNING in config.py: Invalid day names in work_days: {invalid_days}. "
              f"Use one of: {_VALID_DAY_NAMES}")

    # Validate workday times (start before end)
    try:
        t_start = _parse_time_12h(workday_start_time)
        t_end = _parse_time_12h(workday_end_time)
        if t_end <= t_start:
            print(f"WARNING in config.py: workday_end_time ('{workday_end_time}') "
                  f"is not after workday_start_time ('{workday_start_time}').")
    except ValueError as ve:
        print(f"WARNING in config.py: Invalid time format. Use 'H:MM AM/PM'. Details: {ve}")

    # Validate / resolve PTO Percentages
    resolved_pto = _resolve_pto_distribution(projects, pto_percentage_distribution)
    if resolved_pto:
        total_pto_percentage = sum(resolved_pto.values())
        if not abs(total_pto_percentage - 100.0) < 0.01:
            print(f"WARNING in config.py: PTO distribution percentages sum to {total_pto_percentage}, not 100.")
        # Check if PTO projects exist in main projects list
        for pto_proj_name in resolved_pto:
            if pto_proj_name not in projects:
                print(f"WARNING in config.py: Project '{pto_proj_name}' listed in 'pto_percentage_distribution' "
                      f"is not defined in 'projects'.")
    else:
        # With no projects, PTO split can't be made
        resolved_pto = {}

except Exception as e:
    print(f"Error during basic configuration validation in config.py: {e}")
    # Fall back to original pto if something above failed
    resolved_pto = pto_percentage_distribution or {}

# --- AGGREGATE CONFIGURATION ---
# Consolidate everything that the application needs.
config = {
    "projects": projects,
    "workday_start_time": workday_start_time,
    "workday_end_time": workday_end_time,
    "paid_time_off": paid_time_off,
    "pto_percentage_distribution": resolved_pto,  # use resolved (equal if empty)
    "start_date": start_date,
    "end_date": end_date,
    "work_days": work_days
}

# --- FILE GENERATION ---
try:
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    print("Configuration file 'config.json' has been generated/updated. Please review it.")
except IOError as e:
    print(f"Error writing configuration file 'config.json': {e}")