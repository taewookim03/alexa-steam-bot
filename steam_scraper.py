import urllib
from bs4 import BeautifulSoup

#info for using steam api (unnecessary for the current functions)
api_key = ''
steam_id = ''

#new releases is popular new releases
overall_tab_url = {"NewReleases":"http://store.steampowered.com/explore/new/",
                   "TopSellers":"http://store.steampowered.com/search/?filter=topsellers",
                   "Specials":"http://store.steampowered.com/search/?specials=1"}

#simple struct-like class to hold game data
class Game(object):
    __slots__ = ['title', 'discount_pct', 'final_price']
    def __init__(self, title=u'', discount_pct=0, final_price=0.00):
        self.title = title
        self.discount_pct = discount_pct
        self.final_price = final_price

    def __repr__(self):
        return self.title + ': $' + str(self.final_price) + ' (' + str(self.discount_pct) + '%)'

    def __str__(self):
        s = self.title + ", "
        if self.discount_pct != 0: s += str(abs(self.discount_pct)) + "% off for "
        s += "${0:.2f}".format(self.final_price)
        return s

def get_games(genre, tab):
    """
    :param genre: Action, Adventure, Strategy, Casual, etc. (based on Steam's Popular Tags http://store.steampowered.com/tag/browse/#global_492
    :param tab: NewReleases, TopSellers, Specials (Discounts)
    :return: a list of game objects holding game title, price and discount percentage
    """
    if genre == "Overall":
        url = overall_tab_url[tab]
    else:
        if tab == "Specials":
            tab = "Discounts"
        url = "http://store.steampowered.com/tag/en/{}/#p=0&tab=NewReleases".format(urllib.quote(genre))#tag is encoded for url
        #url = "http://store.steampowered.com/search/?tags={}&page={}"

    #r = requests.get(url)
    #print r.text

    #check if url opens


    #scrape data
    #url = "http://store.steampowered.com/search/?tags=1698&page=2"
    #url = "http://store.steampowered.com/tag/browse/#global_492"
    page = urllib.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")

    #print soup.prettify()
    #print url
    #print tab

    tag = soup.find("div", id=tab+"Rows")

    games = []
    for child in tag.children:
        if type(child) == type(tag):
            game_data = Game()
            for d in child.descendants:
                if type(d) == type(tag):
                    try:
                        if d["class"] == [u"tab_item_name"]:
                            game_data.title = d.contents[0].encode('ascii', 'ignore')#ignore unicode in game title
                        elif d["class"] == [u"discount_pct"]:
                            game_data.discount_pct = (int)(d.contents[0].rstrip('%'))
                        elif d["class"] == [u"discount_final_price"]:
                            game_data.final_price = (float)(d.contents[0].lstrip('$'))
                    except KeyError:
                        pass
            games.append(game_data)
    print games
    return games

#test
#p = get_games("Action", "Specials")

