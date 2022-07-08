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
cursor.execute("CREATE TABLE facts (fact TEXT)")

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

def scrape_all():
    epochs = math.ceil(get_submission_count() / 100)
    scrape_count = 0
    after = yesterday
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
                    write(f"{created}|{title}", "a")
                after = created
                scrape_count += 1
                print(scrape_count)

def propgrammar(fact, case):
    fact = fact[len(case):len(fact)-1]
    fact = fact.strip()
    fact = fact[0].upper() + fact[1:]
    if fact[len(fact)-1] != ".": fact += "."
    cursor.execute("INSERT INTO facts VALUES (?);", (fact, ))
    connection.commit()

def parse():
    print("Parsing...")
    remove = ['TIL that', 'TIL That', 'TIL: ', "TIL - ", "TIL"]
    with open("db/facts.txt", 'r', encoding='utf-8') as readfile:
        facts = readfile.read()
    facts = facts.split("\n")
    
    for i in range(len(facts)-1):
        fact = facts[i]
        fact.replace("&amp;", "and")
        if fact.find("TIL about") != -1:
            continue
        if fact.find("TIL of") != -1:
            continue
        if fact.find("TIL how") != -1:
            continue
        fact = fact.split("|")[1]
        for edgecase in remove:
            if fact.find(edgecase) != -1:
                propgrammar(fact, edgecase)
                break

if __name__ == '__main__':
    scrape_all()
    time.sleep(3)
    parse()
    write(" ", "w")