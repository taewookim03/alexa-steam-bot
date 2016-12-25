import romanify
from Levenshtein import distance

#custom dictionary that supports fuzzy string matching (Levenshtein distance and numerical representations)
class FuzzyDict(dict):
    @classmethod
    def _lowercase_key(cls, key):
        return key.lower() if isinstance(key, basestring) else key

    @staticmethod
    def _is_roman_numeral(key):
        if not isinstance(key, basestring): return False
        # check if all the letters are valid roman numeral
        romans = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
        for letter in key.upper():
            if letter not in romans: return False
        return True

    def __init__(self, *args, **kwargs):
        super(FuzzyDict, self).__init__(*args, **kwargs)
        self._convert_keys()

    def __getitem__(self, key):
        # try both forms of a number as key - key being a game tag, it is unlikely that it will contain multiple
        # numbers of different forms
        key_arabic = key_roman = key
        for word in key.split():
            if self._is_roman_numeral(word):
                key_arabic = key_arabic.replace(word, romanify.roman2arabic(word))
        for word in key.split():
            if word.isdigit():
                key_roman = key_roman.replace(word, str(romanify.arabic2roman(word)))

        keys = [key, key_arabic, key_roman]

        for k in keys:
            try:
                return super(FuzzyDict, self).__getitem__(self.__class__._lowercase_key(k))
            except:
                pass

        # if converting the keys did not work, see if any of the available tag names are similar
        for similar_key in self.keys():
            if any ([distance(k, similar_key) <= 1 for k in keys]):#checking Levenshtein distance
                return super(FuzzyDict, self).__getitem__(self.__class__._lowercase_key(similar_key))

        raise KeyError

    def __setitem__(self, key, value):
        super(FuzzyDict, self).__setitem__(self.__class__._lowercase_key(key), value)
    def __delitem__(self, key):
        return super(FuzzyDict, self).__delitem__(self.__class__._lowercase_key(key))
    def __contains__(self, key):
        return super(FuzzyDict, self).__contains__(self.__class__._lowercase_key(key))
    def has_key(self, key):
        return super(FuzzyDict, self).has_key(self.__class__._lowercase_key(key))
    def pop(self, key, *args, **kwargs):
        return super(FuzzyDict, self).pop(self.__class__._lowercase_key(key), *args, **kwargs)
    def get(self, key, *args, **kwargs):
        return super(FuzzyDict, self).get(self.__class__._lowercase_key(key), *args, **kwargs)
    def setdefault(self, key, *args, **kwargs):
        return super(FuzzyDict, self).setdefault(self.__class__._lowercase_key(key), *args, **kwargs)
    def update(self, E=None, **F):
        super(FuzzyDict, self).update(self.__class__(E))
        super(FuzzyDict, self).update(self.__class__(**F))
    def _convert_keys(self):
        for k in list(self.keys()):
            v = super(FuzzyDict, self).pop(k)
            self.__setitem__(k, v)


#print distance("track ir", "detective")

# names = [ 'Catherine', 'Katherine', 'Katarina',
#           'Johnathan', 'Jonathan', 'John',
#           'Teresa', 'Theresa',
#           'Smith', 'Smyth',
#           'Jessica',
#           'Joshua',
#           ]

#for name in names:
#    print dmeta(name)

# #sanitize string and then encode in dmeta
# def dmeta_wrapper(key):
#     dmeta = fuzzy.DMetaphone()
#
#     return dmeta(key)

#print dmeta_wrapper("Xpack - SD3: Digital Sound Factory - Acoustic Kits")
#print dmeta_wrapper("rwby")