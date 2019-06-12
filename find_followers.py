import tweepy
import sys
import traceback
import os
import csv

def show_usage():
    print("python find_followers.py <user_handle> <similar_profiles_file>")
    print("\tuser_handle: the handle of the user we are attempting to find new followers for")
    print("\tsimilar_profiles_file: the name of a file containing other profiles potential followers are likely to follow")
    print()
    print("This application also requires a configuration file named 'tweepy_config' with four lines of text representing the consumer_key, consumer_secret, access_token, and access_token_secret, respectively. For details, consult the tweepy documentation.")
    print()

def get_current_followers(this_handle, profile):
    print("Name: " + profile.name)
    print("Screen Name: " + profile.screen_name)
    print("Followers_count: " + str(profile.followers_count))
    print()

    print("====================")
    print("Followers")
    print("====================")

    fn = this_handle + "/followers.csv"
    followers = []
    with open(fn, 'w') as write_file:
        writer = csv.writer(write_file)
        writer.writerow(['Screen_name', 'Name', 'Bio'])
        for follower in tweepy.Cursor(api.followers,user_id=profile.id).items():
            print("===Screen_name: " + follower.screen_name + ",\tName: " + follower.name + '\n\t--Bio: ' + follower.description.replace('\n',' ') + '')
            writer.writerow([follower.screen_name, follower.name, follower.description])
            followers.append({'screen_name': follower.screen_name, 'name': follower.name, 'bio': follower.description})

    return followers

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

    this_handle = sys.argv[1]
    profile = api.get_user(screen_name=this_handle)
    if profile is None:
        print("The given profile does not exist.")
        raise Exception

    os.mkdir(this_handle)

    followers = get_current_followers(this_handle, profile)

except:
    traceback.print_exc()
    print("\n==========================================\n")
    show_usage()