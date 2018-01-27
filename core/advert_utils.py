from .models import product, adverts

def ad_contract_completion(ad):
	ad.advert_status = adverts.AD_STATUS[3][0]
	pass

def fetch_adverts():
	LOAD_ADS = 3
	num_list = []
	# fetch ads
	fetch_ = adverts.objects.filter(advert_status="Paid")
	# fetch the total number of ads available
	limit_ = fetch_.count()
	if limit_ == 0:
		return None
	elif limit_ <= LOAD_ADS:
		rand_ad = fetch_[:limit_]
	else:
		# generate 3 number from the limited range
		num_list = random.sample(range(0, limit_), LOAD_ADS)
		# fetch those ads
		rand_ad = [fetch_[num] for num in num_list]

	# print(rand_ad)
	# mark those ads with viewed!
	mark_viewed(rand_ad)
	return rand_ad

def mark_viewed(rand_ad):
	for ad in rand_ad:
		# increment the advert_view field
		ad.advert_view += 1
		ad.save()
		# print(ad.advert_view)
	pass