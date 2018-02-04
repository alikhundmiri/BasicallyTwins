from . import manager_tweet, manager_email


# get the url of post
# get the twitter id
# get the email address

# generate the editable url

# if tweet, send it all to manager_tweet
# if email, send it all to manager_email



def initial_sort(product_name, slug, new_details):
	secret_url = generate_url(slug, new_details)
	print("the slug is: "+slug)
	# print(slug)
	for i in new_details:
		message = """
		hi @{}, I am the maker of basically Twins, a collection of profitable internet websites. 
		I added {} to my site. You can tweet me back here or you can visit this link to claim it as yours. {}
		""".format(i.contact, product_name, secret_url)
		if i.contact_type == "Twitter":
			manager_tweet.function_1(message)
		elif i.contact_type == "e-mail":
			manager_email.function_1(message)


def generate_url(slug, new_details):
	baselink = "127.0.0.1:8000/claim_products/"
	complete_link = baselink + slug
	return complete_link

