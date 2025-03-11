import datetime
def get_time():
    current_date_time = datetime.datetime.now()
    current_date_time_string = current_date_time.strftime("%Y-%m-%d/%H:%M")
    # Split into day and Time
    current_date_time_string_list = current_date_time_string.split("/")
    date = current_date_time_string_list[0]
    # Get and Round Minutes
    minutes_int = int((current_date_time_string_list[1].split(":"))[1])
    hours_int = int((current_date_time_string_list[1].split(":"))[0])
    minutes_int_rounded = minutes_int - (minutes_int % 5)

    #Get Rounded Time
    if minutes_int_rounded < 10:
        rounded_time = str(hours_int) + ":0" + str(minutes_int_rounded)
    else:
        rounded_time = str(hours_int) + ":" + str(minutes_int_rounded)
    res = date + " " + rounded_time + ":00"

    return res
