import click
from datetime import date
from . import data_manager, logic

@click.group()
def cli():
    """A CLI tool to track attendance."""
    pass

def prompt_for_attendance(day, subjects, records):
    """Prompts the user for attendance for a given day and subjects."""
    click.echo(f"Attendance for {day.strftime('%A, %Y-%m-%d')}:")
    for subject in subjects:
        status = click.prompt(f"  {subject}", type=click.Choice(['p', 'a']), default='p')
        records.append({
            "date": day.isoformat(),
            "subject": subject,
            "status": "present" if status == 'p' else "absent"
        })

@cli.command()
def check():
    """Check for missed days and prompt for today's attendance."""
    timetable = data_manager.get_timetable()
    attendance_data = data_manager.get_attendance_data()
    records = attendance_data['records']
    holidays = attendance_data['holidays']

    last_run_date_str = data_manager.get_last_run_date()
    missed_days = logic.get_missed_days(last_run_date_str, holidays)

    if missed_days:
        click.echo("You have some missed days to account for.")
        for day in missed_days:
            day_name = day.strftime('%A')
            subjects = timetable.get(day_name, [])
            if subjects:
                prompt_for_attendance(day, subjects, records)

    # Handle today
    today = date.today()
    if today.isoformat() not in holidays and today.weekday() < 5:
        day_name = today.strftime('%A')
        subjects_today = timetable.get(day_name, [])
        if subjects_today:
            # Check if attendance for today has already been recorded
            todays_records = [r for r in records if r['date'] == today.isoformat()]
            if not todays_records:
                 prompt_for_attendance(today, subjects_today, records)
            else:
                click.echo("Attendance for today has already been recorded.")

    data_manager.save_attendance_data(attendance_data)
    click.echo("Attendance data saved.")


@cli.command()
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


@cli.command()
@click.option('--subject', prompt='Subject name')
@click.option('--date', prompt='Date (YYYY-MM-DD)')
def add_class(subject, date):
    """Adds an extra class."""
    # Logic to add a class will be implemented here
    click.echo(f"Adding extra class for {subject} on {date}")

@cli.command()
@click.argument('date')
def add_holiday(date):
    """Marks a specific date as a holiday."""
    # Logic to add a holiday
    click.echo(f"Adding {date} as a holiday.")

@cli.command()
def edit():
    """Edit a past attendance record."""
    # Logic to edit a record
    click.echo("Editing past attendance...")


if __name__ == '__main__':
    cli()
