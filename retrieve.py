import requests
import math
import time
from datetime import datetime, timedelta
import sqlite3
'''
all posts from ~2020 -- could change to 28, dec, 2008 to get all posts,
but the previous posts are undesirable --> don't fit a format
initially scraped ~2K posts
'''
connection = sqlite3.connect("db/facts.db", check_same_thread=False)
cursor = connection.cursor()
#cursor.execute("CREATE TABLE facts (fact TEXT)")

yesterday = datetime.today()-timedelta(days=1)
yesterday = int(time.mktime(yesterday.timetuple()))
subreddit = "todayilearned"

def write(string, mode):
    with open("db/facts.txt", mode, encoding='utf-8') as wfile:
        wfile.write(f"{string} \n")

def get_submission_count():
    api = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&metadata=true&size=0&after={yesterday}"
    response = requests.get(api)
    return response.json()['metadata']['total_results']

def canparse(fact):
    skip = ['TIL about', 'TIL of', 'TIL how']
    eval = True
    if len(fact) == 0:
        eval = False
        return eval
    for check in skip:
        if fact.find(check) != -1:
            eval = False
            break
    return eval

def propgrammar(fact, case):
    fact = fact[len(case):len(fact)-1]
    fact = fact.strip()
    fact.replace("&amp;", "and")
    fact = fact[0].upper() + fact[1:]
    if fact[len(fact)-1] != ".": fact += "."
    cursor.execute("INSERT INTO facts VALUES (?);", (fact, ))
    connection.commit()

def scrape_all():
    epochs = math.ceil(get_submission_count() / 100)
    scrape_count = 0
    after = yesterday

    remove = ['TIL that', 'TIL That', 'TIL: ', "TIL - ", "TIL"]

    for epoch in range(epochs):
        api = f"https://api.pushshift.io/reddit/submission/search/?after={after}&before={int(time.time())}&subreddit={subreddit}&limit=1000"
        response = requests.get(api)
        if response.status_code == 200:
            response = response.json()
            for submission in response['data']:
                author = submission['author']
                if author == "[deleted]":
                    continue
                created = submission['created_utc']
                title = submission['title']
                if len(title) < 40:
                    continue
                if "TIL" in title:
                    if canparse(title) == True:
                        for edgecase in remove:
                            if title.find(edgecase) != -1:
                                propgrammar(title, edgecase)
                                break
                after = created
                scrape_count += 1
                print(scrape_count)

if __name__ == '__main__':
    scrape_all()