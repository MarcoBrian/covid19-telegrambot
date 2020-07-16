# stores helper functions

# this function is used to reformat country names into more intuitive sense
# because the database does not store the country name in such a way.
def format_country_name_for_db(country_name):
    if country_name == "South Korea":
        return "Korea, South"
    elif country_name == "Taiwan":
        return "Taiwan*"
    elif country_name == "United States":
        return "US"
    else:
        return country_name

# opposite of above function
def format_country_name(country_name):
    if country_name == "Korea, South":
        return "South Korea"
    elif country_name == "Taiwan*":
        return "Taiwan"
    elif country_name == "US":
        return "United States"
    else:
        return country_name

def retrieve_info_from_object(obj):
    try:
        total_confirmed = obj["confirmed"]
    except Exception as e:
        total_confirmed = 0
    try:
        total_deaths = obj["deaths"]
    except Exception as e:
        total_deaths = 0
    try:
        total_recovered = obj["recovered"]
    except Exception as e:
        total_recovered = 0

    return total_confirmed , total_deaths, total_recovered

def put_info_to_object(total_confirmed,total_deaths,total_recovered,current_date):
    obj = {}
    obj["confirmed"] = total_confirmed
    obj["deaths"] = total_deaths
    obj["recovered"] = total_recovered
    obj["date"] = current_date
    return obj

def stats_to_text_world(obj,last_date):
    total_confirmed , total_deaths , total_recovered = retrieve_info_from_object(obj)
    total_confirmed_str = f"{total_confirmed:,}"
    total_deaths_str = f"{total_deaths:,}"
    total_recovered_str = f"{total_recovered:,}"
    date_str = "<b>" + last_date.strftime("%d %B, %Y") + "</b>"
    text = "Global COVID19 statistics as of " + date_str + ". \n\n" + \
           "Total confirmed cases : " + total_confirmed_str + "\n" + \
           "Total deaths : " + total_deaths_str + "\n" \
            "Total recovered: " + total_recovered_str + "\n"
    return text

def stats_to_text_country(obj,last_date,country_name):

    total_confirmed, total_deaths, total_recovered = retrieve_info_from_object(obj)
    total_confirmed_str = f"{total_confirmed:,}"
    total_deaths_str = f"{total_deaths:,}"
    total_recovered_str = f"{total_recovered:,}"
    date_str = "<b>" + last_date.strftime("%d %B, %Y") + "</b>"
    country_name = format_country_name(country_name)
    text = "COVID19 statistics of " + country_name + " as of " + date_str + ". \n\n" + \
           "Total confirmed cases : " + total_confirmed_str + "\n" + \
           "Total deaths : " + total_deaths_str + "\n" \
            "Total recovered: " + total_recovered_str + "\n"
    return text


def stats_to_text_world_diff(obj):
    confirmed = obj["confirmed"]
    deaths = obj["deaths"]
    current_date = obj["current_date"]
    before_date = obj["before_date"]

    confirmed_str = f"{confirmed:,}"
    deaths_str = f"{deaths:,}"

    current_date_str = "<b>" + current_date.strftime("%d %B, %Y") + "</b>"
    before_date_str = "<b>" + before_date.strftime("%d %B, %Y") + "</b>"

    text = "Global increase from " + before_date_str + " to " + current_date_str + ". \n\n" \
           "Confirmed cases increased by : " + confirmed_str + "\n" + \
           "Deaths increased by : " + deaths_str + "\n"
    return text
