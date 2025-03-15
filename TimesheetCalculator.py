#!/usr/bin/env python3
import json
import datetime
import os
import sys
import argparse
import subprocess
import logging

# Set up logging.
logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s: %(message)s")

class ConfigurationError(Exception):
    """Custom exception for configuration errors."""
    pass

class Configuration:
    """
    Loads and validates the JSON configuration.
    
    Expected keys:
      - projects: dict mapping project names to {total_hours, speedtype_percentage_distribution}
      - work_schedule: dict mapping weekdays (e.g. "Monday") to project names.
      - weeks: number of weeks to schedule (e.g. 2 creates 10 work days).
      - workday_start_time, lunch_start_time, lunch_end_time, workday_end_time: time strings.
      - paid_time_off: a number (global PTO hours).
    """
    def __init__(self, config_path):
        self.config_path = config_path
        self.data = self._load_config()
        self._validate_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            raise ConfigurationError(f"Configuration file '{self.config_path}' not found.")
        try:
            with open(self.config_path, "r") as f:
                data = json.load(f)
            logger.debug(f"Configuration loaded: {data}")
            return data
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Error parsing JSON: {e}")

    def _validate_config(self):
        required_keys = [
            "projects", "work_schedule", "weeks",
            "workday_start_time", "lunch_start_time",
            "lunch_end_time", "workday_end_time", "paid_time_off"
        ]
        missing = [key for key in required_keys if key not in self.data]
        if missing:
            raise ConfigurationError(f"Missing configuration keys: {', '.join(missing)}")

    @property
    def projects(self):
        return self.data["projects"]

    @property
    def work_schedule(self):
        return self.data["work_schedule"]

    @property
    def weeks(self):
        return self.data["weeks"]

    @property
    def workday_start_time(self):
        return self.data["workday_start_time"]

    @property
    def lunch_start_time(self):
        return self.data["lunch_start_time"]

    @property
    def lunch_end_time(self):
        return self.data["lunch_end_time"]

    @property
    def workday_end_time(self):
        return self.data["workday_end_time"]

    @property
    def paid_time_off(self):
        return self.data["paid_time_off"]

