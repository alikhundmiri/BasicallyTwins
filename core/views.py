from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.db import IntegrityError, transaction
from django.db.models import Q, Count
from django.forms.formsets import formset_factory
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.urls import reverse

from django.utils import timezone
from datetime import datetime, timedelta

from .models import product, tags, links, adverts, product_catagory, anon_user_detail, revenue_source, list_items
from .forms import ProductForm, EmailForm, AdvertForm, NewDetailForm, BaseDetailFormSet, ListOneForm
from . import catagory_utils, advert_utils, manager_start

from social_django.models import UserSocialAuth

import random
import json


def list_one(request):
	all_item_in_list = list_items.objects.filter(public_view=True)
	"""
	I have no idea why I am counting category,								^^^^^^^
	I should be counting "product" to find out the number of products each category is connected. 
	DONT CHANGE
	"""

	ads = advert_utils.fetch_adverts()
	context = {
		"all_item_in_list" : all_item_in_list,
		"ads" : ads,
		"show_ads" : True,
	}
	return render(request, 'core/list_one.html', context)	

@user_passes_test(lambda u: u.is_superuser)
def list_one_new(request):
	if not request.user.is_authenticated:
		raise Http404

	form = ListOneForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# form.save_m2m()
		return HttpResponseRedirect(reverse('list_one'))

	context = {
		'form' : form,
		"tab_text": "Submit Product",
		"top_text": "Enter the details for Websites which make users Revenue.",
		"form_text": "Please enter all the information below.",

	}
	return render(request, 'general_form.html', context)

"""
purpose : To display all the products which are flagged as claimable.
Claimable is found in the product model, and is flagged as True 
only when using the Anon user entry by Superuser accounts 

This has to be accessible by the unregistered users, doe not require user/Visitors to sign up to go to the next page.
"""
def claim_list(request):
	ads = advert_utils.fetch_adverts()
	products_ = product.objects.filter(claimable=True)

	context = {
		"products_" : products_,
		"ads" : ads,
		"show_ads" : True,
	}
	return render(request,"accounts/claim_list.html", context)

"""
purpose : To display a single product's details. 

This is the page where the user is verified and asked to signup via twitter.

This has to be accessible by the unregistered users, and divert them to login/register page when clicked.
"""
def claim_product(request, slug=None):
	contacts_ = anon_user_detail.objects.filter(connected_product__slug=slug)
	products_ = get_object_or_404(product, slug=slug, claimable=True)
	ads = advert_utils.fetch_adverts()

	user = request.user
	# Fetch this product's twitter Details
	twitter_login = None
	if user.is_authenticated:
		try:
			twitter_login = user.social_auth.get(provider='twitter')
		except UserSocialAuth.DoesNotExist:

			print("Trying failed " + str(twitter_login))
	
	# GOT IT

	twitter_id = None
	
	if twitter_login is not None:
		twitter_id = twitter_login.extra_data['access_token']['screen_name']
	product_twitter = ''
	for contact_ in contacts_:
		product_twitter = contact_.contact


	claim = False
	if product_twitter == twitter_id:
		claim = True

	print("product's attached Twitter : " + str(product_twitter))
	print("User's attached Twitter : " + str(twitter_id))

	context = {
		'claim' : claim,
		"contacts_" : contacts_,
		'twitter_login': twitter_login,
		"products_" : products_,
		"ads" : ads,
		"show_ads" : True,
	}
	return render(request,"accounts/claim_product.html", context)

"""
puprose : A page to process the transfer of product to the rightful creator. 
This step does not do any authntication, and the previous page have already verified.

This page does require the user to be logged in.
"""
@login_required
def check_claim(request, slug=None, username=None):
	products_ = get_object_or_404(product, slug=slug, claimable=True)

	user = request.user
	ads = advert_utils.fetch_adverts()

	claim_process(user, products_)

	context = {
		"ads" : ads,
		"show_ads" : True,
	}	
	return render(request,"accounts/claim_list.html", context)

"""
Purpose : Open the product's object from table, change the user to requested user,
and set the claimable flag as False
"""
def claim_process(user, products_):
	products_.user = user
	products_.claimable = False
	products_.save()
	
