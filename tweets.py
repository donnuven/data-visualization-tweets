from config import *
import tweepy as tw
import sys
import csv
import pandas as pd
import pyfiglet
from pyfiglet import Figlet
import matplotlib.pylab as plt
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
import re

# setup twitter authentication
auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tw.API(auth)


class StartUp:
    '''
    On Start up this will display an options page of the CLI tool  
    with a nice ASCII terminal banner

    '''

    def __init__(self):
        self.color_font = 'cyan'

    def on_start_up(self):
        custom_fig = Figlet(font='big')
        application_name = custom_fig.renderText("Tweeting Mill")
        iteration = "v.0.1.0 - A Twitter CLI Tool"
        introductions = [application_name + '\n' + iteration]
        for introduction in introductions:
            print(introduction)

    def options(self):
        first_option = "0 - Return to the options page."
        second_option = "1 - Search up a twitter user and user's recent post."
        third_option = "2 - Create a data log to form a word cloud of recent tweets of a user."
        fourth_option = "3 - Exit program"
        option_lists = [first_option + "\n" + second_option +
                        "\n" + third_option + "\n" + fourth_option]
        for option in option_lists:
            print(option)


class Tweeting_Mill:
    def __init__(self):
        self.screen_name = screen_name = str(input('twitter user:'))
        self.count = count = int(input('post count:'))

    # search up the most recent tweets from a user's timeline.
    def search_recent_tweet(self):
        tweet_log = tw.Cursor(api.user_timeline, screen_name=self.screen_name,
                              exclude_replies=True).items(self.count)
        for tweet in tweet_log:
            print(tweet.text, '----', tweet.created_at,
                  '-----', tweet.favorite_count, "\n")

    # custom recoloring of words in the word cloud.
    def change_color_func(self, word, font_size, position, orientation, random_state=None, **kwargs):
        return("hsl(230,100%%,%d%%)" % np.random.randint(78, 150))

    # convert the most recent tweet of a user's timeline into a csv file

    def tweet_csv_conversion(self):
        tweet_data = tw.Cursor(api.user_timeline, screen_name=self.screen_name,
                               exclude_replies=True).items(self.count)
        file_name = str(input('csv file name:'))

        # create a csv file
        csv_file = open(file_name + data['fmt_ext'], 'a')
        csv_writer = csv.writer(csv_file)

        # write to the csv file
        for tweet in tweet_data:
            csv_writer.writerow([tweet.text.encode('utf-8')])
            #print(tweet.text, '-----', tweet.created_at, "\n")
        csv_file.close()

    # convert a tweet of a user's timeline into a word cloud

    def tweet_cloud(self):
        # choose a tweet of choice from the csv file.

        csv_file_name = str(input('read which csv file:'))
        tweet_data = pd.read_csv(csv_file_name + data['fmt_ext'])
        print(tweet_data, "\n\n")
        tweet_choice = int(input('tweet of choice(starting with 0 to nth):'))
        tweet_data.columns = ["tweet"]
        tweets = tweet_data.tweet[tweet_choice]
        tweets.replace("https", " ").replace(
            "@", " ").replace("b'", " ").replace("RT", " ")
        twitter_mask = np.array(Image.open('assets/twitter.jpg'))

        # generate word cloud
        wordcloud = WordCloud(width=1800, height=1400,
                              mask=twitter_mask, background_color="black").generate(tweets)
        default_colors = wordcloud.to_array()
        wordcloud_file_name = str(input('wordcloud file name to save file:'))
        # wordcloud recolorization
        wc = wordcloud.recolor(
            color_func=self.change_color_func, random_state=42)

        # display the wordcloud of a tweet from a user
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.savefig(wordcloud_file_name)
        plt.show()


if __name__ == "__main__":
    startup = StartUp()
    startup.on_start_up()
    startup.options()

while True:
    options = str(input('options:'))

    if options == '0':
        startup.on_start_up()
        startup.options()

    elif options == '1':
        tm = Tweeting_Mill()
        tm.search_recent_tweet()

    elif options == '2':
        tm = Tweeting_Mill()
        tm.tweet_csv_conversion()
        tm.tweet_cloud()

    elif options == '3':
        sys.exit()

    elif options != '3':
        print("Error: Invalid option")
