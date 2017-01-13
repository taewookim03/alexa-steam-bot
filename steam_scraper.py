import urllib
from bs4 import BeautifulSoup
from string_matching import *

#info for using steam api (unnecessary for the current functions)
api_key = ''
steam_id = ''

#dictionary mapping tag to its tag id used by steam for search - generated by a separate script
#since there is no api for this
tag_to_id = FuzzyDict()#use a custom dictionary class that supports fuzzy string matching
tag_to_id.update({
    "hunting": "9564",
    "on rails shooter": "56690",
    "trains": "1616",
    "political": "4853",
    "world war i": "5382",
    "demons": "9541",
    "crime": "6378",
    "rogue like": "1716",
    "pinball": "6621",
    "nsfw": "24904",
    "turn based": "1677",
    "animation and modeling": "872",
    "comedy": "1719",
    "dynamic narration": "9592",
    "inventory management": "6276",
    "gaming": "150626",
    "otome": "31579",
    "linear": "7250",
    "football": "7226",
    "benchmark": "5407",
    "text based": "31275",
    "soundtrack": "7948",
    "online co op": "3843",
    "third person": "1697",
    "first person": "3839",
    "ninja": "1688",
    "software": "8013",
    "physics": "3968",
    "thriller": "4064",
    "mod": "5348",
    "building": "1643",
    "lemmings": "17337",
    "magic": "4057",
    "wargame": "4684",
    "great soundtrack": "1756",
    "psychological": "5186",
    "steampunk": "1777",
    "software training": "1445",
    "fighting": "1743",
    "simulation": "599",
    "2d": "3871",
    "realistic": "4175",
    "rome": "6948",
    "lara croft": "21722",
    "grid based movement": "7569",
    "bowling": "7328",
    "military": "4168",
    "assassin": "4376",
    "replay value": "4711",
    "experimental": "13782",
    "parody": "4878",
    "god game": "5300",
    "design and illustration": "84",
    "twin stick shooter": "4758",
    "pirates": "1681",
    "singleplayer": "4182",
    "indie": "492",
    "3d vision": "29363",
    "shoot em up": "4255",
    "real time with pause": "7107",
    "stealth": "1687",
    "dragons": "4046",
    "web publishing": "1038",
    "trading": "4202",
    "cyberpunk": "4115",
    "gun customization": "5765",
    "bullet time": "5796",
    "supernatural": "10808",
    "top down shooter": "4637",
    "education": "1036",
    "swordplay": "4608",
    "aliens": "1673",
    "open world": "1695",
    "underwater": "9157",
    "dark comedy": "19995",
    "nonlinear": "6869",
    "arcade": "1773",
    "hack and slash": "1646",
    "satire": "1651",
    "resource management": "8945",
    "sports": "701",
    "romance": "4947",
    "spectacle fighter": "4777",
    "retro": "4004",
    "bullet hell": "4885",
    "real time": "4161",
    "underground": "21006",
    "family friendly": "5350",
    "difficult": "4026",
    "action rpg": "4231",
    "competitive": "3878",
    "parkour": "4036",
    "relaxing": "1654",
    "kickstarter": "5153",
    "horror": "1667",
    "utilities": "87",
    "cinematic": "4145",
    "stylized": "4252",
    "controller": "7481",
    "rts": "1676",
    "lovecraftian": "7432",
    "point and click": "1698",
    "mythology": "16094",
    "america": "13190",
    "cartoon": "4562",
    "psychedelic": "1714",
    "third person shooter": "3814",
    "action": "19",
    "minimalist": "4094",
    "short": "4234",
    "city builder": "4328",
    "dystopian": "5030",
    "action adventure": "4106",
    "tower defense": "1645",
    "rpgmaker": "5577",
    "programming": "5432",
    "visual novel": "3799",
    "beat em up": "4158",
    "4 player local": "4840",
    "co op": "1685",
    "anime": "4085",
    "historical": "3987",
    "real time tactics": "3813",
    "loot": "4236",
    "interactive fiction": "11014",
    "free to play": "113",
    "side scroller": "3798",
    "procedural generation": "5125",
    "perma death": "1759",
    "2d fighter": "4736",
    "team based": "5711",
    "intentionally awkward controls": "14906",
    "abstract": "4400",
    "detective": "5613",
    "class based": "4155",
    "hex grid": "1717",
    "conspiracy": "5372",
    "gothic": "3952",
    "top down": "4791",
    "narration": "5094",
    "time attack": "5390",
    "drama": "5984",
    "tutorial": "12057",
    "puzzle platformer": "5537",
    "isometric": "5851",
    "politics": "4754",
    "batman": "1694",
    "mature": "5611",
    "audio production": "1027",
    "sandbox": "3810",
    "puzzle": "1664",
    "robots": "5752",
    "clicker": "379975",
    "management": "12472",
    "music": "1621",
    "story rich": "1742",
    "mystery dungeon": "198631",
    "cold war": "5179",
    "economy": "4695",
    "space sim": "16598",
    "racing": "699",
    "war": "1678",
    "jrpg": "4434",
    "split screen": "10816",
    "e sports": "5055",
    "gamemaker": "1649",
    "medieval": "4172",
    "platformer": "1625",
    "fast paced": "1734",
    "documentary": "15339",
    "moba": "1718",
    "score attack": "5154",
    "offroad": "7622",
    "typing": "1674",
    "card game": "1666",
    "mini golf": "22955",
    "space": "1755",
    "illuminati": "7478",
    "tanks": "13276",
    "character action game": "3955",
    "dungeon crawler": "1720",
    "spelling": "71389",
    "female protagonist": "7208",
    "destruction": "5363",
    "villain protagonist": "11333",
    "western": "1647",
    "pvp": "1775",
    "crafting": "1702",
    "multiplayer": "3859",
    "atmospheric": "4166",
    "tactical rpg": "21725",
    "sailing": "13577",
    "silent protagonist": "15954",
    "fmv": "18594",
    "science": "5794",
    "massively multiplayer": "128",
    "board game": "1770",
    "asynchronous multiplayer": "17770",
    "werewolves": "17015",
    "mechs": "4821",
    "pve": "6730",
    "zombies": "1659",
    "2.5d": "4975",
    "sokoban": "1730",
    "hidden object": "1738",
    "hacking": "5502",
    "based on a novel": "3796",
    "crowdfunded": "7113",
    "quick time events": "4559",
    "philisophical": "134316",
    "star wars": "1735",
    "cute": "4726",
    "steam machine": "348922",
    "gambling": "16250",
    "game development": "13906",
    "classic": "1693",
    "noir": "6052",
    "diplomacy": "6310",
    "wrestling": "47827",
    "survival horror": "3978",
    "adventure": "21",
    "sexual content": "12095",
    "moddable": "1669",
    "runner": "8666",
    "hand drawn": "6815",
    "cartoony": "4195",
    "pool": "17927",
    "nudity": "6650",
    "mmorpg": "1754",
    "co op campaign": "4508",
    "time manipulation": "6625",
    "martial arts": "6915",
    "photo editing": "809",
    "trading card game": "9271",
    "voxel": "1732",
    "crpg": "4474",
    "funny": "4136",
    "basketball": "1746",
    "superhero": "1671",
    "grand strategy": "4364",
    "mystery": "5716",
    "movie": "4700",
    "character customization": "4747",
    "mars": "6702",
    "vampire": "4018",
    "strategy": "9",
    "1980s": "7743",
    "surreal": "1710",
    "turn based tactics": "14139",
    "lego": "1736",
    "chess": "4184",
    "rhythm": "1752",
    "dark humor": "5923",
    "dating sim": "9551",
    "soccer": "1679",
    "memes": "10397",
    "warhammer 40k": "12286",
    "fantasy": "1684",
    "horses": "6041",
    "agriculture": "22602",
    "mining": "5981",
    "post apocalyptic": "3835",
    "flight": "15045",
    "episodic": "4242",
    "colorful": "4305",
    "alternate history": "4598",
    "party based rpg": "10695",
    "blood": "5228",
    "survival": "1662",
    "1990s": "6691",
    "transhumanism": "4137",
    "dark": "4342",
    "dinosaurs": "5160",
    "music based procedural generation": "8253",
    "turn based combat": "4325",
    "gore": "4345",
    "rpg": "122",
    "golf": "7038",
    "3d platformer": "5395",
    "sniper": "7423",
    "multiple endings": "6971",
    "heist": "1680",
    "time travel": "10679",
    "cult classic": "7782",
    "faith": "180368",
    "choose your own adventure": "4486",
    "naval": "6910",
    "4x": "1670",
    "psychological horror": "1721",
    "video production": "784",
    "shooter": "1774",
    "games workshop": "5310",
    "metroidvania": "1628",
    "dark fantasy": "4604",
    "foreign": "51306",
    "feature film": "233824",
    "vr": "21978",
    "lore rich": "3854",
    "fps": "1663",
    "6dof": "4835",
    "arena shooter": "5547",
    "level editor": "8122",
    "capitalism": "4845",
    "local co op": "3841",
    "futuristic": "4295",
    "sci fi": "3942",
    "word game": "24003",
    "tactical": "1708",
    "driving": "1644",
    "world war ii": "4150",
    "touch friendly": "25085",
    "match 3": "1665",
    "mouse only": "11123",
    "comic book": "1751",
    "modern": "5673",
    "turn based strategy": "1741",
    "strategy rpg": "17305",
    "hardware": "603297",
    "choices matter": "6426",
    "violent": "4667",
    "rogue lite": "3959",
    "base building": "7332",
    "fishing": "15564",
    "walking simulator": "5900",
    "pixel graphics": "3964",
    "exploration": "3834",
    "remake": "5708",
    "local multiplayer": "7368",
    "casual": "597",
    "trackir": "8075",
})

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
        if self.final_price == 0.00:
            s += "free"
        else:
            if self.discount_pct != 0: s += str(abs(self.discount_pct)) + "% off, "
            s += "${0:.2f}".format(self.final_price)
        return s

