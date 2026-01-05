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
        else:
            return {'records': [], 'holidays': []}

    with open(ATTENDANCE_FILE, 'r') as f:
        return json.load(f)

def save_attendance_data(data):
    """Saves the attendance data to the JSON file."""
    ensure_data_dir_exists()
    with open(ATTENDANCE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_last_run_date():
    """Gets the last date attendance was recorded."""
    data = get_attendance_data()
    if not data['records']:
        return None
    return max(record['date'] for record in data['records'])