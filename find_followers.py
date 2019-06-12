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

def write_followers_file(fn, followers, print_count=False):
    with open(fn, 'w') as write_file:
        writer = csv.writer(write_file)
        if print_count:
            writer.writerow(['Screen_name', 'Name', 'Bio', 'Count'])
        else:
            writer.writerow(['Screen_name', 'Name', 'Bio'])
        for follower in followers:
            if print_count:
                writer.writerow([follower['screen_name'], follower['name'], follower['bio'], follower['count']])
            else:
                writer.writerow([follower['screen_name'], follower['name'], follower['bio']])
    return

def get_current_followers(api, this_handle, profile):
    print("Name: " + profile.name)
    print("Screen Name: " + profile.screen_name)
    print("Followers_count: " + str(profile.followers_count))
    print()

    print("====================")
    print("Followers")
    print("====================")

    followers = []
    for follower in tweepy.Cursor(api.followers,user_id=profile.id).items():
        print("===Screen_name: " + follower.screen_name + ",\tName: " + follower.name + '\n\t--Bio: ' + follower.description.replace('\n',' ') + '')
        followers.append({'screen_name': follower.screen_name, 'name': follower.name, 'bio': follower.description.replace('\n',' ')})
    print()
    print("====================")
    print()
    return followers

def get_similar_profiles(api, similar_fn):
    profs = []

    with open(similar_fn) as similar_file:
        for line in similar_file:
            try:
                profs.append(get_profile(api, line.strip()))
            except:
                continue

    return profs

def get_profile(api, this_handle):
    profile = api.get_user(screen_name=this_handle)
    if profile is None:
        print("The given profile (" + this_handle + ") does not exist.")
        raise Exception
    return profile

def get_similar_followers(api, similar_profiles):
    similar_followers = []
    for profile in similar_profiles:
        similar_followers.extend(get_current_followers(api, profile.screen_name, profile))

    return similar_followers

def get_unique_followers(followers, similar_followers):
    frequencies = {}
    previous_followers = []
    non_unique = []
    potential_followers = []

    for follower in followers:
        previous_followers.append(follower['screen_name'])

    for follower in similar_followers:
        if(follower['screen_name'] not in previous_followers):
            if follower['screen_name'] not in non_unique:
                follower['count'] = 1
                potential_followers.append(follower)
                non_unique.append(follower['screen_name'])
            else:
                for user in potential_followers:
                    if user['screen_name'] == follower['screen_name']:
                        user['count'] = user['count'] + 1

    return sorted(potential_followers, key = lambda i: i['count'], reverse=True)

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

    profile = get_profile(api, sys.argv[1])

    os.mkdir(profile.screen_name)

    followers = get_current_followers(api, profile.screen_name, profile)
    write_followers_file(profile.screen_name + '/followers.csv', followers)
    similar_profiles = get_similar_profiles(api, sys.argv[2])
    similar_followers = get_similar_followers(api, similar_profiles)
    potential_followers = get_unique_followers(followers, similar_followers)
    write_followers_file(profile.screen_name + '/potential_followers.csv', potential_followers, print_count=True)

    print("Potential followers saved to " + profile.screen_name + '/potential_followers.csv')
    print("==========================")
    print("Completed.")

except:
    traceback.print_exc()
    print("\n==========================================\n")
    show_usage()