import requests
from bs4 import BeautifulSoup
import random
import time
import tweepy

# Twitter API credentials
consumer_key = 'MEj7IADVZC8GREkeTqDsqnqhV'
consumer_secret = 'W5cVkPBU4MewdyirBaD7b7VKJpZ1BoAQWoIK6mwAtelnRxvOOQ'
access_token_key = '1467618889823576065-nVZHfVa9pBwLT4jPqEKphjRDVQaLif'
access_token_secret = 'nFW3m1OhcBCVJdmWIchS3XIIcamuWs5EmIqz2Z3LmBx8T'

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

class SearchEngine:
    def __init__(self, query):
        self.query = query
        self.visited_links = set()
        self.found_links = set()
        self.current_link = None

    def start(self):
        url = f"https://scholar.google.com/scholar?q={self.query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("h3", class_="gs_rt")
        links = []
        for result in results:
            link = result.find("a")["href"]
            if link not in self.visited_links and link not in self.found_links:
                links.append(link)
        if links:
            link = random.choice(links)
            self.visited_links.add(link)
            self.found_links.add(link)
            self.current_link = link
            print(f"Link found: {link}")
        else:
            print("No links found.")

    def get_links(self):
        links = []
        for link in self.found_links:
            try:
                response = requests.get(link)
                soup = BeautifulSoup(response.text, "html.parser")
                title = soup.title.text.strip()[:140] if soup.title else "Title not found"
                if len(title) + len(link) + 26 <= 280:
                    tweet_text = f"{title}: {link}\n#SaveTheBees #PollinatorConservation #PlanetKeeperDAO"
                elif len(title) + 26 <= 280:
                    tweet_text = f"{title}\n{link}\n#SaveTheBees #PollinatorConservation #PlanetKeeperDAO"
                else:
                    tweet_text = f"{link}\n#SaveTheBees #PollinatorConservation #PlanetKeeperDAO"
                api.update_status(tweet_text)
                links.append(link)
                print(f"Tweeted: {tweet_text}")
            except tweepy.TweepError as e:
                print(f"Error while tweeting: {e}")
        return links

    def get_new_links(self):
        new_links = set(self.found_links) - set(self.visited_links)
        self.visited_links.update(new_links)
        return new_links

# Create instance of the search engine
search_engine = SearchEngine("bees pollinators conservation")

while True:
    # Run the search engine and get the new links
    search_engine.start()
    new_links = search_engine.get_links()

    # Wait 6 hours before running the search engine again
    time.sleep(21600)


