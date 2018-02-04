from django.conf import settings

from accounts import tweet_client
def function_1(tweet):
	if settings.SEND_TWEETS:
		tweet_client.write_tweet_only(tweet)
		print("Tweeted !\n" + tweet)
	else:
		print("Tweet created, but not send, \n" + tweet)