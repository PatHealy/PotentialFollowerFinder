# PotentialFollowerFinder
A twitter app to find potential followers of a given user: users who don't yet follow them but follow similar people

## Usage
```
python hashtag_search.print("python find_followers.py <user_handle> <similar_profiles_file>
	-user_handle: the handle of the user we are attempting to find new followers for.
	-similar_profiles_file: the name of a file containing other profiles potential followers are likely to follow.
```

###Output will display on the terminal as well as saving to two .csv files: 'followers.csv', a spreadsheet of all of the followers of the given profile, and 'potential_followers.csv', a ranked list of potential followers, with a 'count' of how many similar profiles are also followed by this profile.

###The application will automatically halt based on the Twitter API's rate-limiting. If the application seems to be halting progress, simply wait and it should continue progress within 15 minutes.

####This application also requires a configuration file named 'tweepy_config' with four lines of text representing the consumer_key, consumer_secret, access_token, and access_token_secret, respectively. For details, consult [the tweepy documentation.](https://tweepy.readthedocs.io/en/latest/auth_tutorial.html)
