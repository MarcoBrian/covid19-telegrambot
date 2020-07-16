# Foreword
I was first introduced to the Telegram bot when I was using it to play games with my family during the lockdown period.
I was super excited when i found out that the telegram bots are open to developers 
for them to freely create their own bots. I was inspired
 to creat this bot because i wanted to get easy updates of the current
pandemic through the messaging app and to also easily 
share relevant information with loved ones. 

# Telegram COVID19 Bot
You can find the bot in Telegram : @covid19statsbot

This telegram bot fetches data from the open sourced MongoDB version of the John Hopkins COVID19 Dataset. 

The MongoDB github repo is found in https://github.com/mongodb-developer/open-data-covid-19 .

The bot is hosted using Heroku free plan. Not suited for heavy requests. 

# Features 

The implementation of the bot is fairly simple and straightforward. Honestly there is nothing fancy with this bot and just simple querying from MongoDB. 
Currently the available bot commands are: 

- /start - Getting started command for understanding basic functions

- /worldstats - Returns back the global stats of COVID19

- /stats [country] - Place a country right next to the command to receive stats for the particular country

- /countries - display a list of available countries

- /top [number] - enter a numeric argument and it will display the top [number] countries with highest cases.' \
           '(ex /top 10 will display top 10 countries with highest cases of COVID19). Without argument default is 10 countries

- /news [country] - will get most recent news of COVID19 in the country (retrieves 10 articles)

- /daily - Global daily increase

- /weekly - Global weekly increase 