# Timesheet Calculator

The Timesheet Calculator is a Python-based application designed to help you distribute your work hours across multiple projects and tasks. With a simple configuration file, you can specify your work schedule, project allocations, and paid time off (PTO). The application then generates a detailed, day-by-day timesheet that you can use to track your work.

This guide provides step-by-step instructions to set up a new environment on Windows, macOS, or Linux, configure the application, run the program, and use the test suite. For personalized guidance, you may share this README with your preferred AI assistant.

---

## Overview

The Timesheet Calculator helps you:
- Configure multiple projects with specific work hours and task distributions.
- Specify a work schedule (e.g., which project you work on each weekday).
- Set your workday timings (start time, lunch period, and end time).
- Define your total paid time off (PTO), which is subtracted equally from each project.
- Generate a detailed, day-by-day timesheet over a set number of weeks.

---

## Setup and Tools

### 1. Install Python 3.7 or Later

- **Windows, macOS, or Linux:**  
  Download Python from [python.org](https://www.python.org/downloads/).  
  Run the installer (or use your package manager on macOS/Linux) and make sure to add Python to your system PATH when prompted.

### 2. Choose an IDE or Code Editor

You have a choice between two recommended environments:

- **Cursor:**  
  Cursor is a modern IDE built on VS Code that integrates AI assistance into your workflow. It provides real-time code help, debugging support, and the ability to ask AI questions about the code—all within the IDE.  
  Download Cursor from [Cursor](https://www.cursor.so/).

- **Visual Studio Code (VS Code):**  
  VS Code is a free and powerful code editor.  
  - **Windows:** Download from [Visual Studio Code](https://code.visualstudio.com/).  
  - **macOS:** Download from [Visual Studio Code](https://code.visualstudio.com/) or install via Homebrew using `brew install --cask visual-studio-code`.  
  - **Linux:** Download from [Visual Studio Code](https://code.visualstudio.com/Download) or install via your distribution’s package manager (e.g., `sudo snap install --classic code` on Ubuntu).  
  After installation, open VS Code and install the Python extension by searching for "Python" by Microsoft in the Extensions view.

### 3. Clone the Repository

1. **Install Git:**
   - **Windows:** Download and install Git from [git-scm.com](https://git-scm.com/download/win).
   - **macOS:** Install Git via Homebrew with:
     ```
     brew install git
     ```
     or download from [git-scm.com](https://git-scm.com/download/mac).
   - **Linux:** On Ubuntu/Debian, run:
     ```
     sudo apt update
     sudo apt install git
     ```

2. **Set Up an SSH Key (if needed):**
   - Open a terminal.
   - Generate a new SSH key:
     ```
     ssh-keygen -t ed25519 -C "your_email@example.com"
     ```
     (If Ed25519 is not supported, use RSA:
     ```
     ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
     ```
     )
   - Press Enter to accept the default location and optionally enter a passphrase.
   - Start the SSH agent:
     ```
     eval "$(ssh-agent -s)"
     ```
   - Add your SSH key:
     ```
     ssh-add ~/.ssh/id_ed25519
     ```
   - Copy your SSH public key to your clipboard:
     - **Windows (Git Bash):**
       ```
       clip < ~/.ssh/id_ed25519.pub
       ```
     - **macOS:**
       ```
       pbcopy < ~/.ssh/id_ed25519.pub
       ```
     - **Linux:** (with xclip installed)
       ```
       xclip -sel clip < ~/.ssh/id_ed25519.pub
       ```
   - Log in to your GitHub account, navigate to [GitHub SSH Keys](https://github.com/settings/keys), and add your public key.

3. **Clone the Repository:**
   - Open a terminal or command prompt.
   - Run:
     ```
     git clone git@github.com:blakedehaas/Timesheet-Calculator.git
     ```
   - Navigate into the repository folder:
     ```
     cd Timesheet-Calculator
     ```
   - Open this folder in your chosen IDE.

---

## Configuration Setup

1. **Edit the Configuration Script:**
   - Open the `config.py` file in your IDE.
   - Adjust the following sections as needed:
     - **Project Configurations:** Set the total hours and task percentage distribution for each project.
     - **Work Schedule:** Map each weekday to a project.
     - **Workday Timing:** Set your workday start time, lunch start and end times, and end time (format: "H:MM AM/PM").
     - **Paid Time Off (PTO):** Specify your total PTO hours (this will be subtracted equally from each project).
     - **Scheduling Period:** Specify the number of weeks to schedule (e.g., `"weeks": 2` creates a 10-day schedule).

---

## Running the Application

1. **Run the Timesheet Calculator:**
   - In the terminal, run:
     ```
     python TimesheetCalculator.py
     ```
   - The program will regenerate the configuration (by running `config.py`), load it, and generate your timesheet based on `config.json`.

2. **Debug Mode:**
   - For detailed internal output (helpful for troubleshooting), run:
     ```
     python TimesheetCalculator.py --debug
     ```
   - Debug mode will display messages about configuration loading, time conversion, task allocation, and schedule generation.

---

## Running the Tests

A test suite (`tests.py`) is provided to ensure that all functionality works as expected.

- To run the tests, open a terminal and execute:
python test.py

- The tests use Python’s `unittest` framework and will report any issues, so you can be confident that the configuration, allocation, and scheduling logic are correct.

---

For additional personalized guidance, you can share this README with your preferred AI assistant, which can help answer questions about setup, debugging, or customizing the code for your specific use case.

Thank you for using the Timesheet Calculator!