"""
Allow users to create new product listing.

by default, claimable is False here.
"""
@login_required
def create_product(request, username=None):
	if not request.user.is_authenticated:
		raise Http404

	form = ProductForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		form.save_m2m()
		catagory_utils.set_revenue_details(instance.catagory.slug)
		# here
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		'form' : form,
		"tab_text": "Submit Product",
		"top_text": "New Product",
		"form_text": "Please enter all the information below.",

	}
	return render(request, 'general_form.html', context)

"""
Purpose : allow the Super user to create a product listing on behalf of original creator.
An inline formset was used for this. and a seperate template was designed.
By default the Claimable flag is False.

KNOWN BUG: The field of revenue Source is not saved when this page is loaded.
THis is due to the field being a ManyToManyField, and i cant figure out how to save it.

Walkthough : While creating the object, make sure you select the Revenue source blanks,
and once it is saved, you can see all the details you entered, except the revenue source.
To fix this, edit the page (using the default form) and add in the Revenue Source.
"""
@user_passes_test(lambda u: u.is_superuser)
def admin_create_product(request, username=None):
	if not request.user.is_superuser:
		raise Http404
	user = request.user
	new_product = product()

	_revenue_source = revenue_source()

	DetailFormSet = formset_factory(NewDetailForm, formset=BaseDetailFormSet, extra=1, min_num=1, max_num=5, validate_max=True, validate_min=True)
	# print('Lets start...')
	if request.method == "POST":
		# print('Yup, request is POST')
		product_form = ProductForm(request.POST or None)
		detail_formset = DetailFormSet(request.POST)
		# print(product_form.is_valid())
		# print(detail_formset.is_valid())
		if product_form.is_valid() and detail_formset.is_valid():
			# print('product_form and detail_formset are valid...')
			new_product.catagory 				=		product_form.cleaned_data.get('catagory')
			new_product.product_name 			=		product_form.cleaned_data.get('product_name')
			new_product.product_pitch 			=		product_form.cleaned_data.get('product_pitch')
			new_product.website 				=		product_form.cleaned_data.get('website')
			new_product.monthly_revenue 		=		product_form.cleaned_data.get('monthly_revenue')
			new_product.claimable				=		True
			new_product.no_spam					=		True
			new_product.user 					=		user
			# Saving this above data
			new_product.save()
			# now get or create the revenue source, that requires the above fields saved in advance, hence we saved it in upper lines

			# new_product_revenue_source			=		product_form.cleaned_data.get('revenue_source')
			# new_revenue_source					=		revenue_source.objects.get_or_create(source = new_product_revenue_source)
			# new_product.revenue_source.add(new_revenue_source)
			print("Updating the revenue Details")
			catagory_utils.set_revenue_details(new_product.catagory.slug)
			
			# now save the data for each form in formset
			print('Saved all the details of product')
			new_details = []
			print('itterating through all details...')
			for detail_form in detail_formset:
				print('now at...' + str(detail_form))
				if detail_form.is_valid():
					contact = detail_form.cleaned_data.get('contact')
					contact_type = detail_form.cleaned_data.get('contact_type')
					if contact_type and contact:
						print("contact_type and contact are True")
						model_instance = anon_user_detail(connected_product=new_product)
						setattr(model_instance, 'contact', contact)
						setattr(model_instance, 'contact_type', contact_type)
						print(model_instance)
						new_details.append(model_instance)
						print(new_details)
			try:
				print('Trying...')

				with transaction.atomic():
					# Replace the old with the new
					# anon_user_detail.objects.filter(title=title).delete()
					print("Creating Bulk objects")
					anon_user_detail.objects.bulk_create(new_details)
					print("Created Bulk objects")
					# and notify our users that it worked
					messages.success(request, "Successfully submitted new entry")
					print("Starting the tweeting...")
					manager_start.initial_sort(new_product.product_name, new_product.slug, new_details)
					
					print('Done!')
			except IntegrityError: # if the transaction failed
				print('There was an error submitting your entry')
				messages.error(request, 'There was an error submitting your entry')
			return HttpResponseRedirect("/")

	else:
		product_form = ProductForm()
		detail_formset = DetailFormSet()

	context = {
		"tab_text": "Submit Product",
		"top_text": "New Product (Superuser)",
		"form_text": "(Superuser)",
		'product_form' : product_form,
		'link_formset' : detail_formset,
	}	
	return render(request, 'custom_general_form.html', context)

