from config import *
import datetime
import pytz

def get_current_datetime_object():
    timezone_offset_str = TIMEZONE_OFFSET_STR

    # Parse the timezone_offset_str into hours and minutes
    sign, offset_str = timezone_offset_str[0], timezone_offset_str[1:]
    hours, minutes = map(int, offset_str.split(':'))

    # Calculate the total offset in minutes
    offset_minutes = (hours * 60 + minutes) if sign == '+' else -(hours * 60 + minutes)

    # Create a custom timezone with the calculated offset
    custom_tz = pytz.FixedOffset(offset_minutes)

    # Get the current time with the custom timezone
    current_time = datetime.datetime.now(custom_tz)

    return current_time

def get_current_datetime():
    current_time = get_current_datetime_object()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S %Z')
    return formatted_time

def get_current_date():
    current_time = get_current_datetime_object()
    formatted_time = current_time.strftime('%Y-%m-%d')
    return formatted_time

def get_current_time():
    current_time = get_current_datetime_object()
    formatted_time = current_time.strftime('%H:%M:%S')
    return formatted_time

def get_current_day():
    current_time = get_current_datetime_object()
    current_day = current_time.strftime('%A').lower()
    return current_day

def get_today_target(setting):
    current_day = get_current_day()
    if current_day == 'monday':
        return setting.target_monday
    elif current_day == 'tuesday':
        return setting.target_tuesday
    elif current_day == 'wednesday':
        return setting.target_wednesday
    elif current_day == 'thursday':
        return setting.target_thursday
    elif current_day == 'friday':
        return setting.target_friday
    elif current_day == 'saturday':
        return setting.target_saturday
    elif current_day == 'sunday':
        return setting.target_sunday
    else:
        raise ValueError("Invalid day input")


