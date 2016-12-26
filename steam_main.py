from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import logging
from steam_scraper import *

app = Flask(__name__)
ask = Ask(app, '/')#app at the root

#set debug logger
log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

@app.route('/')
def homepage():
    return "steam bot home page"

@ask.launch
def start_skill():
    welcome_message = "welcome to steam bot. say, new games, top sellers, or specials, followed by optional genre," \
                      " to get sales information from steam. for example, say: ask steam bot for top sellers in horror."
    return statement(welcome_message)

@ask.intent('NewReleasesIntent', default={'genre':'Overall'})
def new_releases(genre):
    #note: for overall genre, top popular releases. for specific genre, just newest releases
    try:
        speech_output = get_games_speech(genre, 'NewReleases')
    except KeyError:
        return statement(genre + " is not a valid tag.")

    return statement(speech_output)

@ask.intent('TopSellersIntent', default={'genre':'Overall'})
def top_sellers(genre):
    try:
        speech_output = get_games_speech(genre, 'TopSellers')
    except KeyError:
        return statement(genre + " is not a valid tag.")

    return statement(speech_output)

@ask.intent('SpecialsIntent', default={'genre':'Overall'})
def specials(genre):
    try:
        speech_output = get_games_speech(genre, 'Specials')
    except KeyError:
        return statement(genre + " is not a valid tag.")

    return statement(speech_output)

# not implemented due to the lack of steam api - possible implementation later
# @ask.intent("MoreIntent")
# def more():
#     #track which function the user just used and get more results from the same function.
#     #e.g. if user asked for top games in horror, get more games in horror
#     return question("results")

@ask.intent('AMAZON.Stop')
def stop():
    return statement("Goodbye")

@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Goodbye")

@ask.session_ended
def session_ended():
    log.debug("Session ended")
    return '', 200#http response code

# def get_owned_games(apikey, steamid):
#     url = ("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
#            "?key={}&steamid={}&include_appinfo=1".format(apikey, steamid))
#     r = requests.get(url)
#     return json.loads(r.text)["response"]["games"]
# #for game in get_owned_games(api_key, steam_id):
# #    print game['name']
#
# #cache this upon startup to reduce response delay
# def get_all_games():
#     url = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/"
#     r = requests.get(url)
#     return json.loads(r.text)
#print get_all_games()['applist']['apps'][0]

#games = get_all_games()['applist']['apps']
#dict = {}
#for game in games:
#    dict[game['name']] = game['appid']
#print dict

if __name__ == "__main__":
    app.run(debug=True)