"""
purpose : Allowing the user to edit product details.
Requires the requested user to be same as registered user of the product.
"""
@login_required
def edit_product(request, slug=None, username=None):
	instance = get_object_or_404(product, slug=slug)
	if instance.user != request.user:
		raise Http404
	form = ProductForm(request.POST or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		form.save_m2m()
		catagory_utils.set_revenue_details(instance.catagory.slug)
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		'form' : form,
		"tab_text": "Submit Product",
		"top_text": "New Product",
		"form_text": "Please enter all the information below.",

	}
	return render(request, 'general_form.html', context)

"""
Purpose : Allow the deletion of product.

NOT TO SELF: When a user requests to delete any object, make is invisible to the general public 
and prompt the user with message like " You can revert this change in ext 24 hour." and delete after 24 hour.
"""
@login_required
def delete_product(request, slug=None, username=None):
	instance = get_object_or_404(product, slug=slug)
	if instance.user != request.user:
		raise Http404
	instance.delete()
	return HttpResponseRedirect(reverse('user:user_profile', kwargs={'username':username}))

"""
Load all adverts requested by an user.
"""
@login_required
def all_advert(request, username=None):
	advert = adverts.objects.filter(user__username=username)

	context = {
		"show_ads" : True,
		'all_adverts' : advert,
	}
	return render(request, 'core/all_adverts.html', context)

"""
Purpose : Allow the users to create new advert.

NOT TO SELF : Make this process Automated, with 
1. Integration of payment Gateway, prferably Paytm for Indian users and Stripe for International Users.
2. Know the difference between Date of payment, and date of registeration. 
	1. Create a new field "Payment_date", and set this as now, only when the payment is made,
	2. "advert_end" field should be modified depending on payment_date parameter.
3. Automatic Termination of advert after the period of advert is over.
4. Automatic Maling of "end of Advertising Contract" with details like total views and total clicks. 
"""
@login_required
def create_advert(request, username=None):
	self_products = product.objects.filter(user__username=username)

	form = AdvertForm(request.POST or None, request.FILES or None)
	# overriding the field to show only the products created by this user
	form.fields['customer'].queryset = self_products

	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		d = timedelta(days=instance.advert_lifespan)
		instance.advert_end = datetime.now() + d
		
		instance.save()
		form.save_m2m()

		return HttpResponseRedirect(reverse('user:all_advert', args=[username]))
	context = {
		'form' : form,
		"tab_text": "Submit Advert",
		"top_text": "Buy New Advert!",
		"form_text": "Either enter the Ad words, or Upload an Image. NOT BOTH.",

	}
	return render(request, 'general_form.html', context)

def edit_advert(request):
	context = {
		"item" : "item",
	}
	return render(request, 'general_form.html', context)
"""
Purpose : When an add is clicked on, this is the redirect view.

This will increment the clicked parameter on the advert and redirects to the advert's registered page.

This also check if the advert is out of its final days, and changes the show add field as False. 
This is done in advert_utils.ad_contract_completion
"""
def advert_redirect(request, id=None):
	
	# advert = get_object_or_404(adverts, id=id)
	advert = adverts.objects.filter(id=id)

	for ad in advert:
		newlink = ad.customer.website
		# print(newlink)
		ad.current_clicks += 1
		if timezone.now() > ad.advert_end:
			# if the number of clicks are equal to requested clicks, turn off the advert status
			advert_utils.ad_contract_completion(ad)
		else:
			pass
		ad.save()

	return HttpResponseRedirect(newlink)

def user_profile(request, username=None):
	# print(type(username))
	products = product.objects.filter(user__username=username)
	# for product_ in products:
		# print(product_)
	context = {
		# "page" : 'full-page',
		"products" : products,
		"show_ads" : False,
		"username" : username,
	}
	return render(request, 'user_profile.html', context)

