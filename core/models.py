from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.core.validators import URLValidator

import uuid
import random
from datetime import datetime, timedelta

def upload_location(adverts, filename):
	return "%s/%s/%s/%s" %(adverts.app_name, adverts.customer.product_name, adverts.user, filename)

def suggest_product():
	names = ['Bit translator', 'hoboprinter', 'Phone Smith',
				'Rock anne Role', 'Traders Back', 'Vortex Ship',
				'Rings of Bong', 'BlueSkin', 'Trackin', 
				'Wild flips', 'Cube box', 'Train Fins',
				'Glowing Bulb', 'Eurika', 'Bit Moment',
				'Stick ship', 'Reavling', 'Measurant',
				'Thin Gap', 'Spinning Floor', 'Callar']

	return(random.choice(names))

def unique_link_element():
	uid = uuid.uuid4()
	unque = uid.hex
	return unque

class links(models.Model):
	PLATFORM = (
		('Android', 'android'),
		('iOS', 'ios'),
		('Website', 'website'),
		('Chrome Extension', 'chrome'),
		)
	user					=			models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	platform				=			models.CharField(max_length=30, choices=PLATFORM, default=PLATFORM[0][0])
	link 					=			models.CharField(max_length=1000, blank=False, null=False)
	social_connection		=			models.ForeignKey('product', related_name='social_links', on_delete=models.CASCADE)

	def __str__(self):
		return (str(self.platform) + str(" for ") + str(self.social_connection))

	class Meta:
		verbose_name 		= 			"Link"
		verbose_name_plural = 			"Links"

class tags(models.Model):
	tag 					=			models.CharField(max_length=30, blank=False, null=False)
	slug 					=			models.SlugField(max_length=255, unique=True)

	timestamp				=			models.DateTimeField(auto_now=False, auto_now_add=True)
	updated					=			models.DateTimeField(auto_now=True, auto_now_add=False)

	# def get_absolute_url(self):
	# 	return reverse("user:tag", kwargs={"slug" : self.slug})
	def __str__(self):
		return (str(self.tag))
	class Meta:
		ordering 			=			["-timestamp", "-updated"]
		verbose_name 		=	 		"Tag"
		verbose_name_plural =	 		"Tags"

'''
	Each product is a website which has completed the following 
		1.	Started earning
		2.	Somerhing in common with a different company
		3. 	May or may not be VC funded
		4.	May or may not be Bootstrapped
	

	Each Product MUST be linked to one or more product, via twin Field.
	This is the sole of this website
'''
class email_list(models.Model):
	email 					=			models.EmailField(max_length=100 ,unique=True)
	timestamp				=			models.DateTimeField(auto_now=False, auto_now_add=True)
	updated					=			models.DateTimeField(auto_now=True, auto_now_add=False)

	# def get_absolute_url(self):
	# 	return reverse("user:tag", kwargs={"slug" : self.slug})
	def __str__(self):
		return (str(self.email))
	class Meta:
		ordering 			=			["-timestamp", "-updated"]
		verbose_name 		= 			"Email List"
		verbose_name_plural = 			"Email Lists"

class revenue_source(models.Model):
	REV_SOURCE = (
		("------", "------"),
		("Advertisments", "Ads"),
		("Subscription", "subscription"),
		("One time Payment", "entry fees"),
		("eCommence", "eCommence"),
		("Service sales", "service sales"),
		("Digital Product sales", "digital product sales"),
		("Digital Service sales", "digital service sales"),
		("Affiliate Marketing", 'Affiliate Marketing'),
		)
	source 					=			models.CharField(max_length=50, choices=REV_SOURCE, default=REV_SOURCE[0][0])

	def __str__(self):
		return(str(self.source))

