# stores helper function

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