import click
from datetime import date
from . import data_manager, logic

@click.group()
def cli():
    """A CLI tool to track attendance."""
    pass

# --- Record Group ---
@click.group(name='record')
def record_group():
    """Commands for recording attendance."""
    pass

@record_group.command(name='check')
def check():
    """Check for missed days and prompt for today's attendance."""
    semester_start_date = data_manager.get_semester_start_date()
    semester_end_date = data_manager.get_semester_end_date()

    if not semester_start_date:
        click.echo("Semester start date is not set. Please set it using 'config set-start-date' command.")
        return

    today = date.today()
    if semester_end_date and today > date.fromisoformat(semester_end_date):
        click.echo("Semester has ended. No more attendance tracking.")
        return

    timetable = data_manager.get_timetable()
    attendance_data = data_manager.get_attendance_data()
    records = attendance_data['records']
    holidays = attendance_data['holidays']

    last_run_date_str = data_manager.get_last_run_date()
    missed_days = logic.get_missed_days(last_run_date_str, holidays, semester_start_date)

    if missed_days:
        click.echo("You have some missed days to account for.")
        for day in missed_days:
            if semester_end_date and day > date.fromisoformat(semester_end_date):
                continue
            day_name = day.strftime('%A')
            subjects = timetable.get(day_name, [])
            if subjects:
                prompt_for_attendance(day, subjects, records, holidays)

    # Handle today
    if today.isoformat() not in holidays and today.weekday() < 5 and today.isoformat() >= semester_start_date:
        if not semester_end_date or today <= date.fromisoformat(semester_end_date):
            day_name = today.strftime('%A')
            subjects_today = timetable.get(day_name, [])
            if subjects_today:
                todays_records = [r for r in records if r['date'] == today.isoformat()]
                if not todays_records:
                    prompt_for_attendance(today, subjects_today, records, holidays)
                else:
                    click.echo("Attendance for today has already been recorded.")

    data_manager.save_attendance_data(attendance_data)
    click.echo("Attendance data saved.")

@record_group.command(name='add-class')
@click.option('--subject', prompt='Subject name')
@click.option('--date', 'date_str', prompt='Date (YYYY-MM-DD)')
def add_class(subject, date_str):
    """Adds an extra class. Date format: YYYY-MM-DD"""
    try:
        date.fromisoformat(date_str)
    except ValueError:
        click.echo("Error: Date must be in YYYY-MM-DD format.")
        return

    attendance_data = data_manager.get_attendance_data()
    records = attendance_data['records']

    status = click.prompt(f"Status for {subject} on {date_str}", type=click.Choice(['p', 'a', 'c']), default='p')
    
    if status != 'c':
        records.append({
            "date": date_str,
            "subject": subject,
            "status": "present" if status == 'p' else "absent"
        })

    data_manager.save_attendance_data(attendance_data)
    click.echo(f"Added extra class for {subject} on {date_str}")

@record_group.command(name='cancel-class')
@click.option('--subject', prompt='Subject name')
@click.option('--date', 'date_str', prompt='Date (YYYY-MM-DD)')
def cancel_class(subject, date_str):
    """Cancels a class for a given date. Date format: YYYY-MM-DD"""
    try:
        date.fromisoformat(date_str)
    except ValueError:
        click.echo("Error: Date must be in YYYY-MM-DD format.")
        return

    data_manager.cancel_class(date_str, subject)
    click.echo(f"Cancelled {subject} on {date_str}")

# --- Config Group ---
@click.group(name='config')
def config_group():
    """Commands for configuration."""
    pass

@config_group.command(name='set-start-date')
@click.argument('date_str')
def set_start_date(date_str):
    """Sets the semester start date. Date format: YYYY-MM-DD"""
    try:
        date.fromisoformat(date_str)
    except ValueError:
        click.echo("Error: Date must be in YYYY-MM-DD format.")
        return

    data_manager.set_semester_start_date(date_str)
    click.echo(f"Semester start date set to {date_str}")

@config_group.command(name='set-end-date')
@click.argument('date_str')
def set_end_date(date_str):
    """Sets the semester end date. Date format: YYYY-MM-DD"""
    try:
        date.fromisoformat(date_str)
    except ValueError:
        click.echo("Error: Date must be in YYYY-MM-DD format.")
        return

    data_manager.set_semester_end_date(date_str)
    click.echo(f"Semester end date set to {date_str}")