class product_catagory(models.Model):
	PRODUCT_CAT = (
		("Virtual Reality", "VR"),
		("Argument Reality", "AR"),
		("Analytics", "analytics"),
		("Video Sharing", "video sharing"),
		("audio books", "audio books"),
		)
	catagory_name			=			models.CharField(max_length=50, blank=False, null=False, default=suggest_product())
	catagory_pitch			=			models.TextField(max_length=280, blank=True, null=True, default="Our revolutionary product will change the world", help_text="Catagory Detail")
	slug					=			models.SlugField(max_length=255, unique=True)
	# This field is to parse common words from the connected product's pitch.
	popular					=			models.TextField(max_length=1000, blank=True, null=True)
	UserBase				=			models.IntegerField(blank=True, null=True, default='0')
	total_revenue			= 			models.IntegerField(blank=True, null=True, default='0')
	avg_revenue				= 			models.IntegerField(blank=True, null=True, default='0')
	high_revenue			= 			models.IntegerField(blank=True, null=True, default='0')
	timestamp				=			models.DateTimeField(auto_now=False, auto_now_add=True)
	updated					=			models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return(self.catagory_name)

	def get_absolute_url(self):
		return reverse("user:catagory_detail", kwargs={'slug' : self.slug})

	class Meta:
		verbose_name 		= 			"Product Catagory"
		verbose_name_plural = 			"Product Catagories"

class anon_user_detail(models.Model):
	CONTACTS_LIST = (
		('Twitter', 'twitter'),
		('e-mail', 'email'),
		)
	contact					=			models.CharField(max_length=200, blank=False, null=False)
	contact_type			=			models.CharField(max_length=30, choices=CONTACTS_LIST, default=CONTACTS_LIST[0][0])
	connected_product		=			models.ForeignKey('product', related_name='product_connected', on_delete=models.CASCADE, default=1)
	
	def __str__(self):
		return(self.contact)

class product(models.Model):
	REV_INFO_SOURCE = (
		("from the Internet, unverified.", "internet, unverified"),
		("from the Internet, Admin Verified.", "internet, admin verified"),
		("verified by the Maker.", "maker verified"),
		("not for Public Viewing", "Not for public viewing"),
		)
	# who is uploading this product
	user					=			models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	# the product name
	product_name			=			models.CharField(max_length=50, blank=False, null=False, default=suggest_product())
	product_pitch			=			models.TextField(max_length=280, blank=True, null=True, default="Our revolutionary product will change the world", help_text="Product Pitch in less than 280 character")
	# If the product is uploaded by the maker, this needs to be done manually.
	product_verified 		=			models.BooleanField(default=False)
	slug					=			models.SlugField(max_length=255, unique=True)
	monthly_revenue			=			models.IntegerField(blank=False, null=False, default=0, help_text="Product's Current Monthly Revenue in USD. Enter '0' if product is in development phase.")
	# Added this on request of visitors
	revenue_source			=			models.ManyToManyField('revenue_source', blank=False, help_text='How do you get the revenue? please choose atleast one')
	revenue_info_source		=			models.CharField(max_length=50, choices=REV_INFO_SOURCE, default=REV_INFO_SOURCE[0][0])
	# the website url
	website					=			models.URLField(max_length=1000, blank=False, null=False, help_text="Your Landing page URL. When you choose to advert, your advert will divert to this URL.")
	# other website which are twins to this
	claimable				=			models.BooleanField(default=False)
	twin					=			models.ManyToManyField('product', blank=True, help_text="Websites which are very similar to your website.")
	tag 					=			models.ManyToManyField('tags', blank=True, help_text="Features your website offers.")

	catagory 				=			models.ForeignKey(product_catagory, related_name='catagory', default=1, on_delete=models.CASCADE)

	timestamp				=			models.DateTimeField(auto_now=False, auto_now_add=True)
	updated					=			models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return(self.product_name + str(" By ") + self.user.username)

	def get_absolute_url(self):
		return reverse("user:product_detail", kwargs={"slug" : self.slug})

	def get_claim_url(self):
		return reverse("user:claim_product", kwargs={"slug" : self.slug})

	class Meta:
		ordering	 		=			["-timestamp", "-updated"]
		verbose_name 		= 			"Product"
		verbose_name_plural = 			"Products"


