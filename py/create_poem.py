#!/usr/bin/env python
# coding: utf-8

from twython import Twython
from string import punctuation
from nltk.corpus import stopwords
import pandas as pd
import re
import random
import json
import sys
import argparse

# These bottom two lines are only used when I delpy this srcript on my RaspberryPi server
import nltk
nltk.data.path.append("/home/pi/nltk_data")

'''---------------------------Command line processing---------------------------'''

parser = argparse.ArgumentParser()
parser.add_argument("-q", help='Required. Your search query.', required=True)
parser.add_argument(
    "-p", help='Number of posts to retrieve. 10 by default. 50 is maximum.')
parser.add_argument(
    "-l", help='Number of lines in the poem. If null, random number of lines will be generated.')
parser.add_argument(
    "-w", help='Number of words per line. If null, random number of words per line will be generated.')
args = parser.parse_args()

if args.p is not None:
    num_posts = args.p
else:
    num_posts = 10

if args.l is not None and int(args.l) > 50:
    args.l = 50

# Credentials for the Twitter API
consumer_key = '3qDoGtyhlhUTztzR3kDbVBCzl'
consumer_secret = 'IhW5jrCDf42Zz6Cd93qkB9faUEixPmb6kUGEJg8AGd22OTsF02'
access_token = '1136751418201837568-rJcG56DNfek9wClV63VlOI5eAEq2Gp'
access_secret = '1PrHTj8V26Y3TXVzfaHsIa3Sb1TE5ULUihIbukiwzh5pI'

# Instantiate an object
twit = Twython(consumer_key, consumer_secret)


def twitSearch(query, count):
    # Create our query
    query = {'q': args.q,
             'result_type': 'popular',
             'count': num_posts,
             'lang': 'en',
             'tweet_mode': 'extended'
             }
    # twit.search(**query)['statuses']

    # Search tweets
    d = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
    for status in twit.search(**query)['statuses']:
        d['user'].append(status['user']['screen_name'])
        d['date'].append(status['created_at'])
        d['text'].append(status['full_text'])
        d['favorite_count'].append(status['favorite_count'])

    # Structure data in a pandas DataFrame for easier manipulation
    return pd.DataFrame(d)


# We will use pandas to visualize and modify our data. It will make our life easier.

df = twitSearch('joy happiness', 10)
df.sort_values(by='favorite_count', inplace=True, ascending=False)


'''---------------------------Filtering---------------------------'''
# There are special characters in there. We want to remove characters like '&amp', '...'.
# Let's also get rid of the link at the end of each post ('https...').
# Split all the posts on a space to make a list. Makes modifying easier.
df['post_as_list'] = df['text'].apply(lambda i: i.split(' '))

# Let's remove puntuation from the end of every word in every post.
l = []

for i in df['post_as_list']:
    temp = []
    for j in i:
        # Remove punctuation and make the word lowercase
        temp.append(j.rstrip(punctuation).lower())
    l.append(temp)
df['post_as_list'] = l


# Let's filter the posts of words that conatain non alphanumeric characters.
# Filter the posts of words that conatain non alphanumeric characters. Ex: &amp, https://, \n, ...
filtered_list = []

for i in df['post_as_list']:
    temp = []
    for j in i:
        if re.match('^[\w+]+$', j) is not None:
            temp.append(j)
    filtered_list.append(temp)
df['filtered_text'] = filtered_list


# Let's filter out the stop words

# nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
l = []
for i in df['filtered_text']:
    filtered_sentence = [w for w in i if not w in stop_words]
    l.append(filtered_sentence)

df['filtered_text'] = l

# There are times when users use '2' instead of 'to', or '4' instead of for. I don't want that in my poem, so let's
# filter them out. I'm actually going to filter all the numberical values out. They may also use 'n' instead of 'in'.
# I am going to remove all words of length one.

# Fucntion to remove words of length one


def remove_one_len_words(lst):
    return [value for value in lst if len(value) > 1]


# Removing words of length one
l = []
for i in df['filtered_text']:
    l.append(remove_one_len_words(i))
df['filtered_text'] = l


# Let's now remove the numerical values
for i in df['filtered_text']:
    for j in i:
        if j.isnumeric():
            i.remove(j)


'''---------------------------Consrtuct the poem---------------------------'''

# Let's take all the words from the posts and combine them to make one list.
word_library = []

for i in df['filtered_text']:
    for j in i:
        word_library.append(j)

# Let's shuffle the list. Why not?
random.shuffle(word_library)

# Create the poem
poem = []

if args.l is None:
    num_lines = random.randint(8, 10)  # Number of lines in the poem
else:
    num_lines = int(args.l)

for i in range(num_lines):
    if args.w is None:
        num_words = random.randint(5, 8)  # Number of words per line
    else:
        num_words = int(args.w)
    temp_line = []  # Current line of the poem
    words_used = []  # Used to keep track of the words used on a line

    for j in range(num_words):
        r = random.randint(0, len(word_library)-1)
        word = word_library[r]

        if len(words_used) < len(word_library):
            while word in words_used:  # Keep trying to get a unique word
                r = random.randint(0, len(word_library)-1)
                word = word_library[r]

        temp_line.append(word)
        words_used.append(word)

    poem.append(temp_line)

# for i in poem:
#     print(i)

jsonPoem = json.dumps(poem)

print(jsonPoem)
