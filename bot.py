import time
import os
import requests
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
import database
from database import *
import helper

# callback for handlers
@run_async
def worldstats(update,context):
    total_confirmed = 0
    total_deaths = 0
    current_date = None
    # get latest date available
    meta = database.get_latest_metadata()
    last_date = meta["last_date"]
    # check context bot_data for world stat cache
    world_object = context.bot_data.get("worldstats", None)
    if world_object is not None and world_object["date"] == last_date:
        print("catched")
        # fetch data from cache
        total_confirmed = world_object["confirmed"]
        total_deaths = world_object["deaths"]
        current_date = last_date
    else:
        print("storing in cache")
        total_confirmed , total_deaths = database.fetch_cases(last_date)
        current_date = last_date
        # store data in bot_data cache
        world_object = {}
        world_object["confirmed"] = total_confirmed
        world_object["deaths"] = total_deaths
        world_object["date"] = current_date
        context.bot_data["worldstats"] = world_object

    total_confirmed_str = f"{total_confirmed:,}"
    total_deaths_str = f"{total_deaths:,}"
    date_str = "<b>" + last_date.strftime("%d %B, %Y") + "</b>"
    text = "Global COVID19 statistics as of " + date_str + ". \n\n" + \
           "Total confirmed cases : " + total_confirmed_str + "\n" + \
           "Total deaths : " + total_deaths_str
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode = telegram.ParseMode.HTML)

@run_async
def stats(update,context):
    total_confirmed = 0
    total_deaths = 0
    current_date = None

    # get latest date available
    meta = database.get_latest_metadata()
    last_date = meta["last_date"]

    country_name = ' '.join(context.args)
    if country_name in context.bot_data["countries"]:
        pass
    else:
        arguments = [arg.lower() for arg in context.args]
        arguments = [arg.capitalize() for arg in arguments]
        country_name = ' '.join(arguments)

    if country_name == '':
        context.bot.send_message(chat_id=update.effective_chat.id, text='Please place a country next to the command')
        return

    country_name = helper.format_country_name_for_db(country_name)

    # check if this country exists
    exist = global_stat.find_one({"country":country_name})
    if exist is None:
        text = 'The country you typed does not exist.\nSome common error might be your misspelling or you have typed a word ' \
               'that is not a country. Look at available countries from the /countries command.'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    else:
        country_object = context.bot_data.get(country_name, None)
        if country_object is not None and country_object["date"] == last_date:
            print("catched")
            # fetch data from cache
            total_confirmed = country_object["confirmed"]
            total_deaths = country_object["deaths"]
            current_date = last_date
        else:
            print("storing in cache")
            total_confirmed , total_deaths = database.fetch_cases(last_date,country_name)
            current_date = last_date
            # store data in bot_data cache
            country_object = {}
            country_object["confirmed"] = total_confirmed
            country_object["deaths"] = total_deaths
            country_object["date"] = current_date
            context.bot_data[country_name] = country_object

        total_confirmed_str = f"{total_confirmed:,}"
        total_deaths_str = f"{total_deaths:,}"
        date_str = "<b>" + last_date.strftime("%d %B, %Y") + "</b>"
        country_name = helper.format_country_name(country_name)
        text = "COVID19 statistics of " + country_name +  " as of " + date_str + ". \n\n" + \
               "Total confirmed cases : " + total_confirmed_str + "\n" + \
               "Total deaths : " + total_deaths_str
        context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode = telegram.ParseMode.HTML)

@run_async
def countries(update,context):
    #list of available countries
    countries = context.bot_data["countries"]
    text = 'List of countries where COVID19 Data is available: \n\n'
    for i in range(len(countries)):
        line = str(i+1) + ". " + countries[i] + '\n'
        text += line
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