class adverts(models.Model):
	app_name = "adverts"
	AD_STATUS = (
		("Unpaid", 'unpaid'),
		("Paid", 'paid'),
		('Displaying', 'displaying'),
		('Completed', 'completed'),
		)
	AD_LIFE = (
		(1, "1 Day"),
		(7, "7 Days"),
		(28, "28 Days"),
		)

	user					=			models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	customer				=			models.ForeignKey('product',related_name='product_advert', on_delete=models.CASCADE)
	ad_words				=			models.CharField(max_length=128, default=0, blank=True, null=True, help_text="Your advertisment text in 128 characters")
	advert_text				=			models.CharField(max_length=20, default='learn more', blank=False, null=False,help_text="Button text to redirect to your link")
	image = models.ImageField(
		help_text="Image size MUST be 350×250",
		upload_to=upload_location,
		null = True,
		blank = True,
		height_field = "height_field",
		width_field = "width_field",
	)
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)

	advert_status			=			models.CharField(max_length=20, choices=AD_STATUS, default=AD_STATUS[0][0])

	advert_view 			=			models.IntegerField(default=0)
	current_clicks			=			models.IntegerField(default=0)

	max_clicks				=			models.IntegerField(default=10, blank=True, null=True)
	advert_lifespan			=			models.IntegerField(choices=AD_LIFE, default=AD_LIFE[0][0], help_text="Number of days you want the advert to be live")
	advert_end				=			models.DateTimeField(editable=True)
	# advert_duration 		=			models.DurationField()
	timestamp				=			models.DateTimeField(auto_now=False, auto_now_add=True)
	updated					=			models.DateTimeField(auto_now=True, auto_now_add=False)
	
	def __str__(self):
		return (str(self.customer) + str(" by ") + str(self.user.username))

	class Meta:
		verbose_name 		= 			"Advert"
		verbose_name_plural = 			"Advertisments"

"""
	# This save function when enabled, doesnt allow other ANY OTHER FIELD to be edited, 
	# Neither from User interface, nor from admin or code.
	# Think how to over come this bug

	def save(self):
		d = timedelta(days=self.advert_lifespan)

		if not self.id:
			self.advert_end = datetime.now() + d
			super(adverts, self).save()
"""
	
# SLUG FOR PRODUCT
def slug_for_group(instance, new_slug=None):
	slug = slugify(instance.product_name)
	if new_slug is not None:
		slug = new_slug
	qs = product.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		# print("slug: " + str(slug))
		a = slug.split('-')
		# print("a: " + str(a[0]))
		new_slug = "%s-%s" %(a[0], qs.first().id)
		# print("new_slug: " + str(new_slug))
		# new_slug = "%s-%s" %(slug, qs.first().id)
		return slug_for_group(instance, new_slug=new_slug)
	return slug
def pre_save_group(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slug_for_group(instance)

# SLUG FOR TAGS
def slug_for_tag(instance, new_slug=None):
	slug = slugify(instance.product_name)
	if new_slug is not None:
		slug = new_slug
	qs = tags.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		# print("slug: " + str(slug))
		a = slug.split('-')
		# print("a: " + str(a[0]))
		new_slug = "%s-%s" %(a[0], qs.first().id)
		# print("new_slug: " + str(new_slug))
		# new_slug = "%s-%s" %(slug, qs.first().id)
		return slug_for_tag(instance, new_slug=new_slug)
	return slug
def pre_save_tag(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slug_for_tag(instance)

# SLUG FOR CATAGORY
def slug_for_catagory(instance, new_slug=None):
	slug = slugify(instance.catagory_name)
	if new_slug is not None:
		slug = new_slug
	qs = product_catagory.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		# print("slug: " + str(slug))
		a = slug.split('-')
		# print("a: " + str(a[0]))
		new_slug = "%s-%s" %(a[0], qs.first().id)
		# print("new_slug: " + str(new_slug))
		# new_slug = "%s-%s" %(slug, qs.first().id)
		return slug_for_catagory(instance, new_slug=new_slug)
	return slug
def pre_save_catagory(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slug_for_catagory(instance)


pre_save.connect(pre_save_group, sender=product)
pre_save.connect(pre_save_tag, sender=tags)
pre_save.connect(pre_save_catagory, sender=product_catagory)