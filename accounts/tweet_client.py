from twython import Twython, TwythonError

from .credentials import (
	consumer_key,
	consumer_secret,
	access_token,
	access_token_secret
	)
twitter = Twython(
	consumer_key,
	consumer_secret,
	access_token,
	access_token_secret
	)


def write_tweet_only(tweet):
	try:
		twitter.update_status(status=tweet)
		print("Tweeted : {}".format(tweet))
		return True
	except TwythonError as e:
		print(e)
		return False

