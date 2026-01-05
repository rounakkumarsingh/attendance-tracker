# Proactive Attendance Tracker CLI

A command-line application to proactively track your academic attendance. The application prompts for daily attendance based on a predefined timetable, handles missed days, and provides statistics to maintain a desired attendance percentage.

## Features

- **Proactive Prompting:** Checks for attendance records daily.
- **Missed Day Catch-up:** Prompts for any missed days since the last session.
- **Timetable-Driven:** Based on a user-provided `timetable.json`.
- **Flexible Scheduling:** Add extra classes and holidays.
- **Attendance Statistics:** Calculates and displays attendance percentages for each subject and shows how many classes are needed to reach 75%.
- **Data Management:** Edit past attendance records.
- **Semester Start Date:** Set a semester start date to only track attendance from that day onwards.
- **Cancelled Classes:** Mark classes as "cancelled" so they don't affect your attendance percentage.
- **Holiday on Prompt:** Mark a day as a holiday directly when prompted for attendance.

## Setup and Installation

### Prerequisites

- Python 3.10+
- `pip` and `venv`

### Installation Steps

1.  **Clone the repository (if you are setting it up from GitHub):**
    ```bash
    git clone <repository-url>
    cd attendance-tracker
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the package in editable mode:**
    This command will install the necessary dependencies and make the `attendance` command available in your terminal.
    ```bash
    pip install -e .
    ```

4.  **Configure your timetable:**
    The first time you run the application, it will create a `~/.attendance-tracker` directory in your home folder. Inside this directory, you will find a `timetable.json` file. Edit this file to match your weekly schedule.

    ```json
    {
      "Monday": ["Math", "Physics"],
      "Tuesday": ["Chemistry"],
      "Wednesday": ["Math", "Physics"],
      "Thursday": ["Chemistry"],
      "Friday": ["Math", "Biology"],
      "Saturday": [],
      "Sunday": []
    }
    ```
5. **Set the semester start date:**
    Before you start tracking your attendance, set the semester start date.
    ```bash
    attendance set-start-date YYYY-MM-DD
    ```

## Usage

The application provides several commands to manage your attendance.

-   **`attendance check`**: The main command to run daily. It prompts for missed days and the current day's attendance. When prompted for attendance, you can enter:
    - `p` for present
    - `a` for absent
    - `c` for cancelled
-   **`attendance summary`**: Displays the attendance statistics for all subjects.
-   **`attendance edit`**: Starts an interactive prompt to modify a past attendance record.
-   **`attendance add-class`**: Adds an extra class for a subject on a specific date. The date format is `YYYY-MM-DD`.
-   **`attendance add-holiday <YYYY-MM-DD>`**: Marks a specific date as a holiday. The date format is `YYYY-MM-DD`.
-   **`attendance set-start-date <YYYY-MM-DD>`**: Sets the semester start date. The date format is `YYYY-MM-DD`.

### Example: Setting up a Daily Cron Job

To have the application prompt you automatically, you can set up a cron job.

1.  Open your crontab file:
    ```bash
    crontab -e
    ```

2.  Add a line to run the `attendance check` command on a schedule. For example, to run it every hour from 9 AM to 5 PM on weekdays:
    ```
    0 9-17 * * 1-5 /path/to/your/attendance-tracker/.venv/bin/attendance check
    ```
    *Make sure to replace `/path/to/your/attendance-tracker` with the absolute path to the project directory.*

## Data Storage

All application data (attendance records, holidays, and your timetable) is stored in the `~/.attendance-tracker/` directory in your home folder.
