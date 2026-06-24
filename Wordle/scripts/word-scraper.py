import requests
from lxml import html
import numpy as np
import pandas as pd

"""
This code is not production. 
This was code ran once that scraped a forum page for all world allowed guesses and potential answers.
"""

def wordScrape():
    url = "https://eslforums.com/5-letter-words/"
    headers = {"User-Agent" : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    pageContent = requests.get(url=url, headers=headers)

    tree = html.fromstring(pageContent.content)

    allWords = np.array(tree.xpath("//main//ul//li/text()"))

    pd.DataFrame(np.char.lower(allWords)).to_csv("5-letter-words.csv", header=False, index=False)

def organizeFiles():
    answers = np.loadtxt("wordle answers.txt",  dtype=str)
    guesses = np.loadtxt("wordle guesses.txt", dtype=str)

    allGuesses = np.concatenate([answers, guesses])

    pd.DataFrame(answers).to_csv("wordle_answers.csv", header=False, index=False)
    pd.DataFrame(allGuesses).to_csv("world_guesses.csv", header=False, index=False)

organizeFiles()