import fuzzy
import Levenshtein
import re

names = [ 'Catherine', 'Katherine', 'Katarina',
          'Johnathan', 'Jonathan', 'John',
          'Teresa', 'Theresa',
          'Smith', 'Smyth',
          'Jessica',
          'Joshua',
          ]

dmeta = fuzzy.DMetaphone()
#for name in names:
#    print dmeta(name)

#compute double metaphone encoding and save
def multi_word_dmeta(title):
    #delimit based on colon to separate titles and subtitles e.g. "The Elder Scrolls V: Skyrim Special Edition"
    #also - (e.g. "Xpack - SD3: Digital Sound Factory - Acoustic Kits")
    substrings = re.split(':|-', title)
    print substrings

    list = []
    for word in substrings:
        #if word is a number (roman numeral, arabic number, or written out ("one" "two"))
        #convert to a list of possible number representations
        list.append(dmeta(word))
    return list
print multi_word_dmeta("Xpack - SD3: Digital Sound Factory - Acoustic Kits")
print multi_word_dmeta("rwby")