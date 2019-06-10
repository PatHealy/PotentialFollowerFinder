import tweepy
import sys
import csv

def show_usage():
    print("python hashtag_search.py <hashtag> <output_file_name> [<limit>]")
    print("\thashtag: the hashtag you're searching for")
    print("\toutput_file_name: the name of the file this will be saved to (will be extended with .csv)")
    print("\tlimit: the maximum number of tweets you want to query (optional). Defaults to 20. Use 'max' if you want to attempt to load without limit. Note: This limit corresponds to how many tweets are loaded but RTs are ignored regardless, so one will almost always get less than their limit of tweets.")
    print()
    print("This application also requires a configuration file named 'tweepy_config' with four lines of text representing the consumer_key, consumer_secret, access_token, and access_token_secret, respectively. For details, consult the tweepy documentation.")

def clean_query_string(q):
    q = str(q)
    if q[0] != '#':
        q = '#' + q
    return '(' + q + ')'

def clean_output_filename(fn):
    fn = str(fn)
    ind = fn.rfind('.')
    if ind != -1:
        fn = fn[:ind-1]
    return fn + '.csv'

def get_tweets(api, query_string, limit):
    if limit == -1:
        public_tweets = tweepy.Cursor(api.search, q=query_string, tweet_mode='extended').items()
    else:
        public_tweets = tweepy.Cursor(api.search, q=query_string, tweet_mode='extended').items(limit)
    
    tweets = []
    
    for tweet in public_tweets:
        if 'retweeted_status' not in vars(tweet).keys():
            t = {}
            t['tweet_id'] = str(tweet.id)
            t['author'] = str(tweet.author.name)
            t['handle'] = "@" + str(tweet.author.screen_name)
            t['created_at'] = str(tweet.created_at)
            t['text'] = str(tweet.full_text)
            t['media'] = []
            print("id: " + str(tweet.id))
            print("author: " + str(tweet.author.name))
            print("handle: " + "@" + str(tweet.author.screen_name))
            print("date: " + str(tweet.created_at))
            print("text: " + str(tweet.full_text))
            if 'extended_entities' in tweet._json and 'media' in tweet._json['extended_entities']:
                out = 'extended media: '
                for m in tweet._json['extended_entities']['media']:
                    t['media'].append(str(m['media_url']))
                    out = out + str(m['media_url']) + ', '
                out = out[:-2]
                print(out)
            elif 'media' in tweet.entities:
                out = 'media: '
                for m in tweet.entities['media']:
                    t['media'].append(str(m['media_url']))
                    out = out + str(m['media_url']) + ', '
                out = out[:-2]
                print(out)
            print()
            print("====================================")
            print()
            tweets.append(t)
    return tweets

def save_tweets(fn, tweets):
    with open(fn, 'w') as writeFile:
        writer = csv.writer(writeFile)
        
        header = ['tweet_id', 'author', 'handle', 'datetime', 'text', 'media_link', 'media_link_2', 'media_link_3', '...']
        writer.writerow(header)
        
        for tweet in tweets:
            ln = []
            ln.append(tweet['tweet_id'])
            ln.append(tweet['author'])
            ln.append(tweet['handle'])
            ln.append(tweet['created_at'])
            ln.append(tweet['text'])
            for m in tweet['media']:
                ln.append(m)
            writer.writerow(ln)

try:
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''

    with open('tweepy_config') as config_file:
        consumer_key = config_file.readline().strip()
        consumer_secret = config_file.readline().strip()
        access_token = config_file.readline().strip()
        access_token_secret = config_file.readline().strip()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    query_string = clean_query_string(sys.argv[1])
    output_fn = clean_output_filename(sys.argv[2])
    limit = 20
    if len(sys.argv) > 3:
        if sys.argv[3] == 'max':
            limit = -1
        else:
            limit = int(sys.argv[3])

    tweets = get_tweets(api, query_string, limit)
    save_tweets(output_fn, tweets)
except:
    #traceback.print_exc()
    show_usage()