from .models import product, product_catagory
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

all_revenue = []
def revenue_details(this_cat, products_):
		
	# print("FETCHING FROM this_cat...")
	total_revenue = this_cat.total_revenue
	# print("total_revenue \t: \t\t" + str(total_revenue))
	avg_revenue = this_cat.avg_revenue
	# print("avg_revenue \t: \t\t" + str(avg_revenue))
	high_revenue = this_cat.high_revenue
	# print("high_revenue \t: \t\t" + str(high_revenue))
	return (total_revenue, avg_revenue, high_revenue)

def set_revenue_details(slug=None):
	this_cat = get_object_or_404(product_catagory, slug=slug)
	products_ = product.objects.filter(catagory__slug=slug).order_by('-updated')
	total_revenue = 0
	avg_revenue = 0
	high_revenue = 0
	# print("Creating Values...")
	# print("This catagory last update \t\t" + str(this_cat.updated))
	# print("Product added last update \t\t" + str(products_[0].updated))

	for p in products_:
		# print(p.monthly_revenue)
		total_revenue += p.monthly_revenue
		all_revenue.append(p.monthly_revenue)

	# print("Total revenue \t\t: \t\t" + str(total_revenue))
	# print("Total products \t\t: \t\t" + str(products_.count()))

	avg_revenue = total_revenue/(products_.count())
	high_revenue = max(all_revenue)
	high_revenue_product = products_.filter(monthly_revenue=high_revenue)

	# print("Average revenue \t: \t\t" + str(avg_revenue))
	# print("Highest revenue \t: \t\t" + str(high_revenue) + " by " + str(high_revenue_product))
	# print("saving TO this_cat...")
	this_cat.total_revenue = total_revenue
	this_cat.avg_revenue = avg_revenue
	this_cat.high_revenue = high_revenue
	this_cat.save()
	# print("Saved!")

	return (total_revenue, avg_revenue, high_revenue)