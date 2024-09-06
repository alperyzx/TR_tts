# Description: This script reads a text file, processes the text, and outputs the text in SSML format.
import functions
import re
import time
from google.cloud import texttospeech

with open("givenText.txt", "r", encoding="utf-8") as file:
    givenText = file.read()


#roman2numeral = functions.replace_roman_numerals(givenText)
#pfirstCheck = functions.firstCheck(roman2numeral)


pfirstCheck = functions.firstCheck(givenText)
prepParen = functions.repParen(pfirstCheck.lower())
prepWords = functions.repWords(prepParen)
pLastcheck = functions.lastCheck(prepWords)
prepPunct = functions.fixPunct(pLastcheck)
paddSsml = functions.addSsml(prepPunct)