# Project Specification: Proactive Attendance Tracker CLI

## 1. Vision

To create a smart command-line application that proactively helps a user track their academic attendance. The application will prompt the user for their attendance daily, based on a predefined timetable. It is designed to be flexible, allowing for missed days, extra classes, and holidays. The core goal is to provide the user with clear, actionable statistics to maintain a desired attendance percentage (e.g., 75%).

## 2. Core Features

### 2.1. Attendance Prompting
- **Daily Prompts:** The application should be run once per day to prompt for attendance for that day's classes as defined in the timetable.
- **Missed Day Catch-up:** On launch, the application will check for any days between its last run and the current day. It will sequentially prompt the user for attendance for each missed day.

### 2.2. Timetable and Scheduling
- **Timetable-Based:** The app will use a `timetable.json` file to know which subjects to ask for on which day of the week.
- **Extra Classes:** The user can add an "extra class" for any subject on any date (past, present, or future). This can be done proactively or retroactively.
- **Holidays:**
  - Saturdays and Sundays are automatically treated as holidays.
  - The user can manually add a specific date as a holiday. This will prevent the app from asking for attendance on that day.

### 2.3. Statistics and Reporting
- **Percentage Calculation:** For each subject, the application will calculate and display the attendance percentage.
- **75% Threshold Analysis:**
  - It will clearly indicate if the attendance is >= 75% or < 75%.
  - If below 75%, it will calculate and display the number of consecutive classes the user must attend to reach the 75% mark.
- **Summary View:** A command to show a comprehensive summary of all subjects.

### 2.4. Data Management
- **Edit Past Records:** The user must be able to edit a past attendance record (e.g., change 'absent' to 'present' for a specific class on a specific date).

## 3. Proposed Implementation

### 3.1. Execution Model
- Instead of a complex, continuously running daemon, the application will be a script designed to be run automatically once per day via a system utility like **cron** (for Linux/macOS) or **Task Scheduler** (for Windows). This provides the desired "daily prompt" functionality in a robust and standard way.

### 3.2. Data Storage
- **`timetable.json`:** A file to store the user's weekly class schedule.
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
- **`attendance.json`:** A file to store all attendance records, holidays, and extra classes.
  ```json
  {
    "records": [
      {"date": "2026-01-05", "subject": "Math", "status": "present"},
      {"date": "2026-01-05", "subject": "Physics", "status": "absent"}
    ],
    "holidays": ["2026-01-01"]
  }
  ```

### 3.3. Language and Libraries
- **Language:** Python
- **Libraries:**
  - `click` for the command-line interface.
  - `datetime` for handling dates.
  - `json` for data storage.

## 4. CLI Commands (Proposed)

- `attendance check`: The main command, run daily. It checks for missed days and then prompts for the current day.
- `attendance summary`: Displays the statistics for all subjects.
- `attendance edit`: Starts an interactive prompt to modify a past record.
- `attendance add-class --subject <name> --date <YYYY-MM-DD>`: Adds an extra class.
- `attendance add-holiday <YYYY-MM-DD>`: Marks a specific date as a holiday.
