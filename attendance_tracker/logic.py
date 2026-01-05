from datetime import date, timedelta

def calculate_attendance_percentage(records, subject):
    """Calculates the attendance percentage for a given subject."""
    subject_records = [r for r in records if r['subject'] == subject and r['status'] != 'cancelled']
    if not subject_records:
        return 100.0
    
    present_count = sum(1 for r in subject_records if r['status'] == 'present')
    total_count = len(subject_records)
    
    return (present_count / total_count) * 100

def get_missed_days(last_run_date_str, holidays, semester_start_date_str):
    """Gets a list of dates that were missed since the last run."""
    start_date = date.fromisoformat(semester_start_date_str)
    
    if not last_run_date_str:
        last_run_date = start_date
    else:
        last_run_date = date.fromisoformat(last_run_date_str)

    if last_run_date < start_date:
        last_run_date = start_date

    today = date.today()
    missed_days = []
    
    current_date = last_run_date + timedelta(days=1)
    while current_date < today:
        if current_date.weekday() < 5 and current_date.isoformat() not in holidays:
            missed_days.append(current_date)
        current_date += timedelta(days=1)
        
    return missed_days

def calculate_classes_needed(records, subject):
    """
    Calculates how many more classes need to be attended to reach 75%.
    Returns 0 if the percentage is already >= 75%.
    """
    subject_records = [r for r in records if r['subject'] == subject and r['status'] != 'cancelled']
    total_classes = len(subject_records)
    present_classes = sum(1 for r in subject_records if r['status'] == 'present')

    if total_classes == 0:
        return 0

    percentage = (present_classes / total_classes) * 100 if total_classes > 0 else 100.0
    if percentage >= 75:
        return 0

    # Let 'x' be the number of additional classes to attend.
    # (present_classes + x) / (total_classes + x) = 0.75
    # present_classes + x = 0.75 * total_classes + 0.75 * x
    # 0.25 * x = 0.75 * total_classes - present_classes
    # x = (0.75 * total_classes - present_classes) / 0.25
    
    needed = (0.75 * total_classes - present_classes) / 0.25
    
    # Return the ceiling of the needed value
    return int(-(-needed // 1)) if needed > 0 else 0