def index(request):
	ads = advert_utils.fetch_adverts()
	products_ = product.objects.filter(no_spam=True)
	tags_ = tags.objects.all()
	links_ = links.objects.all()


	query = request.GET.get("q")
	if query:
		products_ = products_.filter(
			Q(product_name__icontains=query)|
			Q(product_pitch__icontains=query)|
			Q(catagory__catagory_name__icontains=query)|
			Q(catagory__catagory_pitch__icontains=query)|
			Q(twin__product_name__icontains=query)
		).distinct()

	paginator = Paginator(products_, 10) # show 10 Blogs per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		_products = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		_products = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		_products = paginator.page(paginator.num_pages)


	context = {
		"products_" : _products,
		"tags_" : tags_,
		"links_" : links_,
		"ads" : ads,
        "page_request_var" : page_request_var,
		"show_ads" : True,
	}
	return render(request, 'core/all_products.html', context)

def catagory_list(request):
	all_cats = product_catagory.objects.annotate(number_of_products=Count('catagory', distinct=True))
	"""
	I have no idea why I am counting category,								^^^^^^^
	I should be counting "product" to find out the number of products each category is connected. 
	DONT CHANGE
	"""

	ads = advert_utils.fetch_adverts()
	context = {
		"all_cats" : all_cats,
		"ads" : ads,
		"show_ads" : True,
	}
	return render(request, 'core/catagory_list.html', context)

def catagory_detail(request, slug=None):
	this_cat = get_object_or_404(product_catagory, slug=slug)
	products_ = product.objects.filter(catagory__slug=slug).order_by('-updated')
	
	total_revenue, avg_revenue, high_revenue = catagory_utils.revenue_details(this_cat, products_)

	query = request.GET.get("q")
	if query:
		products_ = products_.filter(
			Q(product_name__icontains=query)|
			Q(product_pitch__icontains=query)|
			Q(twin__product_name__icontains=query)
		).distinct()

	paginator = Paginator(products_, 10) # show 10 Blogs per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		_products = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		_products = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		_products = paginator.page(paginator.num_pages)

	ads = advert_utils.fetch_adverts()

	context = {
		'this_cat' : this_cat,
		'products_' : products_,
        "page_request_var" : page_request_var,
    	'total_revenue' : total_revenue,
    	'avg_revenue' : avg_revenue,
    	'high_revenue' : high_revenue,
    	"ads" : ads,
		"show_ads" : True,
	}
	return render(request, 'core/catagory_detail.html', context)


"""
	get the product

	get product's twins
	all the M2M it is connected
"""

def product_detail(request, slug=None):
	this_product = get_object_or_404(product, slug=slug)
	inspired_twins = product.objects.filter(twin=this_product)
	market_cap = 0
	# print("This products revenue > " + str(this_product.monthly_revenue))

	# products from same catagory

	this_catagory = product.objects.filter(catagory=this_product.catagory).exclude(id=this_product.id)
	# print(this_catagory)

	for g1 in this_product.twin.all():
		market_cap += g1.monthly_revenue
		# print("Other player's revenue > " + str(g1.monthly_revenue))

	for g2 in inspired_twins.all():
		market_cap += g2.monthly_revenue
		# print("Other player's revenue > " + str(g2.monthly_revenue))

	# print("market revenue > " + str(market_cap))
	ads = advert_utils.fetch_adverts()
	links_ = links.objects.filter(social_connection=this_product)

	context = {
		"product" : this_product,
		"inspired_twins" : inspired_twins,
		"links_" : links_,
		"ads" : ads,
		"market_cap" : market_cap,
		'this_catagory' : this_catagory,
		"show_ads" : False,
	}
	return render(request, 'core/product_detail.html', context)

'''
	List of all tags with
		1. tag name
		2. number of products with that tag
		3. total estimated market cap caculated with summing all revenue
'''

def all_tags(request):
	return render(request, 'core/twinslist.html')

def tag_detail(request, slug=None):
	return render(request, 'core/twinslist.html')

def lander(request):

	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('user:home'))
	else:
		pass

	form = EmailForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

	context = {
		'page' : 'full-page',
		'form' : form,
	}

	return render(request, 'lander.html', context)