@run_async
def top(update,context):

    # get latest date available
    meta = database.get_latest_metadata()
    last_date = meta["last_date"]
    top = 0

    arg_len = len(context.args)
    if arg_len > 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Please enter one argument only')
        return
    elif arg_len == 0:
        top = 10 #if no argument specified top 10 by default
    else:
        first_param = context.args[0]
        if first_param.isnumeric():
            top = int(first_param)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Please enter a number for the argument')
            return
    if top > 50 :
        context.bot.send_message(chat_id=update.effective_chat.id, text='The message will be too long, try a smaller number')
        return
    date_str = "<b>" + last_date.strftime("%d %B, %Y") + "</b>"
    text = 'Top ' + str(top) + ' countries with highest confirmed cases as of ' + date_str + ' : \n\n'
    results = global_stat.find({"date": last_date}).sort("confirmed", pymongo.DESCENDING).limit(top)
    index = 1
    for result in results:
        line = ''
        try:
            country_name = result["country"]
            line += str(index) + "." + country_name + ": \n"
        except Exception as e:
            logging.warning(e)
        try:
            confirmed = result["confirmed"]
            confirmed_str = f"{confirmed:,}"
            line += "confirmed cases: " + confirmed_str + "\n"
        except Exception as e:
            logging.warning(e)

        try:
            deaths = result["deaths"]
            deaths_str = f"{deaths:,}"
            line += "deaths : " + deaths_str + "\n"
        except Exception as e:
            logging.warning(e)
        line += "\n"
        text += line
        index += 1
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode = telegram.ParseMode.HTML)

@run_async
def news(update,context):
    country_name = ' '.join(context.args)
    if country_name in context.bot_data["countries"]:
        pass
    else:
        arguments = [arg.lower() for arg in context.args]
        arguments = [arg.capitalize() for arg in arguments]
        country_name = ' '.join(arguments)

    country_name = helper.format_country_name_for_db(country_name)

    countries_list = context.bot_data["countries"]

    if country_name == '':
        context.bot.send_message(chat_id=update.effective_chat.id, text='Please place a country next to the command')
        return

    if country_name not in countries_list:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Please enter one of the countries as argument')
    else:
        country_name = helper.format_country_name(country_name)
        query = country_name.replace(" ", "%20") + "%20coronavirus"
        news_token = os.environ['NEWS_API_KEY']
        url = 'https://gnews.io/api/v3/search?q=' + query + '&token=' + news_token
        response = requests.get(url)
        result = response.json()
        articles = result["articles"]
        for art in articles:
            url = art["url"]
            text = url + '\n'
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=text, parse_mode=telegram.ParseMode.HTML)
            time.sleep(2.5) #small delay in sending for better UX


@run_async
def start(update,context):
    text = '<b> Getting Started: </b> \n\n'\
           'To get quick access to the current latest confirmed cases globally please use the /worldstats command.\n\n' \
           'To get the current stats for a particular country type in /stats followed by the country name.\n' \
           '(For eg: \'/stats United Kingdom\' , \'/stats United States\') \n\n' \
           'For more commands take a look at /info! \n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text,parse_mode = telegram.ParseMode.HTML)

@run_async
def info(update,context):
    text = '/start - Getting started command for understanding basic functions \n\n' \
           '/worldstats - Returns back the global stats of COVID19 \n\n' \
           '/stats [country] - Place a country right next to the command to receive stats for the particular country \n\n' \
           '/countries - display a list of available countries \n\n' \
           '/top [number] - enter a numeric argument and it will display the top [number] countries with highest cases.' \
           '(ex /top 10 will display top 10 countries with highest cases of COVID19) \n\n' \
           '/news [country] - will get most recent news of COVID19 in the country (retrieves 10 articles) \n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

# handling unknown command and non-commands
@run_async
def unknown(update, context):
    response = 'Sorry, the command you entered is not valid ' \
               'please have a look at the /start command to get started or /info for all available commands.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

@run_async
def noncommand(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='/info for description of available commands')

def main():
    token = os.environ['BOT_API_KEY']
    bot = telegram.Bot(token=token)
    print(bot.get_me())
    updater = Updater(token=token, use_context=True, workers=20)
    dispatcher = updater.dispatcher

    # initialization store country data
    meta = database.get_latest_metadata()
    dispatcher.bot_data["countries"] = meta["countries"]

    # register handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    world_handler = CommandHandler('worldstats', worldstats)
    dispatcher.add_handler(world_handler)

    stats_handler = CommandHandler('stats', stats)
    dispatcher.add_handler(stats_handler)

    countries_handler = CommandHandler('countries', countries)
    dispatcher.add_handler(countries_handler)

    info_handler = CommandHandler('info', info)
    dispatcher.add_handler(info_handler)

    top_handler = CommandHandler('top',top)
    dispatcher.add_handler(top_handler)

    news_handler = CommandHandler('news', news)
    dispatcher.add_handler(news_handler)

    noncommand_handler = MessageHandler(Filters.text & (~Filters.command), noncommand)
    dispatcher.add_handler(noncommand_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    PORT = int(os.environ.get('PORT','8443'))
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=token)
    updater.bot.set_webhook("https://hidden-depths-10325.herokuapp.com/" + token)
    updater.idle()

main()