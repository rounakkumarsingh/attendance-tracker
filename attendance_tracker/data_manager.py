import json
from pathlib import Path
import shutil

# The root directory of the project installation
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = Path.home() / '.attendance-tracker'
TIMETABLE_FILE = DATA_DIR / 'timetable.json'
ATTENDANCE_FILE = DATA_DIR / 'attendance.json'

def ensure_data_dir_exists():
    """Creates the data directory if it doesn't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def get_timetable():
    """Reads the timetable from the JSON file in the data directory.
    
    If the file doesn't exist in the data directory, it copies it from the project root.
    """
    ensure_data_dir_exists()
    if not TIMETABLE_FILE.exists():
        source_file = PROJECT_ROOT / 'timetable.json'
        if source_file.exists():
            shutil.copy(source_file, TIMETABLE_FILE)
        else:
            return {}
            
    with open(TIMETABLE_FILE, 'r') as f:
        return json.load(f)

def save_timetable(timetable):
    """Saves the timetable to the JSON file."""
    ensure_data_dir_exists()
    with open(TIMETABLE_FILE, 'w') as f:
        json.dump(timetable, f, indent=2)

def get_attendance_data():
    """Reads the attendance data from the JSON file in the data directory.
    
    If the file doesn't exist in the data directory, it copies it from the project root.
    """
    ensure_data_dir_exists()
    if not ATTENDANCE_FILE.exists():
        source_file = PROJECT_ROOT / 'attendance.json'
        if source_file.exists():
            shutil.copy(source_file, ATTENDANCE_FILE)
            with open(ATTENDANCE_FILE, 'r') as f:
                data = json.load(f)
        else:
            data = {'records': [], 'holidays': [], 'semester_start_date': None, 'semester_end_date': None}
    else:
        with open(ATTENDANCE_FILE, 'r') as f:
            data = json.load(f)

    if 'semester_start_date' not in data:
        data['semester_start_date'] = None
    if 'semester_end_date' not in data:
        data['semester_end_date'] = None
    if 'holidays' not in data:
        data['holidays'] = []
    if 'records' not in data:
        data['records'] = []

    return data

def save_attendance_data(data):
    """Saves the attendance data to the JSON file."""
    ensure_data_dir_exists()
    with open(ATTENDANCE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_last_run_date():
    """Gets the last date attendance was recorded."""
    data = get_attendance_data()
    if not data['records']:
        return get_semester_start_date()
    return max(record['date'] for record in data['records'])

def get_semester_start_date():
    """Gets the semester start date."""
    data = get_attendance_data()
    return data.get('semester_start_date')

def set_semester_start_date(start_date):
    """Sets the semester start date."""
    data = get_attendance_data()
    data['semester_start_date'] = start_date
    save_attendance_data(data)

def get_semester_end_date():
    """Gets the semester end date."""
    data = get_attendance_data()
    return data.get('semester_end_date')

def set_semester_end_date(end_date):
    """Sets the semester end date."""
    data = get_attendance_data()
    data['semester_end_date'] = end_date
    save_attendance_data(data)

def add_holiday(holiday_date):
    """Adds a holiday to the list of holidays."""
    data = get_attendance_data()
    if holiday_date not in data['holidays']:
        data['holidays'].append(holiday_date)
        save_attendance_data(data)

def remove_holiday(holiday_date):
    """Removes a holiday from the list of holidays."""
    data = get_attendance_data()
    if holiday_date in data['holidays']:
        data['holidays'].remove(holiday_date)
        save_attendance_data(data)

def cancel_class(date_str, subject):
    """Cancels a class for a given date and subject."""
    data = get_attendance_data()
    records = data['records']
    
    # Check if a record for this class already exists
    for record in records:
        if record['date'] == date_str and record['subject'] == subject:
            record['status'] = 'cancelled'
            break
    else:
        # If no record exists, create one
        records.append({
            "date": date_str,
            "subject": subject,
            "status": "cancelled"
        })
        
    save_attendance_data(data)