# --- Holiday Group ---
@click.group(name='holiday')
def holiday_group():
    """Commands for managing holidays."""
    pass

@holiday_group.command(name='add')
@click.argument('date_str')
def add_holiday(date_str):
    """Marks a specific date as a holiday. Date format: YYYY-MM-DD"""
    try:
        date.fromisoformat(date_str)
    except ValueError:
        click.echo("Error: Date must be in YYYY-MM-DD format.")
        return

    attendance_data = data_manager.get_attendance_data()
    holidays = attendance_data['holidays']
    
    if date_str in holidays:
        click.echo(f"{date_str} is already a holiday.")
    else:
        holidays.append(date_str)
        data_manager.save_attendance_data(attendance_data)
        click.echo(f"Added {date_str} as a holiday.")

@holiday_group.command(name='remove')
@click.argument('date_str')
def remove_holiday(date_str):
    """Removes a holiday. Date format: YYYY-MM-DD"""
    try:
        date.fromisoformat(date_str)
    except ValueError:
        click.echo("Error: Date must be in YYYY-MM-DD format.")
        return

    attendance_data = data_manager.get_attendance_data()
    holidays = attendance_data['holidays']

    if date_str in holidays:
        data_manager.remove_holiday(date_str)
        click.echo(f"Removed {date_str} from holidays.")
    else:
        click.echo(f"{date_str} was not found in holidays.")

# --- View Group ---
@click.group(name='view')
def view_group():
    """Commands for viewing attendance data."""
    pass

@view_group.command(name='summary')
def summary():
    """Display the attendance summary."""
    attendance_data = data_manager.get_attendance_data()
    records = attendance_data['records']
    timetable = data_manager.get_timetable()
    
    all_subjects = sorted(list(set(subject for day_subjects in timetable.values() for subject in day_subjects)))
    
    for subject in all_subjects:
        percentage = logic.calculate_attendance_percentage(records, subject)
        needed = logic.calculate_classes_needed(records, subject)
        
        status = ">= 75%" if percentage >= 75 else "< 75%"
        
        message = f"{subject}: {percentage:.2f}% ({status})"
        if needed > 0:
            message += f" - You need to attend the next {needed} classes to reach 75%."
            
        click.echo(message)

@view_group.command(name='edit')
def edit():
    """Edit a past attendance record."""
    attendance_data = data_manager.get_attendance_data()
    records = attendance_data['records']

    if not records:
        click.echo("No records to edit.")
        return

    for i, record in enumerate(records):
        click.echo(f"{i+1}: {record['date']} - {record['subject']} ({record['status']})")

    try:
        record_num = click.prompt("Enter the number of the record to edit", type=int)
        if not (1 <= record_num <= len(records)):
            click.echo("Invalid number.")
            return
    except click.exceptions.Abort:
        return # User pressed Ctrl+C

    record_to_edit = records[record_num - 1]

    click.echo("Editing record:")
    click.echo(f"  Date: {record_to_edit['date']}")
    click.echo(f"  Subject: {record_to_edit['subject']}")
    click.echo(f"  Status: {record_to_edit['status']}")
    
    new_status = click.prompt("New status", type=click.Choice(['p', 'a', 'c']), default=record_to_edit['status'][0])
    
    if new_status == 'c':
        records.pop(record_num - 1)
    else:
        record_to_edit['status'] = 'present' if new_status == 'p' else 'absent'
    
    data_manager.save_attendance_data(attendance_data)
    click.echo("Record updated.")

def prompt_for_attendance(day, subjects, records, holidays):
    """Prompts the user for attendance for a given day and subjects."""
    click.echo(f"Attendance for {day.strftime('%A, %Y-%m-%d')}:")

    # Option to mark the whole day as a holiday
    if click.confirm(f"  Was this day a holiday?", default=False):
        holidays.append(day.isoformat())
        return

    for subject in subjects:
        status = click.prompt(f"  {subject}", type=click.Choice(['p', 'a', 'c']), default='p')
        if status != 'c': # Don't record cancelled classes
            records.append({
                "date": day.isoformat(),
                "subject": subject,
                "status": "present" if status == 'p' else "absent"
            })

cli.add_command(record_group)
cli.add_command(config_group)
cli.add_command(holiday_group)
cli.add_command(view_group)

if __name__ == '__main__':
    cli()