class DistributionCalculator:
    """
    Calculates allocated work minutes for each task within a project.
    
    The effective work hours (for non-PTO tasks) are provided.
    Returns, for each task in the speedtype distribution, the allocated minutes.
    """
    def __init__(self, effective_work_hours, speedtype_distribution):
        self.effective_work_hours = effective_work_hours  # in hours
        self.speedtype_distribution = speedtype_distribution

    def calculate(self):
        total_minutes = self.effective_work_hours * 60
        results = {}
        for task, percentage in self.speedtype_distribution.items():
            allocated_minutes = total_minutes * (percentage / 100)
            hours = int(allocated_minutes // 60)
            minutes = int(allocated_minutes % 60)
            results[task] = (hours, minutes, percentage, allocated_minutes)
            logger.debug(f"Task '{task}': {hours}h {minutes}m ({percentage}%), allocated {allocated_minutes} minutes.")
        return results

class TimesheetGenerator:
    """
    Generates a single day's schedule based on fixed workday timings and the list of tasks.
    
    The generate_day() method schedules tasks in order over the morning and afternoon segments.
    (Lunch is fixed.) This method now treats "Paid Time Off" as just another task.
    """
    def __init__(self, config):
        self.config = config
        self.workday_start = self._parse_time(self.config.workday_start_time)
        self.lunch_start = self._parse_time(self.config.lunch_start_time)
        self.lunch_end = self._parse_time(self.config.lunch_end_time)
        self.workday_end = self._parse_time(self.config.workday_end_time)
        self.default_morning = self.lunch_start - self.workday_start
        self.default_afternoon = self.workday_end - self.lunch_end
        # Total effective day minutes (excluding lunch).
        self.effective_day_minutes = self.default_morning + self.default_afternoon
        logger.debug(f"Workday timings: start={self.workday_start}, lunch_start={self.lunch_start}, "
                     f"lunch_end={self.lunch_end}, end={self.workday_end}, effective_minutes={self.effective_day_minutes}")

    def _parse_time(self, time_str):
        try:
            dt = datetime.datetime.strptime(time_str, "%I:%M %p")
            return dt.hour * 60 + dt.minute
        except ValueError as e:
            raise ValueError(f"Time format error for '{time_str}': {e}")

    def _format_time(self, minutes_since_midnight):
        hour = minutes_since_midnight // 60
        minute = minutes_since_midnight % 60
        period = "AM" if hour < 12 or hour == 24 else "PM"
        hour_mod = hour % 12
        if hour_mod == 0:
            hour_mod = 12
        return f"{hour_mod}:{minute:02d} {period}"

    def generate_day(self, day_name, tasks, extra_pto=0):
        """
        Generates the schedule for one day.
        
        Args:
            day_name (str): Weekday name.
            tasks (list): List of [task_name, allocated_minutes] pairs.
            extra_pto (int): (Not used; PTO is now a task.)
        
        Returns:
            list of strings representing the day's schedule.
        """
        lines = []
        lines.append(f"{day_name}:")
        current_time = self.workday_start

        # --- Morning Segment ---
        morning_remaining = self.lunch_start - current_time
        while morning_remaining > 0 and tasks:
            task_name, task_minutes = tasks[0]
            if task_minutes <= morning_remaining:
                start_time = current_time
                end_time = current_time + task_minutes
                # If end_time is within 1 minute of lunch_start, force it to match.
                if abs(end_time - self.lunch_start) <= 1:
                    end_time = self.lunch_start
                lines.append(f"{self._format_time(start_time)} - {self._format_time(end_time)}: {task_name}")
                current_time = end_time
                tasks.pop(0)
            else:
                start_time = current_time
                end_time = current_time + morning_remaining
                if abs(end_time - self.lunch_start) <= 1:
                    end_time = self.lunch_start
                lines.append(f"{self._format_time(start_time)} - {self._format_time(end_time)}: {task_name}")
                tasks[0][1] -= morning_remaining
                current_time = self.lunch_start
            morning_remaining = max(0, self.lunch_start - current_time)

        # --- Lunch Break ---
        lines.append(f"{self.config.lunch_start_time} - {self.config.lunch_end_time}: Lunch")

        # --- Afternoon Segment ---
        current_time = self.lunch_end
        afternoon_remaining = self.workday_end - self.lunch_end
        while afternoon_remaining > 0 and tasks:
            task_name, task_minutes = tasks[0]
            if task_minutes <= afternoon_remaining:
                start_time = current_time
                end_time = current_time + task_minutes
                if abs(end_time - self.workday_end) <= 1:
                    end_time = self.workday_end
                lines.append(f"{self._format_time(start_time)} - {self._format_time(end_time)}: {task_name}")
                current_time = end_time
                tasks.pop(0)
            else:
                start_time = current_time
                end_time = current_time + afternoon_remaining
                if abs(end_time - self.workday_end) <= 1:
                    end_time = self.workday_end
                lines.append(f"{self._format_time(start_time)} - {self._format_time(end_time)}: {task_name}")
                tasks[0][1] -= afternoon_remaining
                current_time = self.workday_end
            afternoon_remaining = max(0, self.workday_end - current_time)

        return lines

class TimesheetApp:
    """
    Main application class tying configuration, task allocation, and daily scheduling together.
    
    This version subtracts the global PTO equally from each project's total hours by adding a
    "Paid Time Off" task to each project. The schedule is then produced for a fixed number of workdays.
    """
    def __init__(self, config_path):
        self.config = Configuration(config_path)
        self.generator = TimesheetGenerator(self.config)
        self.project_tasks = {}
        self._initialize_projects()

    def _initialize_projects(self):
        """
        For each project, compute the effective work hours by subtracting an equal share of the global PTO,
        allocate tasks using the provided speedtype percentages on the remaining work hours, and then add
        a "Paid Time Off" task with the allocated PTO minutes.
        """
        num_projects = len(self.config.projects)
        pto_per_project = self.config.paid_time_off / num_projects if self.config.paid_time_off > 0 else 0  # in hours
        logger.debug(f"Global PTO: {self.config.paid_time_off} hours; Each project gets {pto_per_project} PTO hours.")
        for project, cfg in self.config.projects.items():
            total_hours = cfg["total_hours"]
            work_hours = total_hours - pto_per_project
            if work_hours < 0:
                raise ValueError(f"Effective work hours for project '{project}' cannot be negative.")
            speed_distribution = cfg["speedtype_percentage_distribution"]
            tasks = []
            # Allocate work tasks based on the effective work hours.
            for task, percentage in speed_distribution.items():
                allocated = int(work_hours * 60 * (percentage / 100))
                tasks.append([task, allocated])
                logger.debug(f"Project '{project}': Task '{task}' allocated {allocated} minutes.")
            # Add the PTO task only if there are PTO hours.
            if pto_per_project > 0:
                tasks.append(["Paid Time Off", int(pto_per_project * 60)])
            self.project_tasks[project] = tasks
            total_alloc = sum(t[1] for t in tasks)
            logger.info(f"Project '{project}' effective hours: {work_hours} work + {pto_per_project} PTO = {total_hours} total hours (total minutes: {total_alloc}).")

    def run(self):
        """
        Runs the scheduling loop for a fixed number of workdays (weeks * 5).
        For each day (cycling Monday–Friday), the app uses the project scheduled for that day
        and generates the day's schedule from its task list.
        """
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        total_work_days = self.config.weeks * len(days_order)
        schedule_output = []
        # Debug: tally total allocated minutes.
        total_allocated = sum(
            sum(task[1] for task in tasks) for tasks in self.project_tasks.values()
        )
        logger.info(f"Total effective minutes allocated across projects: {total_allocated}")
        for day in range(total_work_days):
            day_name = days_order[day % len(days_order)]
            project = self.config.work_schedule.get(day_name)
            schedule_output.append(f"\nDay {day + 1} ({day_name} - {project}):")
            tasks = self.project_tasks.get(project, [])
            # PTO is scheduled as a task.
            day_lines = self.generator.generate_day(day_name, tasks, extra_pto=0)
            schedule_output.extend(day_lines)
        # Final check: All tasks should be scheduled completely.
        for project, tasks in self.project_tasks.items():
            assert not tasks, f"Tasks remain unscheduled for project '{project}': {tasks}"
        print("\nPopulated Timesheet:")
        for line in schedule_output:
            print(line)

def main():
    parser = argparse.ArgumentParser(description="Timesheet Application with PTO as a Speedtype")
    parser.add_argument("--config", type=str, default="config.json",
                        help="Path to configuration JSON file")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Regenerate configuration by running config.py.
    print("Regenerating configuration file by running config.py...")
    try:
        subprocess.run(["python", "config.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error generating configuration: {e}")
        sys.exit(1)

    try:
        app = TimesheetApp(args.config)
        app.run()
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