def get_games(genre, tab):
    """
    :param genre: Action, Adventure, Strategy, Casual, etc. (based on Steam's Popular Tags http://store.steampowered.com/tag/browse/#global_492
    :param tab: NewReleases, TopSellers, Specials (Discounts)
    :return: a list of game objects holding game title, price and discount percentage
    """

    #sanitize string
    genre = genre.encode("ascii").lower().replace('-', ' ').replace("'", '')

    search_filter = {"NewReleases":"filter=popularnew",
                     "TopSellers":"filter=topsellers",
                     "Specials":"specials=1"}

    # sort_param = ''
    # if tab == "NewReleases":
    #     sort_param = "sort_by=Released_DESC&"

    tag_param = ''
    if genre != "overall":
        tag_param = "tags=" + tag_to_id[genre] + "&"
    url = "http://store.steampowered.com/search/?{}{}".format(tag_param, search_filter[tab])
    #print url

    #overall urls:
    #http://store.steampowered.com/search/?sort_by=Released_DESC&filter=popularnew
    #http://store.steampowered.com/search/?filter=topsellers
    #http://store.steampowered.com/search/?specials=1

    #genre example urls:
    #http://store.steampowered.com/search/?sort_by=Released_DESC&tags=113&filter=popularnew
    #http://store.steampowered.com/search/?tags=492&filter=topsellers
    #http://store.steampowered.com/search/?tags=19&specials=1

    # check if url opens
    try:
        page = urllib.urlopen(url)
    except:
        raise IOError("invalid url")

    # scrape data
    soup = BeautifulSoup(page, "html.parser")
    #print soup.prettify()

    games_set = soup.find_all("div", class_="responsive_search_name_combined")#finds all game data (html)

    games = []
    for tag in games_set:
        game_data = Game()
        for child in tag.descendants:
            if type(child) == type(tag):
                try:
                    if child["class"] == [u'title']:
                        game_data.title = child.contents[0].encode('ascii', 'ignore')\
                            .replace('&', 'and')#ignore ascii and translate & (not valid SSML)
                    elif child["class"] == [u'col', u'search_discount', u'responsive_secondrow']:
                        try:
                            game_data.discount_pct = (int)(child.contents[1].string.strip('%'))
                        except:
                            pass#if above doesn't extract discount %, the game is free to play

                    #note: it seems child.contents[0] gets the full price for non-discounted items,
                    # child.contents[1] gets the full price for discounted items,
                    # and [2] gets the discounted price.
                    elif child["class"] == [u'col', u'search_price', u'discounted', u'responsive_secondrow']:
                        try:
                            game_data.final_price = (float)(child.contents[2].string.strip().lstrip('$'))
                        except:
                            pass#free to play

                    elif child["class"] == [u'col', u'search_price', u'responsive_secondrow']:
                        try:
                            game_data.final_price = (float)(child.contents[0].string.strip().lstrip('$'))
                        except:
                            pass#free to play
                except KeyError:#happens when tag does not have a class attribute (not interested in such tags)
                    pass
        games.append(game_data)
    #print games
    return games

def get_games_speech(genre, criterion):
    games = get_games(genre, criterion)#list of Game objects according to the criteria
    filter_description = {'NewReleases':"popular new releases ",
                          'TopSellers':"top sellers ",
                          'Specials':"special deals "}

    speech_output = filter_description[criterion]
    #overall is capitalized if default genre, not if explicitly passed.
    if not(genre == 'Overall' or genre == 'overall'): speech_output += "in "
    speech_output += genre + ". "

    game_titles = [str(game) for game in games]
    speech_output += ". ".join(game_titles)

    return speech_output

#test
#print get_games_speech("indie", "NewReleases")


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



