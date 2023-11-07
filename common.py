from config import *
import datetime
import pytz

def get_current_datetime():
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

    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S %Z')
    return formatted_time