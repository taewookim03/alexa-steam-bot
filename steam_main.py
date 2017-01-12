from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, request
import logging
from steam_scraper import *

app = Flask(__name__)
ask = Ask(app, '/')#app at the root

#set debug logger
log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

INVOCATION_NAME = "hot dog"

#to easily verify that the skill is online
@app.route('/')
def homepage():
    return INVOCATION_NAME + " home page"

@ask.launch
def start_skill():
    welcome_message = "welcome to " + INVOCATION_NAME + " for steam. say, new games, top sellers, or specials, " \
                      "followed by optional tag, to get sales information from steam. for example, say: top sellers in strategy."
    return question(welcome_message)

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
@ask.intent('AMAZON.HelpIntent')
def help():
    help_message = INVOCATION_NAME + " is a skill that allows you to browse games and apps on steam, sorted by tag " \
                                     "and filter. for example, if you would like to know what strategy games are " \
                                     "on sale in the steam store, you can say: specials in strategy. " \
                                     "similarly, you can also ask for the new releases or top sellers in any " \
                                     "of the popular steam tags by saying: new games in tag, or top sellers in tag. " \
                                     "examples of steam tags include: indie, action, horror, adventure, racing, and many more. " \
                                     "what would you like?"
    return question(help_message)


@ask.intent('AMAZON.StopIntent')
@ask.intent('AMAZON.CancelIntent')
def stop():
    bye = "goodbye"
    return statement(bye)

@ask.session_ended
def session_ended():
    return "", 200

if __name__ == "__main__":
    app.run(debug=True)
