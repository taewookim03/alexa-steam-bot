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

INVOCATION_NAME = "steam bot"

@app.route('/')
def homepage():
    return INVOCATION_NAME + " home page"

@ask.launch
def start_skill():
    welcome_message = "welcome to " + INVOCATION_NAME + ". say, new games, top sellers, or specials, followed by optional genre," \
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

if __name__ == "__main__":
    app.run(debug=True)
