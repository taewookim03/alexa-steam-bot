from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import requests
import json
from urllib import urlopen

import logging

#info for using steam api (unnecessary for the current functions)
api_key = ''
steam_id = ''

app = Flask(__name__)
ask = Ask(app, '/')#app at the root

#set debug logger
log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@app.route('/')
def homepage():
    return "news for steam home page"

@ask.launch
def start_skill():
    welcome_message = "Welcome to Steam News. Say [put instructions here]."
    return statement(welcome_message)

# @ask.intent("GameIntent")
# def game_intent(game):
#    print game
#    return statement("you entered " + game)

def get_url(genre, tab):
    """
    :param genre: Action, Adventure, Strategy, Casual, etc. (based on Steam's Popular Tags http://store.steampowered.com/tag/browse/#global_492
    :param tab: NewReleases, TopSellers, Specials (Discounts)
    :return: url of the web page containing desired data
    """
    url = ''
    if genre == "Overall":
        url = "http://store.steampowered.com/search/?filter=topsellers"
    else:

    return



@ask.intent("NewReleasesIntent", default={"genre":"Overall"})
def new_releases(genre):
    url = "something"

    return question("new releases")

@ask.intent("TopSellersIntent", default={"genre":"Overall"})
def top_sellers(genre):
    url = "http://store.steampowered.com/search/?{}{}".format(genre_tag(genre), filtr)

    return question("top sellers")
#do you want more? say yes, more or no, stop

@ask.intent("SpecialsIntent", default={"genre":"Overall"})
def specials(genre):
    return question("specials")

@ask.intent("MoreIntent")
def more():
    #track which function the user just used and get more results from the same function.
    #e.g. if user asked for top games in horror, get more games in horror
    return question("results")

@ask.intent("AMAZON.Stop")
def stop():
    return statement("Goodbye")

@ask.intent("AMAZON.CancelIntent")
def cancel():
    return statement("Goodbye")

@ask.session_ended
def session_ended():
    log.debug("Session ended")
    return '', 200#response code

#function name according to PEP-8
def get_owned_games(apikey, steamid):
    url = ("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
           "?key={}&steamid={}&include_appinfo=1".format(apikey, steamid))
    r = requests.get(url)
    return json.loads(r.text)["response"]["games"]
    #return json.loads(urlopen(url).read().decode("utf-8"))["response"]["games"]
#for game in get_owned_games(api_key, steam_id):
#    print game['name']

#cache this upon startup to reduce response delay
def get_all_games():
    url = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/"
    r = requests.get(url)
    return json.loads(r.text)
    #return json.loads(urlopen(url).read().decode('utf-8'))
#print get_all_games()['applist']['apps'][0]

#games = get_all_games()['applist']['apps']
#dict = {}
#for game in games:
#    dict[game['name']] = game['appid']

#print dict.keys()
#print dict['Portal']
#print len(dict)
#print dict


if __name__ == "__main__":
    app.run(debug=True)
