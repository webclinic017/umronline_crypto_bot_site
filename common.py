from config import *
from datetime import datetime, timedelta
import pytz
import re


def get_summary_of_orders(orders):
    order_summary = {
        "total_trades": 0,
        "total_profit": 0,
        "total_trading_fees": 0
    }
    for order in orders:
        if order.status == "sold":
            order_summary["total_trades"] += 1
            order_summary["total_profit"] += order.profit
            order_summary["total_trading_fees"] += order.total_trading_fees
    return order_summary


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
    current_time = datetime.now(custom_tz)

    return current_time

def get_current_datetime():
    current_time = get_current_datetime_object()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S %Z')
    return formatted_time

def get_current_date_beautified():
    current_date = get_current_datetime_object()
    formatted_time = f"{current_date.strftime('%A')} ~ {current_date.strftime('%B')} {current_date.strftime('%d')}"
    return formatted_time

def get_current_time_beautified():
    current_time = get_current_datetime_object()
    formatted_time = current_time.strftime('%I:%M:%S %p')
    return formatted_time

def beautify_date(date_str):
    current_date = datetime.strptime(date_str, '%Y-%m-%d')
    formatted_date = f"{current_date.strftime('%A')} ~ {current_date.strftime('%B')} {current_date.strftime('%d')}"
    return formatted_date

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

def get_target(date_str, setting):
    current_date = datetime.strptime(date_str, '%Y-%m-%d')
    current_day = current_date.strftime('%A').lower()
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
def get_today_target(setting):
    current_date = get_current_date()
    get_target(current_date, setting)

def extract_logs_for_today():
    today = get_current_date()
    with open(LOG_FILE, 'r') as file:
        file_content = file.read()
        logs_for_today = today + file_content.split(today,1)[1]
    return logs_for_today

